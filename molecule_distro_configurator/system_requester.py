import requests
from datetime import datetime
import os
from distro_fetcher import fetcher
from os_finder import find_md_files, match_operating_systems
from distutils.dir_util import copy_tree

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

            if "latest" in tag_names:
                print(f"Latest Docker image for {os_name}: {os_name}:latest")
                selected_tag = "latest"
            elif "stable" in tag_names:
                print(f"Stable Docker image for {os_name}: {os_name}:stable")
                selected_tag = "stable"
            else:
                newest_tag = "unstable"
                index = 0
                while "unstable" in newest_tag:
                    tags.sort(
                        key=lambda x: datetime.strptime(
                            x["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        reverse=True,
                    )
                    newest_tag = tags[index]["name"] if tags else "No tags available"
                    index += 1
                else:
                    print(f"Newest Docker image for {os_name}: {os_name}:{newest_tag}")
                    selected_tag = newest_tag
        else:
            print(
                f"\033[91mFailed to fetch images for {os_name}. HTTP Status code: {response.status_code}\033[0m"
            )

        system_tags[os_name] = selected_tag
    return system_tags


def write_to_molecule(tags):
    molecule_systems = ""

    for entry in tags:
        if tags[entry] is None:
            print(f"\033[91mNo tag found for {entry}\033[0m")
            continue
        molecule_systems += f"  - name: {entry}\n"
        molecule_systems += f"    image: {entry}:{tags[entry]}\n"
    copy_tree("../template/molecule", "../molecule")
    # os.system("mkdir -p ../molecule/default")

    with open("../template/molecule/default/molecule.yml", "r") as infile, open(
        "../molecule/default/molecule.yml", "w+"
    ) as outfile:
        data = infile.read()
        print(data)
        data = data.replace("# FOUND_SYSTEMS #", molecule_systems)

        outfile.write(data)


if __name__ == "__main__":
    #TODO remove it, replace with normal file reader, commented below
    files = find_md_files("../examples/ansible-examples-master")
    # file = sys.argv[1]
    
    operating_systems = fetcher()
    #! EXCEPTIONS
    operating_systems.append("RHEL")

    file = files[6]
    matches = match_operating_systems(file, operating_systems)
    #! EXCEPTIONS
    if "centos" in matches:
        matches.remove("centos")
        matches.append("rockylinux")

    print(f"\033[92m{matches}\033[0m")
    
    if matches == []:
        print("\033[91mNo OS found in the file\033[0m")
        print("\033[93mAdding default (ubuntu)...\033[0m")
        matches.append("ubuntu")

    tags = fetch_docker_images(matches)
    print(f"\033[95m{tags}\033[0m")
    print("===")

    write_to_molecule(tags)
