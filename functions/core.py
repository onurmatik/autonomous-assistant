import os
from time import sleep as _sleep


DEFINITIONS = [
    {
        "name": "write_file",
        "description": "Writes content to a file in the specified folder, which can be retrieved later. "
                       "Use this function when you want to store insights, intermediate outputs, or final results "
                       "aligned with your objectives for future reference or publishing.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The content to be written into the file. This can be text, insights, "
                                   "or generated outputs."
                },
                "folder": {
                    "type": "string",
                    "description": "The target folder where the file will be stored. "
                                   "Organize files under folders as you find appropriate. "
                                   "For example you can use 'insights' for analytical findings, "
                                   "'publish' for content intended for distribution, "
                                   "and 'notes' for miscellaneous records."
                },
                "filename": {
                    "type": "string",
                    "description": "The name of the file, including its extension (e.g., 'report.txt', 'insight.md')."
                }
            },
            "required": ["content", "folder", "filename"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of the given file under the given folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "The folder where the file is stored."
                },
                "filename": {
                    "type": "string",
                    "description": "The name of the file to read."
                }
            },
            "required": ["folder", "filename"]
        }
    },
    {
        "name": "list_folders",
        "description": "List the folders available.",
    },
    {
        "name": "list_files",
        "description": "List the files in the given folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "The folder where the file is stored."
                },
                "filename": {
                    "type": "string",
                    "description": "The name of the file to read."
                }
            },
            "required": ["folder", "filename"]
        }
    },
    {
        "name": "sleep",
        "description": "Do nothing for the given period.",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "string",
                    "description": "The duration to sleep."
                },
            },
            "required": ["duration"]
        }
    },
]


def write_file(content: str, folder: str, filename: str) -> None:
    """
    Writes content to a file in the specified folder, which can be retrieved later.
    Use this function when you want to store insights, intermediate outputs, or final results
    aligned with your objectives for future reference or publishing.
    """
    full_folder_path = f"./outputs/{folder}"
    file_path = os.path.join(full_folder_path, filename)

    # Create the folder if not exists
    os.makedirs(full_folder_path, exist_ok=True)

    print(f"Writing {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_file(folder, name):
    """
    Read the contents of the given file.
    """
    try:
        file_path = os.path.join(f".{folder}", name)
        with open(file_path, 'r') as f:
            return f.read()
    except (FileNotFoundError, IsADirectoryError):
        return (
            f"File '{name}' not found in folder '{folder}'. "
            f"You may want to get a list of available files with list_files('{folder}') first."
        )


def list_folders():
    """
    Returns a list of subfolders in the given folder.
    """
    outputs_folder = "./outputs"
    return "\n".join([
        name for name in os.listdir(outputs_folder)
        if os.path.isdir(os.path.join(outputs_folder, name))
    ])


def list_files(folder: str):
    """
    Returns a list of files in the given folder.
    """
    try:
        return "\n".join([
            name for name in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, name))
        ])
    except (FileNotFoundError, NotADirectoryError):
        return (
            f"There is no directory called '{folder}'. "
            f"You may want to call 'list_folders' first to get a list of available folders."
        )


def sleep(duration):
    """
    Do nothing for the given period.
    """
    print(f"Sleeping for {duration} seconds")
    _sleep(duration)
