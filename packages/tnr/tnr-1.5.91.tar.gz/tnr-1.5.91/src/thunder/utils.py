import os
from os.path import join
import requests
import platform
import getpass
import subprocess
import json
from typing import Tuple, Optional

from rich.console import Console
from rich.table import Table
from rich import box
import click
import time
import errno
import tempfile
import shutil
import sys
import hashlib
from packaging import version as version_parser
try:
    from importlib.metadata import version
except Exception as e:
    from importlib_metadata import version

from thunder.config import Config

BASEURL = "https://api.thundercompute.com:8443"
# For debug mode
if os.environ.get('API_DEBUG_MODE') == "1":
    BASEURL = 'http://localhost:8080'

PLATFORM = "unknown"
try:
    platform_str = platform.system().lower()
    if platform_str == "linux":
        PLATFORM = "linux"
    elif platform_str == "darwin":
        PLATFORM = "mac"
    elif platform_str == "windows":
        PLATFORM = "windows"
except Exception:
    pass

IS_WINDOWS = PLATFORM == "windows"

if IS_WINDOWS:
    import win32security
    import ntsecuritycon as con


session = requests.Session()


def setup_instance(token):
    basedir = join(os.path.expanduser("~"), ".thunder")
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    scriptfile = join(basedir, "setup.sh")
    script_contents_file = join(os.path.dirname(__file__), "tnr_setup.sh")
    with open(script_contents_file, "r", encoding="utf-8") as f:
        setup_sh = f.read()

    if not os.path.exists(scriptfile):
        with open(scriptfile, "w+", encoding="utf-8") as f:
            f.write(setup_sh)
        os.chmod(scriptfile, 0o555)

        # Only add this if it doesn't exist inside the bashrc already
        bashrc = join(os.path.expanduser("~"), ".bashrc")
        if f". {scriptfile}" not in bashrc:
            with open(bashrc, "a", encoding="utf-8") as f:
                f.write(f"\nexport TNR_API_TOKEN={token}")
                f.write(
                    f"\n# start tnr setup\n. {scriptfile}\n# end tnr setup\n")
    else:
        with open(scriptfile, "r", encoding="utf-8") as f:
            current_contents = f.read()

        if current_contents != setup_sh:
            os.chmod(scriptfile, 0o777)
            with open(scriptfile, "w+", encoding="utf-8") as f:
                f.write(setup_sh)
            os.chmod(scriptfile, 0o555)


def get_next_id(token):
    try:
        endpoint = f"{BASEURL}/next_id"
        response = session.get(
            endpoint, headers={"Authorization": f"Bearer {token}"}
        )
        return str(response.json()["id"]), None
    except Exception as e:
        return None, e


