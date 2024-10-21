import nmap
import paramiko


def scan_subnet(subnet):
    """Scan the given subnet for open SSH ports (22)."""
    nm = nmap.PortScanner()
    nm.scan(subnet, '22')  # Scanning for SSH port (22)
    hosts = []

    for host in nm.all_hosts():
        if 'tcp' in nm[host] and nm[host]['tcp'][22]['state'] == 'open':
            hosts.append(host)
    return hosts


def change_password(host, username, old_password, new_password):
    """Change the root password on the specified host using SSH."""
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=old_password)

        # Command to change the root password
        stdin, stdout, stderr = ssh.exec_command(f'echo -e "{new_password}\\n{new_password}" | passwd root')
        stdout.channel.recv_exit_status()  # Wait for command to finish

        ssh.close()
        print(f"Password successfully changed on {host}.")
        return True
    except Exception as e:
        print(f"Failed to connect or change password on {host}: {str(e)}")
        return False


def verify_password(host, username, new_password):
    """Verify if the new password works by logging in via SSH."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=new_password)

        # Run a simple command to verify access
        stdin, stdout, stderr = ssh.exec_command('whoami')
        if stdout.read().strip() == 'root':
            print(f"Successfully verified root access on {host}.")
            ssh.close()
            return True
        else:
            print(f"Failed to verify root access on {host}.")
            ssh.close()
            return False
    except Exception as e:
        print(f"Failed to verify root access on {host}: {str(e)}")
        return False


def main(subnet, username, old_password, new_password):
    """Main function to scan, change passwords, and verify them."""
    print(f"Scanning subnet {subnet} for SSH servers...")
    hosts = scan_subnet(subnet)

    if not hosts:
        print("No SSH hosts found.")
        return

    for host in hosts:
        print(f"Attempting to change password on {host}...")
        if change_password(host, username, old_password, new_password):
            print(f"Password changed on {host}. Verifying...")
            verify_password(host, username, new_password)
        else:
            print(f"Password change failed on {host}. Skipping verification.")


if __name__ == "__main__":
    subnet = "192.168.1.0/24"  # Example subnet, change to target subnet
    username = "root"
    old_password = "oldpassword"  # Replace with the known old password
    new_password = "newpassword"  # Replace with the new password you want to set

    main(subnet, username, old_password, new_password)