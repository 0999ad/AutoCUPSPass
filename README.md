# AutoCUPSPass

## Overview

**AutoCUPSPass** is a Python tool designed for penetration testers to automate the process of changing the root password on systems running CUPS and accessible via SSH. The tool scans a given subnet, attempts to connect to systems using the provided SSH credentials, changes the root password, and then verifies if the password change was successful.

## Features

- Scans a subnet for open SSH ports (port 22).
- Connects to systems via SSH and changes the root password.
- Verifies that the new password is working by attempting to log back in.
- Logs success and failure for password changes and verification.

## Prerequisites

- Python 3.x
- nmap (network scanning tool)
- Libraries: `python-nmap`, `paramiko`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/AutoCUPSPass.git
   cd AutoCUPSPass
   ```

2. Install the required Python libraries:

   ```bash
   pip install python-nmap paramiko
   ```

3. Ensure that `nmap` is installed on your system:

   - **Debian/Ubuntu**: `sudo apt install nmap`
   - **CentOS/Fedora**: `sudo yum install nmap`
   - **MacOS**: `brew install nmap`

## Usage

To use the tool, run the Python script as follows:

```bash
python autocupspass.py
```

### Example:

1. Modify the subnet, username, and passwords in the script:

```python
subnet = "192.168.1.0/24"  # Example subnet, change this to your target subnet
username = "root"           # SSH user
old_password = "oldpassword"  # Known current password
new_password = "newpassword"  # New password you want to set
```

2. Run the script:

```bash
python autocupspass.py
```

The script will:
- Scan the subnet for open SSH ports.
- Try to log in to each detected system.
- Change the root password on each system.
- Verify the password change by logging in again.

## Error Handling

- The tool logs any connection failures or issues with password changes, ensuring that all accessible systems are processed.
- Systems that cannot be connected to or that fail to change the password are skipped but logged for later review.

## License

This project is licensed under the MIT License.