def remove_host_key(device_ip):
    try:
        subprocess.run(
            ['ssh-keygen', '-R', device_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        return False


def enable_default_tnr_activate():
    with open(os.path.expanduser("~/.bashrc"), "r") as f:
        if "tnr activate" not in f.read():
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("\ntnr activate\n")


def get_available_gpus():
    endpoint = f"{BASEURL}/hosts2"
    try:
        response = session.get(endpoint, timeout=10)
        if response.status_code != 200:
            return None

        return response.json()
    except Exception as e:
        return None


def save_token(filename, token):
    if os.path.isfile(filename):
        if platform.system() == "Windows":
            subprocess.run(
                ["icacls", rf"{filename}", "/grant", f"{getpass.getuser()}:R"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            os.chmod(filename, 0o600)

    with open(filename, "w") as f:
        f.write(token)

    if platform.system() == "Windows":
        subprocess.run(
            [
                "icacls",
                rf"{filename}",
                r"/inheritance:r",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["icacls", f"{filename}", "/grant:r", rf"{getpass.getuser()}:(R)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        os.chmod(filename, 0o400)


def delete_unused_keys():
    pass


def get_key_file(uuid):
    basedir = join(os.path.expanduser("~"), ".thunder")
    basedir = join(basedir, "keys")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    return join(basedir, f"id_rsa_{uuid}")


def get_instances(token, use_cache=True, update_ips=False):
    if use_cache and get_instances.cache is not None:
        return get_instances.cache

    endpoint = f"{BASEURL}/instances/list"
    if update_ips:
        endpoint += "?update_ips=true"
    try:
        response = session.get(
            endpoint, headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text, {}

        result = (True, None, response.json())
        if use_cache:
            get_instances.cache = result
        return result
    except Exception as e:
        return False, str(e), {}


get_instances.cache = None


def create_instance(token, cpu_cores, gpu_type, template, num_gpus, disk_size_gb):
    endpoint = f"{BASEURL}/instances/create"
    payload = {
        "cpu_cores": cpu_cores,
        "gpu_type": gpu_type,
        "template": template,
        "num_gpus": num_gpus,
        "disk_size_gb": disk_size_gb,
    }
    try:
        response = session.post(
            endpoint,
            headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM},
            json=payload,
            timeout=30
        )
        if response.status_code != 200:
            return False, response.text, None

        data = response.json()

        token_file = get_key_file(data["uuid"])
        save_token(token_file, data["key"])
        return True, None, data["identifier"]
    except Exception as e:
        return False, str(e), None


def delete_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/delete"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def start_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/up"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def stop_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/down"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM}, timeout=30
        )
        if response.status_code != 200:
            return False, response.text

        return True, None
    except Exception as e:
        return False, str(e)


def get_active_sessions(token):
    endpoint = f"{BASEURL}/active_sessions"
    try:
        response = session.get(
            endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM}, timeout=30
        )
        if response.status_code != 200:
            return None, []

        data = response.json()
        ip_address = data.get("ip", "N/A")
        sessions = data.get("sessions", [])
        return ip_address, sessions
    except Exception as e:
        return None, []


def add_key_to_instance(instance_id, token):
    endpoint = f"{BASEURL}/instances/{instance_id}/add_key"
    try:
        response = session.post(
            endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM}, timeout=30
        )
        if response.status_code != 200:
            return False, f"Failed to add key to instance {instance_id}: {response.text}"

        data = response.json()
        token_file = get_key_file(data["uuid"])
        save_token(token_file, data["key"])
        return True, None

    except Exception as e:
        return False, f"Error while adding key to instance {instance_id}: {str(e)}"


def get_ip(token):
    endpoint = f"{BASEURL}/current_ip"
    try:
        response = session.get(
            endpoint,
            headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM},
            timeout=30,
        )
        if response.status_code != 200:
            return False, response.text

        return True, response.text
    except Exception as e:
        return False, str(e)


# Updating ~/.ssh/config automatically
SSH_DIR = os.path.join(os.path.expanduser("~"), ".ssh")
SSH_CONFIG_PATH = os.path.join(SSH_DIR, "config")
SSH_CONFIG_PERMISSIONS = 0o600
SSH_DIR_PERMISSIONS = 0o700


def set_windows_permissions(path, is_dir=False):
    """Set appropriate Windows permissions for SSH files/directories."""
    if not IS_WINDOWS:
        return

    try:

        # Get the current user's SID
        username = os.environ.get('USERNAME')
        domain = os.environ.get('USERDOMAIN')
        user_sid, _, _ = win32security.LookupAccountName(domain, username)

        # Get current user and Administrators group
        admin_sid = win32security.ConvertStringSidToSid(
            "S-1-5-32-544")  # Administrators group
        system_sid = win32security.ConvertStringSidToSid(
            "S-1-5-18")  # SYSTEM account

        # Create a new DACL (Discretionary Access Control List)
        dacl = win32security.ACL()

        if is_dir:
            # For directories
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION, con.FILE_ALL_ACCESS, user_sid)
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION, con.FILE_ALL_ACCESS, system_sid)
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admin_sid)
        else:
            # For files - more restrictive
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION,
                                     con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE,
                                     user_sid)
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION,
                                     con.FILE_ALL_ACCESS,
                                     system_sid)
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION,
                                     con.FILE_ALL_ACCESS,
                                     admin_sid)

        # Get the file's security descriptor
        security_descriptor = win32security.GetFileSecurity(
            path, win32security.DACL_SECURITY_INFORMATION)

        # Set the new DACL
        security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(
            path,
            win32security.DACL_SECURITY_INFORMATION,
            security_descriptor)
    except ImportError:
        # If pywin32 is not available, fall back to basic file permissions
        if is_dir:
            os.chmod(path, 0o700)
        else:
            os.chmod(path, 0o600)
    except Exception as e:
        # Log error but don't fail - SSH might still work
        click.echo(click.style(
            f"Warning: Could not set Windows permissions: {str(e)}", fg="yellow"))


def ensure_ssh_dir():
    """Ensure SSH directory exists with correct permissions."""
    if not os.path.exists(SSH_DIR):
        os.makedirs(SSH_DIR)
        if IS_WINDOWS:
            set_windows_permissions(SSH_DIR, is_dir=True)
        else:
            os.chmod(SSH_DIR, SSH_DIR_PERMISSIONS)
    elif not IS_WINDOWS:
        # Only check/update permissions on non-Windows systems
        current_mode = os.stat(SSH_DIR).st_mode & 0o777
        if current_mode != SSH_DIR_PERMISSIONS:
            os.chmod(SSH_DIR, SSH_DIR_PERMISSIONS)


