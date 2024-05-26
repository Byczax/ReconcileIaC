import requests
from datetime import datetime
import os, shutil
from molecule_distro_configurator.distro_fetcher import fetcher
from molecule_distro_configurator.os_finder import (
    find_md_files,
    match_operating_systems,
)
from distutils.dir_util import copy_tree

BASE_PATH = "molecule_distro_configurator"
BASE_PROJECT_PATH = "ansible-tester"


def fetch_docker_images(os_list):
    base_url = "https://hub.docker.com/v2/repositories/library/"

    system_tags = {}
    for os_name in os_list:
        url = f"{base_url}{os_name}/tags"
        response = requests.get(url)
        selected_tag = None
        if response.status_code == 200:
            data = response.json()
            tags = data["results"]
            tag_names = [tag["name"] for tag in tags]
            tags.sort(
                key=lambda x: datetime.strptime(
                    x["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                reverse=True,
            )
            if "latest" in tag_names:
                print(f"[MolDiCo] Latest Docker image for {os_name}: {os_name}:latest")
                selected_tag = "latest"
            elif "stable" in tag_names:
                print(f"[MolDiCo] Stable Docker image for {os_name}: {os_name}:stable")
                selected_tag = "stable"
            else:
                newest_tag = "unstable"
                index = 0
                while "unstable" in newest_tag or "minimal" in newest_tag:
                    newest_tag = tags[index]["name"] if tags else "No tags available"
                    index += 1
                else:
                    print(
                        f"[MolDiCo] Newest Docker image for {os_name}: {os_name}:{newest_tag}"
                    )
                    selected_tag = newest_tag
            if selected_tag is None:
                newest_tag = tags[0]["name"] if tags else "No tags available"
        else:
            print(
                f"\033[91m[MolDiCo] Failed to fetch images for {os_name}. HTTP Status code: {response.status_code}\033[0m"
            )

        system_tags[os_name] = selected_tag
    return system_tags


def write_to_molecule(tags):
    molecule_systems = ""

    for entry in tags:
        if tags[entry] is None:
            print(f"\033[91m[MolDiCo] No tag found for {entry}\033[0m")
            continue
        molecule_systems += f"  - name: {entry}\n"
        molecule_systems += f"    image: {entry}:{tags[entry]}\n"
    copy_tree(BASE_PATH + "/template/molecule", BASE_PROJECT_PATH + "/molecule")

    with open(
        BASE_PATH + "/template/molecule/default/molecule.yml", "r"
    ) as infile, open(
        BASE_PROJECT_PATH + "/molecule/default/molecule.yml", "w+"
    ) as outfile:
        data = infile.read()
        data = data.replace("# FOUND_SYSTEMS #", molecule_systems)

        outfile.write(data)


def find_yaml_project_file(project_path):

    yaml_files = []
    for file in os.listdir(project_path):
        if file.endswith((".yaml", ".yml")):
            yaml_files.append(os.path.join(project_path, file))
    return yaml_files


def write_to_converge(yaml_files):
    to_append = ""
    for file in yaml_files:
        basename = os.path.basename(file)
        to_append += f"- name: Include playbook {basename}\n"
        to_append += f"  ansible.builtin.import_playbook: ../../{basename}\n\n"

    with open(
        f"{BASE_PROJECT_PATH}/molecule/default/converge.yml", "a"
    ) as converge_file:
        converge_file.write(to_append)


def copy_files_to_test_dir(src_dir, dst_dir=BASE_PROJECT_PATH):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        elif os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)


def run_script(project_path):
    files = find_md_files(project_path)
    file = files[0]
    operating_systems = fetcher(BASE_PATH)

    matches = match_operating_systems(file, operating_systems)
    print(f"\033[92m[MolDiCo] {matches}\033[0m")

    tags = fetch_docker_images(matches)
    if not tags:
        print("\033[91m[MolDiCo] No tags found\033[0m")
        return False
    print(f"\033[95m[MolDiCo] {tags}\033[0m")

    write_to_molecule(tags)

    copy_files_to_test_dir(project_path)

    yaml_files = find_yaml_project_file(project_path)
    if not yaml_files:
        print("\033[91m[MolDiCo] No YAML file found in the project path\033[0m")
        return False

    write_to_converge(yaml_files)

    return True
