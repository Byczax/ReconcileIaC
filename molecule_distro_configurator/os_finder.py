import re
import os
from distro_fetcher import fetcher

def find_md_files(root_folder):
    files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('README.md'):
                print(os.path.join(dirpath, filename))
                files.append(os.path.join(dirpath, filename))
    return files



def normalize_text(text):
    """Normalize text by removing whitespaces and converting to lowercase."""
    # return re.sub(r'\s+', '', text).lower()
    return text.lower()

def read_file(file_path):
    """Read the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def match_operating_systems(file, operating_systems):
    normalized_os = [normalize_text(os_name) for os_name in operating_systems]
    # print(f"Checking file '{file}'...")
    if not os.path.isfile(file):
        print(f"File '{file}' does not exist.")
        return None

    file_content = read_file(file)
    normalized_content = normalize_text(file_content)

    matched_os = []
    for os_name in normalized_os:
        if os_name in normalized_content:
            matched_os.append(os_name)
    # color print
    # print(f"\033[92m{matched_os}\033[0m")
    
    return matched_os

if __name__ == "__main__":
    files = find_md_files('examples/ansible-examples-master')
    print("=== FOUND FILES ===")
    
    operating_systems = fetcher()
    print("=== FOUND OPERATING SYSTEMS ===")
    for file in files:
        matches = match_operating_systems(file, operating_systems)
        print(f"\033[92m{matches}\033[0m")
    