def read_ssh_config():
    """Read SSH config file with proper error handling and permissions."""
    try:
        ensure_ssh_dir()
        if not os.path.exists(SSH_CONFIG_PATH):
            return []

        # Check and fix file permissions on non-Windows systems
        if not IS_WINDOWS:
            current_mode = os.stat(SSH_CONFIG_PATH).st_mode & 0o777
            if current_mode != SSH_CONFIG_PERMISSIONS:
                os.chmod(SSH_CONFIG_PATH, SSH_CONFIG_PERMISSIONS)

        with open(SSH_CONFIG_PATH, "r", encoding="utf-8") as f:
            return f.readlines()
    except (IOError, OSError, UnicodeDecodeError) as e:
        return []


def clean_config_lines(lines):
    """Clean and normalize SSH config lines to ensure consistent formatting."""
    # Remove empty lines and normalize spacing
    cleaned = []
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("Host "):
            # Add single newline before Host entries
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
        cleaned.append(line)

    if cleaned:  # Ensure single newline at end of file
        cleaned.append("")
    return [line + "\n" for line in cleaned]


def write_ssh_config(lines):
    """Write SSH config with proper permissions and error handling."""
    try:
        ensure_ssh_dir()

        # Clean up the config lines
        lines = clean_config_lines(lines)

        # Write to temporary file first
        temp_path = os.path.join(SSH_DIR, "config.tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        # Set correct permissions
        if IS_WINDOWS:
            set_windows_permissions(temp_path, is_dir=False)
        else:
            os.chmod(temp_path, SSH_CONFIG_PERMISSIONS)

        # Atomic replace
        os.replace(temp_path, SSH_CONFIG_PATH)

        # Set permissions again after replace on Windows
        if IS_WINDOWS:
            set_windows_permissions(SSH_CONFIG_PATH, is_dir=False)

    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass
        raise


def add_instance_to_ssh_config(hostname, key_path, host_alias=None, port=None):
    """Add instance to SSH config with proper validation and formatting."""
    if not hostname or not key_path:
        raise ValueError("Hostname and key_path are required")

    config_lines = read_ssh_config()
    host_alias = host_alias or hostname

    # Remove any existing entry first
    config_lines = [line for line in config_lines if not (
        line.strip() == f"Host {host_alias}" or
        (line.startswith(" ") and any(prev.strip() == f"Host {host_alias}"
                                      for prev in config_lines[:config_lines.index(line)]))
    )]

    new_entry = [
        f"Host {host_alias}\n",
        f"    HostName {hostname}\n",
        f"    User ubuntu\n",
        f"    IdentityFile {key_path}\n",
        f"    IdentitiesOnly yes\n",
        f"    StrictHostKeyChecking no\n",
    ]

    if port:
        new_entry.append(f"    LocalForward {port} localhost:{port}\n")

    config_lines.extend(new_entry)
    write_ssh_config(config_lines)


def remove_instance_from_ssh_config(host_alias):
    """Remove instance from SSH config safely."""
    if not host_alias:
        return

    config_lines = read_ssh_config()
    new_lines = []
    skip_until_next_host = False

    for line in config_lines:
        if line.strip().startswith("Host "):
            skip_until_next_host = (line.strip() == f"Host {host_alias}")

        if not skip_until_next_host:
            new_lines.append(line)

    write_ssh_config(new_lines)


def get_ssh_config_entry(instance_name):
    """Get SSH config entry with proper validation and error handling."""
    if not instance_name:
        return False, None

    try:
        config_lines = read_ssh_config()
        entry_exists = False
        ip_address = None

        for i, line in enumerate(config_lines):
            if line.strip() == f"Host {instance_name}":
                entry_exists = True
                # Look ahead for HostName
                for next_line in config_lines[i+1:]:
                    if not next_line.startswith(" "):
                        break
                    if next_line.strip().startswith("HostName"):
                        ip_address = next_line.split()[1].strip()
                        break
                break

        return entry_exists, ip_address
    except Exception as e:
        return False, None


def update_ssh_config_ip(instance_name, new_ip_address, keyfile=None):
    """Update instance IP and optionally key file in SSH config atomically."""
    if not instance_name or not new_ip_address:
        return

    config_lines = read_ssh_config()
    new_lines = []
    in_target_host = False
    updated_ip = False
    has_strict_checking = False
    updated_key = False if keyfile else True  # If no keyfile, consider it updated

    for line in config_lines:
        stripped = line.strip()
        if stripped.startswith("Host "):
            if in_target_host:
                # Add any missing configurations before moving to next host
                if not has_strict_checking:
                    new_lines.append("    StrictHostKeyChecking no\n")
                if keyfile and not updated_key:
                    new_lines.append(f"    IdentityFile {keyfile}\n")
            in_target_host = (stripped == f"Host {instance_name}")
            has_strict_checking = False
            updated_key = False if keyfile else True
            new_lines.append(line)
            continue

        if in_target_host:
            if stripped.startswith("HostName") and not updated_ip:
                new_lines.append(f"    HostName {new_ip_address}\n")
                updated_ip = True
                continue
            if stripped.startswith("StrictHostKeyChecking"):
                has_strict_checking = True
            if keyfile and stripped.startswith("IdentityFile"):
                new_lines.append(f"    IdentityFile {keyfile}\n")
                updated_key = True
                continue

        new_lines.append(line)

    # Handle case where target host was last in file
    if in_target_host:
        if not has_strict_checking:
            new_lines.append("    StrictHostKeyChecking no\n")
        if keyfile and not updated_key:
            new_lines.append(f"    IdentityFile {keyfile}\n")

    if updated_ip:
        write_ssh_config(new_lines)


def validate_token(token):
    endpoint = f"https://api.thundercompute.com:8443/uid"
    response = session.get(
        endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM})

    if response.status_code == 200:
        return True, None
    elif response.status_code == 401:
        return False, "Invalid token, please update the TNR_API_TOKEN environment variable or login again"
    else:
        return False, "Failed to authenticate token, please use `tnr logout` and try again."
    

