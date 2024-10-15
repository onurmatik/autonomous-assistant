import json
import os
import shutil
import argparse
import string
import random
from datetime import datetime
from time import sleep

from dotenv import load_dotenv, set_key, dotenv_values
from openai import Client
import functions
import config


load_dotenv()

client = Client()


if config.VECTOR_STORE_ID is None:
    # Create the vector store and save its ID as an environment variable
    vector_store = client.beta.vector_stores.create(
        name="AA vector store",
    )
    config.VECTOR_STORE_ID = vector_store.id
    set_key(".env", "VECTOR_STORE_ID", config.VECTOR_STORE_ID)
    print("Vector store created:", config.VECTOR_STORE_ID)


ASSISTANT_DEFINITION = {
    "name": "Autonomous Assistant",
    "description": "An AI assistant that plans and executes tasks to achieve the given objective",
    "instructions": f"You are an AI assistant that plans and executes tasks to achieve the given objective.\n"
                    f"After each step, evaluate the result and decide the next best action.\n\n"
                    f"You have access to the following functions:\n"
                    f"{"".join(f"{fn['name']}: {fn['description']}\n" for fn in functions.DEFINITIONS)}\n"
                    f"Considering what you already know, think thoroughly and critically about "
                    f"what additional information you need and which function to call next.\n\n"
                    f"OBJECTIVE:\n{config.OBJECTIVE}",
    "model": config.MODEL,
    "tools": [{
        "type": "file_search"
    }, {
        "type": "code_interpreter"
    }] + [{
        "type": "function",
        "function": fn,
    } for fn in functions.DEFINITIONS],
    "tool_resources": {
        "file_search": {
            "vector_store_ids": [config.VECTOR_STORE_ID]
        }
    },
}


if config.ASSISTANT_ID is None:
    # Create the assistant and save its ID as an environment variable
    assistant = client.beta.assistants.create(**ASSISTANT_DEFINITION)
    config.ASSISTANT_ID = assistant.id
    set_key(".env", "ASSISTANT_ID", config.ASSISTANT_ID)
    print("Assistant created:", config.ASSISTANT_ID)


assistant = client.beta.assistants.retrieve(config.ASSISTANT_ID)


if config.THREAD_ID is None:
    thread = client.beta.threads.create()
    config.THREAD_ID = thread.id
    set_key(".env", "THREAD_ID", config.THREAD_ID)
    print("Thread created:", config.THREAD_ID)


thread = client.beta.threads.retrieve(config.THREAD_ID)


def run_assistant():
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S.') + f"{now.microsecond // 1000:03d}"  # time with milliseconds

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"{now.strftime('%Y-%m-%d %H:%M')}: "
                f"Considering what you know and what you have done so far, "
                f"what would be your next move to achieve your objective?",
        metadata={'timestamp': timestamp}
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    print("Waiting for the assistant's response...")

    while run.status != 'completed':
        if run.status == 'requires_action':
            tool_outputs = []
            max_total_size = 510 * 1024  # 512 KB size limit; keep 2 KB for "trimmed" messages
            total_size = 0
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S.') + f"{now.microsecond // 1000:03d}"

                function_name = tool.function.name
                arguments = json.loads(tool.function.arguments)

                try:
                    output = getattr(functions, function_name)(**arguments) or ''
                except AttributeError:
                    output = f"[Error: {function_name} does not exist]"

                output_bytes = output.encode('utf-8')
                output_size = len(output_bytes)

                # If adding this output exceeds the total size limit, trim it
                if total_size + output_size > max_total_size:
                    remaining_size = max_total_size - total_size
                    trimmed_bytes = output_bytes[:remaining_size]
                    output = trimmed_bytes.decode('utf-8', errors='ignore') + ' ... [trimmed]'
                    output_size = len(output.encode('utf-8'))  # Recalculate trimmed size

                total_size += output_size  # Update the running total

                if total_size + output_size > max_total_size:
                    output = '[Total output size exceeded. Skipping. You can repeat the call separately.]'

                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": output,
                })

                log_key = f"{timestamp}_{function_name}_{''.join(random.choices(string.ascii_letters, k=4))}.out"
                with open("./logs/" + log_key, 'w', encoding='utf-8') as log_file:
                    log_file.write(output)

            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        sleep(0.1)

    run_assistant()


def list_messages():
    # List the assistant's responses
    thread_messages = client.beta.threads.messages.list(thread_id=config.THREAD_ID, order="asc")
    for message in thread_messages.data:
        if message.role == "user":
            print(message.metadata.get('datetime'))
        else:
            for content in message.content:
                print("\nASSISTANT:", content.text.value)


def reset_thread():
    # Remove the thread
    env_vars = dotenv_values(".env")
    if 'THREAD_ID' in env_vars:
        client.beta.threads.delete(config.THREAD_ID)
        with open('.env', 'w'):
            pass
        for key, val in env_vars.items():
            if key != 'THREAD_ID':
                set_key(".env", key, val)

    # Remove the logs
    for filename in os.listdir("./logs"):
        os.remove(f"./logs/{filename}")

    # Remove the outputs
    outputs_dir = "./outputs"
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir, exist_ok=True)

    print("Thread reset done.")


def update_assistant():
    client.beta.assistants.update(config.ASSISTANT_ID, **ASSISTANT_DEFINITION)
    print("Assistant updated.")


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Run assistant or list messages.")
    parser.add_argument(
        'action',
        choices=['run', 'thread', 'reset', 'update'],
        help="run: run the assistant\n"
             "thread: list assistant's responses\n"
             "update: update the assistant\n"
             "reset: reset the thread"
    )
    args = parser.parse_args()

    if args.action == 'run':
        run_assistant()
    elif args.action == 'thread':
        list_messages()
    elif args.action == 'reset':
        reset_thread()
    elif args.action == 'update':
        update_assistant()


if __name__ == '__main__':
    main()
