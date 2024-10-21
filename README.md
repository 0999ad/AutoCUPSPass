# AutoCUPSPass

## Overview

**AutoCUPSPass** is a Python tool designed for penetration testers to automate the process of changing the root password on systems running CUPS that are accessible via SSH. The tool scans a given subnet, attempts to connect to systems using a list of possible old passwords, changes the root password, and verifies the success of the password change.

## Features

- Scans a subnet for systems with open SSH ports (port 22).
- Attempts to log in using old passwords from a file (`passwords.txt`).
- Changes the root password upon successful login.
- Verifies that the new password works by reconnecting to the system.
- Logs success and failure for each system.

## Prerequisites

To use this tool, you will need:

- Python 3.x
- `nmap` (network scanning tool)
- Required Python libraries: `python-nmap`, `paramiko`, `python-dotenv`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/AutoCUPSPass.git
   cd AutoCUPSPass
   ```

2. Install the required Python libraries:

   ```bash
   pip install python-nmap paramiko python-dotenv
   ```

3. Ensure that `nmap` is installed on your system:

   - **Debian/Ubuntu**: `sudo apt install nmap`
   - **CentOS/Fedora**: `sudo yum install nmap`
   - **MacOS**: `brew install nmap`

## Configuration

1. **Environment Variables**

   Create a `.env` file in the same directory as the script with the following content:

   ```env
   subnet="192.168.1.0/24"  # Subnet to scan
   username="root"          # SSH username (default is 'root')
   new_password="newpassword"  # New password to be set on the target systems
   ```

2. **Password File**

   Create a `passwords.txt` file in the same directory. This file should contain a list of possible old passwords (one per line) to try during the password change process. For example:

   ```text
   oldpassword1
   oldpassword2
   oldpassword3
   ```

## Usage

Once you have your `.env` file and `passwords.txt` ready, you can run the script:

```bash
python autocupspass.py
```

### Example:

- The script will:
  - Scan the specified subnet for open SSH ports (port 22).
  - Attempt to log in to each detected system using each password from `passwords.txt`.
  - Change the root password on successful login.
  - Verify the new password by reconnecting to the system.
  - Output logs indicating success or failure for each system.

## Error Handling

- If the script fails to connect to a system or change the password, it will log the error and move to the next system.
- Systems where the password change fails will not be verified.

## License

This project is licensed under the MIT License.