def check_client_binary_hash(hash):
    # Get new binary hash
    metadata_url = f"https://storage.googleapis.com/storage/v1/b/client-binary/o/client_linux_x86_64?alt=json"
    latest_metadata = requests.get(metadata_url).json().get("metadata")
    latest_binary_hash = latest_metadata.get("hash")

    if hash == latest_binary_hash:
        return True
    else:
        return False
    
def display_available_gpus():
    available_gpus = get_available_gpus()
    if available_gpus is not None:
        console = Console()
        available_gpus_table = Table(
            title="🌐 Available GPUs:",
            title_style="bold cyan",
            title_justify="left",
            box=box.ROUNDED,
        )
        available_gpus_table.add_column(
            "GPU Type",
            justify="center",
        )
        available_gpus_table.add_column(
            "Node Size",
            justify="center",
        )

        for gpu_type, count in available_gpus.items():
            available_gpus_table.add_row(
                gpu_type,
                ", ".join(map(str, count)),
            )
        console.print(available_gpus_table)


def get_instance_id(token):
    success, ip_address = get_ip(token)
    if not success:
        instance_id = None
    if Config().getX("instanceId") == -1:
        success, error, instances = get_instances(token)
        if not success:
            click.echo(
                click.style(
                    f"Failed to list Thunder Compute instances: {error}",
                    fg="red",
                    bold=True,
                )
            )
            return -1

        for instance_id, metadata in instances.items():
            if "ip" in metadata and metadata["ip"] == ip_address:
                break
        else:
            instance_id = None

        Config().set("instanceId", instance_id)
        Config().save()
    else:
        instance_id = Config().getX("instanceId")
    return str(instance_id) if instance_id is not None else instance_id


def get_uid(token):
    endpoint = f"{BASEURL}/uid"
    response = requests.get(
        endpoint, headers={"Authorization": f"Bearer {token}", "Platform": PLATFORM})

    if response.status_code != 200:
        raise click.ClickException(
            "Failed to get info about user, is the API token correct?"
        )
    return response.text


