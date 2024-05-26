import argparse
import os
import shutil
import subprocess
import sys
from molecule_distro_configurator import configurator_script

# Define ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"


def run_molecule_distro_configurator(
    ansible_project_path, run_tests, clean, interferer_flags
):
    configurator_path = os.path.join(os.getcwd(), "molecule_distro_configurator")

    if not os.path.exists(ansible_project_path):
        print(
            f"{RED}[MolDiCo] The specified Ansible project path does not exist: {ansible_project_path}{RESET}"
        )
        sys.exit(1)

    if not os.path.exists(configurator_path):
        print(
            f"{RED}[MolDiCo] The configurator path does not exist: {configurator_path}{RESET}"
        )
        sys.exit(1)

    try:
        result = configurator_script.run_script(ansible_project_path, interferer_flags)

        # Optionally run molecule test
        if run_tests and result:
            print(f"{BLUE}[MolDiCo] Running 'molecule test'...{RESET}")

            project_path = configurator_script.BASE_PROJECT_PATH
            # change os directory
            os.chdir(project_path)
            result = subprocess.run(["molecule", "-vvv", "test"], check=True)
            print(
                f"{GREEN}[MolDiCo] 'molecule test' completed with return code: {result.returncode}{RESET}"
            )

        if clean:
            try:
                shutil.rmtree(project_path)
                print(
                    f"[MolDiCo] Directory '{project_path}' and its contents have been successfully removed."
                )
            except OSError as e:
                print(f"[MolDiCo] Error: {project_path} : {e.strerror}")

    except subprocess.CalledProcessError as e:
        print(f"{RED}[MolDiCo] An error occurred while running the command: {e}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[MolDiCo] An unexpected error occurred: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"{GREEN}Run molecule_distro_configurator on an Ansible project.{RESET}"
    )
    parser.add_argument(
        "ansible_project_path", type=str, help="Path to the Ansible project folder."
    )
    parser.add_argument(
        "--test", action="store_true", help='Automatically run "molecule test".'
    )
    parser.add_argument(
        "--clean", action="store_true", help="Remove all generated files."
    )

    # Interferer

    parser.add_argument(
        "--uninstall_package",
        action="store_true",
        help="Uninstalls a package",
    )
    parser.add_argument("--stop_service", action="store_true", help="Stops a service")
    parser.add_argument(
        "--change_file_ownership",
        action="store_true",
        help="Changes ownership of a file",
    )
    parser.add_argument(
        "--change_file_permissions",
        action="store_true",
        help="Changes permissions of a file",
    )
    parser.add_argument(
        "--bring_network_interface_down",
        action="store_true",
        help="Brings down a network interface",
    )

    args = parser.parse_args()

    interferer_flags = [
        "--uninstall_package" if args.uninstall_package else "",
        "--stop_service" if args.stop_service else "",
        "--change_file_ownership" if args.change_file_ownership else "",
        "--change_file_permissions" if args.change_file_permissions else "",
        "--bring_network_interface_down" if args.bring_network_interface_down else "",
    ]
    run_molecule_distro_configurator(
        args.ansible_project_path,
        args.test,
        args.clean,
        [f for f in interferer_flags if f],
    )
