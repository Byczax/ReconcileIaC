import subprocess

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
    command = f"sudo apt-get remove -y {package_name}"
    run_command(command)

def stop_service(service_name):
    """Stop a service."""
    command = f"sudo systemctl stop {service_name}"
    run_command(command)

def change_file_ownership(file_path, owner, group):
    """Change file ownership."""
    command = f"sudo chown {owner}:{group} {file_path}"
    run_command(command)

def change_file_permissions(file_path, permissions):
    """Change file permissions."""
    command = f"sudo chmod {permissions} {file_path}"
    run_command(command)

def bring_network_interface_down(interface):
    """Bring a network interface down."""
    command = f"sudo ifconfig {interface} down"
    run_command(command)

def main():
    """Main function to perform system mutations."""
    # Uninstall Apache
    uninstall_package('apache2')
    
    # Stop Apache service
    stop_service('apache2')
    
    # Change ownership of the web directory
    change_file_ownership('/var/www/html/index.html', 'root', 'root')
    
    # Change permissions of the index.html file
    change_file_permissions('/var/www/html/index.html', '0600')
    
    # Bring down the network interface
    bring_network_interface_down('eth0')

if __name__ == "__main__":
    # BE CAREFUL! Uncommenting the next line will execute the main function
    # This will perform system mutations
    # Only uncomment this line if you not on your system but in ex. VM
    pass
    # main()
