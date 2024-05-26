import subprocess
import argparse


def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command succeeded: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Error: {e}")


def uninstall_package(package_name):
    """Uninstall a package."""
    command = f"apt-get remove -y {package_name}"
    run_command(command)


def stop_service(service_name):
    """Stop a service."""
    command = f"systemctl stop {service_name}"
    run_command(command)


def change_file_ownership(file_path, owner, group):
    """Change file ownership."""
    command = f"chown {owner}:{group} {file_path}"
    run_command(command)


def change_file_permissions(file_path, permissions):
    """Change file permissions."""
    command = f"chmod {permissions} {file_path}"
    run_command(command)


def bring_network_interface_down(interface):
    """Bring a network interface down."""
    command = f"ifconfig {interface} down"
    run_command(command)


def main():
    """Main function to perform system mutations."""
    parser = argparse.ArgumentParser(description="System interferer.")
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

    if args.uninstall_package:
        uninstall_package("apache2")

    if args.stop_service:
        stop_service("apache2")

    if args.change_file_ownership:
        change_file_ownership("/var/www/html/index.html", "root", "root")

    if args.change_file_permissions:
        change_file_permissions("/var/www/html/index.html", "0600")

    if args.bring_network_interface_down:
        bring_network_interface_down("eth0")


if __name__ == "__main__":
    main()
