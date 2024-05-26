import argparse
import os
import subprocess
import sys
from molecule_distro_configurator import configurator_script

# Define ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def run_molecule_distro_configurator(ansible_project_path, run_tests):
    configurator_path = os.path.join(os.getcwd(), 'molecule_distro_configurator')

    if not os.path.exists(ansible_project_path):
        print(f"{RED}The specified Ansible project path does not exist: {ansible_project_path}{RESET}")
        sys.exit(1)

    if not os.path.exists(configurator_path):
        print(f"{RED}The configurator path does not exist: {configurator_path}{RESET}")
        sys.exit(1)

    try:
        result = configurator_script.run_script(ansible_project_path)
        exit()

        # Optionally run molecule test
        if run_tests and result:
            print(f"{BLUE}Running 'molecule test'...{RESET}")
            result = subprocess.run(['molecule', 'test'], check=True)
            print(f"{GREEN}'molecule test' completed with return code: {result.returncode}{RESET}")

    except subprocess.CalledProcessError as e:
        print(f"{RED}An error occurred while running the command: {e}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f'{GREEN}Run molecule_distro_configurator on an Ansible project.{RESET}')
    parser.add_argument('ansible_project_path', type=str, help='Path to the Ansible project folder.')
    parser.add_argument('--test', action='store_true', help='Automatically run "molecule test".')

    args = parser.parse_args()
    run_molecule_distro_configurator(args.ansible_project_path, args.test)
