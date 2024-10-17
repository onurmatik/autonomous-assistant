# Autonomous Assistant

An experimental autonomous AI assistant that plans and executes tasks to achieve a given objective using OpenAI’s API.

## Overview

This project implements an AI assistant capable of autonomously planning and executing tasks to achieve a specified objective. It leverages the beta features of the OpenAI API, including assistants, threads, and vector stores.

The assistant interacts with functions defined in a separate functions module, allowing it to perform various actions during its planning and execution phases.

## Features

- **Autonomous Task Planning:** The assistant can determine the next logical steps to achieve the defined objective without manual intervention.
- **Function Calling:** Utilizes function calling to perform specific tasks, enabling more complex operations.
- **Persistent State:** Stores assistant, thread, and vector store IDs in a `.env` file for continuity between runs.
- **Command-Line Interface:** Offers a simple CLI to run, reset, update, or list messages from the assistant.
- **Logging:** Records function outputs and assistant responses for review and debugging.

## Prerequisites

- **Python:** Version 3.7 or higher.
- **OpenAI API Key:** An API key with access to the beta features (assistants, threads, vector stores).
- **Dependencies:** Listed in `requirements.txt`.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/autonomous-ai-assistant.git
    cd autonomous-ai-assistant
    ```

2. **Create a Virtual Environment (Optional)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your-openai-api-key
    ```

## Configuration

The assistant’s behavior and settings can be configured via the `config.py` file:

- **OBJECTIVE:** The main objective for the assistant to achieve.
- **MODEL:** The OpenAI model to use (e.g., `'gpt-4'`).
- **ASSISTANT_ID, THREAD_ID, VECTOR_STORE_ID:** Managed automatically but can be set manually if needed.

## Usage

The script provides a command-line interface with several actions:

```bash
python assistant.py [action]
```

## Actions

- **run:** Start the assistant’s autonomous execution loop.
- **thread:** List the messages in the current thread, including the assistant’s responses.
- **reset:** Reset the current thread and clear logs and outputs.
- **update:** Update the assistant’s configuration.

```bash
python assistant.py [action]
```

## Function Definitions

The assistant can call various functions defined in the `functions.py` module. These functions are registered with the assistant and can perform specific tasks.

- **Adding Functions:** You can add or modify functions in `functions.py` to extend the assistant’s capabilities.
- **Function Registration:** Ensure new functions are added to the `DEFINITIONS` list in `functions.py` for the assistant to recognize them.

## Logging and Outputs

- **Logs:** Outputs of function calls are stored in the `./logs` directory.
- **Outputs:** Assistant's outputs or results are stored in the `./outputs` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.