def modify_instance(instance_id: str, payload: dict, token: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Modify a stopped Thunder Compute instance's properties.
    """
    try:
        response = requests.post(
            f"{BASEURL}/instances/{instance_id}/modify",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        )

        if response.status_code == 200:
            return True, None, str(response.json()["identifier"])
        elif response.status_code == 401:
            return False, "Authentication failed. Please run 'tnr login' to reauthenticate.", None
        elif response.status_code == 404:
            return False, f"Instance {instance_id} not found.", None
        elif response.status_code == 424:
            return False, response.text, None
        else:
            return False, f"Unexpected error (HTTP {response.status_code}): {response.text}", None

    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}", None

# === Template Information ===


TEMPLATE_INFO_CACHE_TTL = 3600  # 1 hour in seconds


def get_template_info_cache_file():
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "template_info.json")


def read_template_info_cache():
    cache_file = get_template_info_cache_file()
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                if cached.get('timestamp', 0) > time.time() - TEMPLATE_INFO_CACHE_TTL:
                    return cached.get('templates', {})
                else:
                    return None
    except Exception as e:
        return None
    
def delete_template_info_cache():
    cache_file = get_template_info_cache_file()
    if os.path.exists(cache_file):
        os.remove(cache_file)


def get_template_info(token=None):
    """Fetch template information from the API"""
    try:
        # Use production endpoint, fallback to localhost for development
        api_endpoint = f"{BASEURL}/thunder-templates"
        cache = read_template_info_cache()
        if cache:
            templates = cache
        else:
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(api_endpoint, headers=headers, timeout=5)
            if response.status_code == 200:
                templates = response.json()

            with open(get_template_info_cache_file(), 'w') as f:
                timestamp = time.time()
                json.dump({
                    'timestamp': timestamp,
                    'templates': templates
                }, f)

        # Extract template information
        template_info = []

        for template_name, template_data in templates.items():
            template_info.append({
                "name": template_name,
                "default": template_data.get("default", True),
                "displayName": template_data['displayName'],
                "defaultStorage": template_data.get('defaultSpecs', {}).get('storage', 100),
                "openPorts": template_data['openPorts'],
                "automountFolders": template_data['automountFolders'][0] if template_data['automountFolders'] else None
            })  

        return template_info
    except Exception as e:
        raise RuntimeError(f"Failed to fetch template information: {str(e)}")

def make_snapshot(token, snapshot_name, instance_name):
    """Create a snapshot from a stopped instance.
    
    Args:
        instance_id: The ID of the instance to create snapshot from
        snapshot_name: Name for the new snapshot
        token: API token for authentication
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.post(
            f"{BASEURL}/instances/snapshot",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": snapshot_name,
                "instance_name": instance_name
            }
        )
        
        if response.status_code == 202:
            return True, ''
        else:
            return False, f"Error creating snapshot: {response.text}"
            
    except Exception as e:
        return False, f"Error creating snapshot: {str(e)}"
    
def get_snapshots(token):
    """Get all snapshots for the current user."""
    response = requests.get(
        f"{BASEURL}/snapshots",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return True, '', response.json()
    else:
        return False, f"Error getting snapshots: {response.text}", None
    
def delete_snapshot(snapshot_id, token):
    """Delete a snapshot."""
    response = requests.delete(
        f"{BASEURL}/snapshots/{snapshot_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 204:
        return True
    else:
        return False

# === Update Checking Logic ===


PACKAGE_NAME = "tnr"
OPTIONAL_UPDATE_CACHE_TTL = 86400  # 24 hours in seconds


def get_optional_update_cache_file():
    """Gets the path for the optional update attempt cache file."""
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "optional_update_status.json")


def read_optional_update_cache():
    """Reads the timestamp of the last optional update attempt."""
    cache_file = get_optional_update_cache_file()
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                return cached.get('last_attempt_timestamp', 0)
    except Exception:
        pass  # Ignore errors, will just trigger a new attempt
    return 0  # Return 0 if no cache or error


def write_optional_update_cache():
    """Writes the current timestamp to the optional update cache."""
    cache_file = get_optional_update_cache_file()
    try:
        with open(cache_file, 'w') as f:
            json.dump({'last_attempt_timestamp': time.time()}, f)
    except Exception as e:
        click.echo(click.style(
            f"Warning: Could not write optional update cache: {e}", fg="yellow"))


def get_pip_version_cache_file():
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "version_requirements.json")


def get_binary_hash_cache_file():
    """Gets the path for the binary hash cache file."""
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "binary_hash.json")


