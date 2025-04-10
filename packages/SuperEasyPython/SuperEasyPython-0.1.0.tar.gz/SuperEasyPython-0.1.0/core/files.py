from pathlib import Path
import json

def read_lines(file_path: str) -> list:
    """Reads a file line by line."""
    return Path(file_path).read_text().splitlines()

def write_json(data: dict, file_path: str):
    """Saves a dictionary to a JSON file."""
    Path(file_path).write_text(json.dumps(data, indent=4))