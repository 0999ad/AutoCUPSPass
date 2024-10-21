import nmap
import paramiko
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

subnet = os.getenv("subnet")
username = os.getenv("username")
new_password = os.getenv("new_password")
password_file = 'passwords.txt'  # Ensure this file contains possible old passwords

def scan_subnet(subnet):
    print(f"Scanning subnet {subnet} for hosts...")
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sn')  # Ping scan
    return nm.all_hosts()

def read_passwords(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f.readlines()]

def change_password(host, client):
    try:
        # Open a session
        ssh_session = client.invoke_shell()
        
        # Execute the command to change the password
        ssh_session.send(f'passwd {username}\n')
        ssh_session.send(f'{new_password}\n')
        ssh_session.send(f'{new_password}\n')
        
        # Wait for the command to complete
        time.sleep(1)
        
        # Check the output
        output = ssh_session.recv(1024).decode('utf-8')
        print(f"Password changed on {host}: {output}")
        return True
    except Exception as e:
        print(f"Error changing password on {host}: {e}")
        return False

def main(subnet, username, new_password):
    hosts = scan_subnet(subnet)
    old_passwords = read_passwords(password_file)

    for host in hosts:
        print(f"Trying passwords for host: {host}")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        for old_password in old_passwords:
            try:
                client.connect(host, username=username, password=old_password)
                # Only show the first three characters of the password
                masked_password = old_password[:3] + '*' * (len(old_password) - 3)
                print(f"Successfully connected to {host} with password: {masked_password}")

                # Change password after successful connection
                if change_password(host, client):
                    # Log success to a file
                    with open('success_log.txt', 'a') as log_file:
                        log_file.write(f"Password changed for {host} to {new_password}\n")
                break  # Exit password loop after successful change
                
            except paramiko.AuthenticationException:
                masked_password = old_password[:3] + '*' * (len(old_password) - 3)
                print(f"Authentication failed for {host} with password: {masked_password}")
            except Exception as e:
                masked_password = old_password[:3] + '*' * (len(old_password) - 3)
                print(f"Failed to connect to {host} with password: {masked_password} - {e}")

        client.close()

if __name__ == '__main__':
    main(subnet, username, new_password)