def calculate_sha256(filepath):
    """Calculates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        click.echo(click.style(
            f"Warning: Could not calculate hash of {filepath}: {e}", fg="yellow"))
        return None


def check_binary_hash():
    """Checks if the running binary matches the latest hash from the GCS manifest."""
    CACHE_TTL = 3600  # 1 hour
    cache_file = get_binary_hash_cache_file()
    current_platform = platform.system().lower()
    # Use 'darwin' consistently for macOS
    if current_platform == 'darwin':
        current_platform = 'darwin'
    current_arch = platform.machine().lower()
    manifest_url = "https://storage.googleapis.com/thunder-cli-executable/signed-releases/manifest.json"

    # Map architectures
    if current_arch in ['amd64', 'x86_64']:
        arch = 'x64'
    elif current_arch in ['aarch64', 'arm64']:
        arch = 'arm64'
    else:
        click.echo(click.style(
            f"Warning: Unsupported architecture '{current_arch}' for binary check.", fg="yellow"))
        return True, None  # Assume up-to-date if arch is unknown

    # Check cache
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                # Invalidate cache if platform/arch changed or TTL expired
                if (cached.get('platform') == current_platform and
                        cached.get('arch') == arch and
                        time.time() - cached.get('timestamp', 0) < CACHE_TTL):

                    current_hash = calculate_sha256(sys.executable)
                    if not current_hash:
                        return True, None  # Assume OK if we can't hash current binary

                    expected_hash = cached.get('expected_hash')
                    if not expected_hash:
                        # If expected hash isn't in cache, proceed to fetch
                        pass
                    elif current_hash == expected_hash:
                        return True, None
                    else:
                        # Hash mismatch, but cache is valid - means binary is outdated
                        return False, ('hash', current_hash, expected_hash)
    except Exception as e:
        click.echo(click.style(
            f"Warning: Could not read binary hash cache: {e}", fg="yellow"))
        pass  # Continue to fetch from GCS

    # Fetch latest manifest from GCS
    try:
        response = requests.get(manifest_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        manifest_data = response.json()

        # Extract expected hash from manifest
        expected_hash = manifest_data.get(current_platform, {}).get(arch)

        if not expected_hash:
            click.echo(click.style(
                f"Warning: Could not find hash for {current_platform}/{arch} in manifest.", fg="yellow"))
            return True, None  # Assume OK if hash is missing in manifest

        current_hash = calculate_sha256(sys.executable)
        if not current_hash:
            return True, None  # Assume OK if we can't hash current binary

        # Cache the fetched hash
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'platform': current_platform,
                    'arch': arch,
                    'expected_hash': expected_hash
                }, f)
        except Exception as e:
            click.echo(click.style(
                f"Warning: Could not write binary hash cache: {e}", fg="yellow"))
            pass  # Proceed even if caching fails

        if current_hash == expected_hash:
            return True, None
        else:
            return False, ('hash', current_hash, expected_hash)

    except requests.exceptions.RequestException as e:
        click.echo(click.style(
            f"Warning: Failed to fetch manifest file: {e}", fg="yellow"))
        # Fallback to assuming it's okay if we can't check
        return True, None
    except json.JSONDecodeError as e:
        click.echo(click.style(
            f"Warning: Failed to parse manifest file: {e}", fg="yellow"))
        return True, None  # Assume OK if manifest is invalid
    except Exception as e:
        click.echo(click.style(
            f"Warning: An unexpected error occurred during binary hash check: {e}", fg="yellow"))
        return True, None


def check_meets_min_version():  # Renamed from check_pip_version
    """Checks if the installed pip package version meets the minimum requirement."""
    # This check is relevant even for binaries to determine if an update is *mandatory*
    CACHE_TTL = 3600  # 1 hour
    cache_file = get_pip_version_cache_file()  # Keep using the version cache file

    # Check cache first
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                # Check if cache contains necessary info and is still valid by TTL
                if ('timestamp' in cached and 'min_version' in cached and
                        time.time() - cached.get('timestamp', 0) < CACHE_TTL):

                    min_version = cached['min_version']
                    try:
                        # Try getting installed version. Might fail if not pip installed.
                        current_version = version(PACKAGE_NAME)
                        meets = version_parser.parse(
                            current_version) >= version_parser.parse(min_version)
                        details = ('version', current_version,
                                   min_version) if not meets else None
                        return meets, details
                    except Exception:
                        # If run as binary, can't get pip version. Assume minimum is met
                        # for the purpose of *this specific function*. The binary hash
                        # check handles whether the binary *itself* is up-to-date.
                        # If the API call below fails, we also default to True.
                        pass  # Fall through to API call if version check fails or not pip
    except Exception:
        pass  # Ignore cache errors, proceed to API call

    # Fetch minimum required version from API
    try:
        response = requests.get(f"{BASEURL}/min_version", timeout=10)
        response.raise_for_status()
        json_data = response.json()
        min_version = json_data.get("version")

        if not min_version:
            click.echo(click.style(
                "Warning: Could not retrieve minimum version from API.", fg="yellow"))
            return True, None  # Assume OK if API response is malformed

        # Cache the fetched minimum version
        try:
            with open(cache_file, 'w') as f:
                # We only cache the min_version and timestamp now
                json.dump({'timestamp': time.time(),
                          'min_version': min_version}, f)
        except Exception as e:
            click.echo(click.style(
                f"Warning: Could not write min version cache: {e}", fg="yellow"))

        # Now compare with installed version if possible
        try:
            current_version = version(PACKAGE_NAME)
            meets = version_parser.parse(
                current_version) >= version_parser.parse(min_version)
            details = ('version', current_version,
                       min_version) if not meets else None
            return meets, details
        except Exception:
            # If run as binary, assume minimum is met for this check.
            return True, None

    except requests.exceptions.RequestException as e:
        click.echo(click.style(
            f"Warning: Failed to fetch minimum required version: {e}", fg="yellow"))
        return True, None  # Assume OK if API fails
    except Exception as e:
        click.echo(click.style(
            f"Warning: Unexpected error during min version check: {e}", fg="yellow"))
        return True, None


def check_cli_up_to_date():
    """Checks if the running CLI meets minimum version and is the latest hash/version."""
    is_binary = getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS')

    meets_min, min_details = check_meets_min_version()

    is_latest = True  # Default to true
    latest_details = None

    if is_binary:
        is_latest, latest_details = check_binary_hash()
    else:
        # For pip installs, we currently only enforce minimum.
        # We could add a check against PyPI for the *absolute* latest if needed.
        is_latest = meets_min  # Consider latest if min is met for pip
        latest_details = min_details  # Use min_details if that's what failed

    # Prioritize showing min_details if minimum is not met
    final_details = min_details if not meets_min else latest_details

    # Return: (Does it meet minimum?, Is it the latest known version/hash?, Details for message)
    return meets_min, is_latest, final_details


def attempt_binary_self_update(expected_hash):
    """Attempts to download and replace the current binary.
    On Unix, replaces in-place and triggers restart, prompting for sudo if needed.
    On Windows, uses a detached batch script to replace after exit.
    """
    current_platform = platform.system().lower()
    # Use 'darwin' consistently for macOS
    if current_platform == 'darwin':
        current_platform = 'darwin'
    current_arch = platform.machine().lower()
    current_exe_path = sys.executable
    current_pid = str(os.getpid())

    # Map architectures
    if current_arch in ['amd64', 'x86_64']:
        arch = 'x64'
    elif current_arch in ['aarch64', 'arm64']:
        arch = 'arm64'
    else:
        click.echo(click.style(
            f"Cannot auto-update: Unsupported architecture '{current_arch}'", fg="red"))
        return False

    binary_name = "tnr.exe" if current_platform == "windows" else "tnr"
    download_url = f"https://storage.googleapis.com/thunder-cli-executable/signed-releases/{current_platform}/{arch}/{binary_name}"
    new_exe_temp_file = None

    try:
        # Download to a temporary file
        with requests.get(download_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=f"_{binary_name}") as f:
                new_exe_temp_file = f.name
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Verify hash
        downloaded_hash = calculate_sha256(new_exe_temp_file)
        if downloaded_hash != expected_hash:
            click.echo(click.style(  # Keep error message
                f"Error: Hash mismatch! Expected {expected_hash[:12]}..., got {downloaded_hash[:12]}...",
                fg="red"
            ))
            return False

        # --- Platform-Specific Update Logic ---
        if current_platform == "windows":
            # Generate a simple batch script: Sleep -> Replace
            updater_bat_content = f"""@echo off
