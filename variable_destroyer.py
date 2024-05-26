import os
import re
from ruamel.yaml import YAML

def is_path(value):
    """Check if a value is a path."""
    # Simple heuristic to determine if a value is a path
    return isinstance(value, str) and ('/' in value or '\\' in value)

def replace_values(data):
    """Recursively replace values in the data."""
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_values(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = replace_values(data[i])
    elif isinstance(data, str) and is_path(data):
        return 'X' * len(data)
    elif isinstance(data, bool):
        return 'T' * len(str(data))
    elif isinstance(data, (int, float)):
        return 'O' * len(str(data))
    return data

def process_yaml_file(file_path):
    yaml = YAML()
    with open(file_path, 'r') as f:
        data = yaml.load(f)

    modified_data = replace_values(data)

    with open(file_path, 'w') as f:
        yaml.dump(modified_data, f)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yml', '.yaml')):
                file_path = os.path.join(root, file)
                process_yaml_file(file_path)

if __name__ == "__main__":
    process_yaml_file("test.yaml")