setlocal
set OLD_EXE=%~1
set NEW_EXE=%~2

rem Wait 3 seconds for the main process to exit and release locks
timeout /t 3 /nobreak > NUL

rem Try to delete the old executable (might fail if still locked briefly)
del "%OLD_EXE%" > NUL 2>&1
rem Wait 1 second more
timeout /t 1 /nobreak > NUL

rem Force move the new executable over the old one
move /Y "%NEW_EXE%" "%OLD_EXE%"
if errorlevel 1 (
    rem Update failed. Clean up downloaded file.
    del "%NEW_EXE%" > NUL 2>&1
    rem Clean up this batch file
    (goto) 2>nul & del "%~f0"
    exit /b 1
)

rem Update likely succeeded. Clean up this batch file.
(goto) 2>nul & del "%~f0"

endlocal
exit /b 0
"""
            updater_bat_path = os.path.join(tempfile.gettempdir(
                # Still use PID for unique name
            ), f"tnr_updater_{current_pid}.bat")
            with open(updater_bat_path, "w") as bf:
                bf.write(updater_bat_content)

            creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW

            try:
                # Pass only OLD_EXE and NEW_EXE to the simplified script
                subprocess.Popen(
                    [updater_bat_path, current_exe_path, new_exe_temp_file],
                    creationflags=creation_flags, close_fds=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            except Exception as e:
                click.echo(click.style(
                    f"Error launching background updater: {e}", fg="red"))
                # Clean up temporary file if Popen failed
                if new_exe_temp_file and os.path.exists(new_exe_temp_file):
                    try:
                        os.remove(new_exe_temp_file)
                    except Exception:
                        pass
                return False

            # Let the batch script handle the downloaded file
            new_exe_temp_file = None
            return 'pending_restart'  # Indicate background update initiated

        else:  # Unix-like (Linux/macOS)
            os.chmod(new_exe_temp_file, 0o755)
            old_exe_path = current_exe_path + ".old"
            direct_replace_failed_permission = False

            try:  # Attempt direct replacement
                os.rename(current_exe_path, old_exe_path)
                try:
                    shutil.move(new_exe_temp_file, current_exe_path)
                    new_exe_temp_file = None  # Prevent deletion
                    try:
                        os.remove(old_exe_path)
                    except OSError:
                        pass
                    return True  # Success!
                except OSError as move_err:
                    # Try to restore the old binary if move failed
                    try:
                        os.rename(old_exe_path, current_exe_path)
                    except OSError:
                        pass
                    # Check if it was a permission error
                    if move_err.errno in [errno.EACCES, errno.EPERM]:
                        direct_replace_failed_permission = True
                    else:
                        raise move_err  # Re-raise if not permission error
            except OSError as rename_err:
                # Check if it was a permission error
                if rename_err.errno in [errno.EACCES, errno.EPERM]:
                    direct_replace_failed_permission = True
                else:
                    raise rename_err  # Re-raise if not permission error
            except Exception as e:
                return False  # Fail if it wasn't specifically a permission issue

            if direct_replace_failed_permission:
                if click.confirm(click.style("Update requires admin privileges. Retry using sudo?", fg="yellow"), default=False):
                    # Ensure temp file still exists before trying sudo
                    if not new_exe_temp_file or not os.path.exists(new_exe_temp_file):
                        click.echo(click.style(
                            "Error: Temporary update file missing. Cannot retry with sudo.", fg="red"))
                        return False

                    sudo_cmd_str = (
                        f"mv \"{current_exe_path}\" \"{old_exe_path}\" && "
                        f"mv \"{new_exe_temp_file}\" \"{current_exe_path}\" && "
                        f"chmod 755 \"{current_exe_path}\" && "
                        f"rm -f \"{old_exe_path}\""
                    )
                    sudo_cmd = ["sudo", "sh", "-c", sudo_cmd_str]
                    try:
                        # Use run instead of Popen to wait for completion
                        result = subprocess.run(
                            sudo_cmd, check=True, capture_output=True, text=True)
                        click.echo(result.stdout)  # Show sudo output
                        new_exe_temp_file = None  # Sudo command handled the move/cleanup
                        return True  # Sudo success!
                    except subprocess.CalledProcessError as sudo_err:
                        click.echo(click.style(
                            f"Sudo command failed (Exit Code {sudo_err.returncode}):", fg="red"))
                        if sudo_err.stderr:
                            click.echo(sudo_err.stderr)
                        if sudo_err.stdout:
                            # Show output even on error
                            click.echo(sudo_err.stdout)
                        # Attempt to restore original if possible
                        if os.path.exists(old_exe_path) and not os.path.exists(current_exe_path):
                            try:
                                # Use sudo to restore too
                                os.system(
                                    f"sudo mv \"{old_exe_path}\" \"{current_exe_path}\"")
                            except:
                                pass
                        return False  # Sudo failed
                    except FileNotFoundError:  # Handle case where sudo is not installed
                        click.echo(click.style(
                            "Error: 'sudo' command not found. Cannot elevate privileges.", fg="red"))
                        return False
                    except Exception as sudo_exec_err:
                        click.echo(click.style(
                            f"Failed to execute sudo command: {sudo_exec_err}", fg="red"))
                        return False  # Sudo failed
                else:
                    click.echo("Permission denied and sudo declined.")
                    return False  # Permission denied, sudo declined
            else:
                # If direct replace failed for a reason other than permissions
                return False

    except requests.exceptions.RequestException as e:
        click.echo(click.style(
            f"Error: Failed to download update: {e}", fg="red"))
        return False
    except Exception as e:
        return False
    finally:
        # Clean up temporary downloaded file ONLY if it wasn't successfully handled
        # or passed off to the Windows updater script.
        if new_exe_temp_file and os.path.exists(new_exe_temp_file):
            try:
                os.remove(new_exe_temp_file)
            except OSError as e:
                click.echo(click.style(
                    f"Warning: Failed cleanup {new_exe_temp_file}: {e}", fg="yellow"))
