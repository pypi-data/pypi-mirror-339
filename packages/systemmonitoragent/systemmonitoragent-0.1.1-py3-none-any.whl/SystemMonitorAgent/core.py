import subprocess
import hashlib
import requests
import os
import json
import time
import sys
import platform
import logging
from datetime import datetime

API_SERVER = "http://152.67.6.225:9088"

# Logger setup (default silent)
logger = logging.getLogger("SystemMonitorAgent")
_null_handler = logging.NullHandler()
logger.addHandler(_null_handler)

SECRETS_FILE = "secrets.json"

def setup_logger(log_level="NONE", log_file=None, log_to_file=False):
    global logger

    # Remove all handlers first
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Reset logger to default state
    logger.setLevel(logging.NOTSET)
    
    # Configure based on log_level
    if log_level == "NONE":
        # Disable all logging
        logger.setLevel(logging.CRITICAL + 1)  # Above all standard levels
        logger.addHandler(logging.NullHandler())
        return
    
    # Set the appropriate log level
    if log_level == "DEBUG" or log_level == "ALL":
        level = logging.DEBUG
    elif log_level == "INFO":
        level = logging.INFO
    elif log_level == "ERROR":
        level = logging.ERROR
    else:
        level = logging.WARNING
    
    # Set the logger's level
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    # Add appropriate handler(s)
    if log_to_file and log_file:
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)  # Important: set the handler's level too
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)  # Important: set the handler's level too
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Test logging at startup
    logger.debug("Logger initialized with level: " + log_level)


def get_hostname():
    return platform.node()

def get_linux_machine_id():
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except Exception as e:
        logger.error(f"Error fetching Linux machine ID: {e}")
        return None

def get_windows_machine_guid():
    try:
        import winreg
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, r"SOFTWARE\\Microsoft\\Cryptography")
        guid, _ = winreg.QueryValueEx(key, "MachineGuid")
        return guid
    except Exception as e:
        logger.error(f"Error fetching Windows machine GUID: {e}")
        return None

def get_macos_serial_number():
    try:
        result = subprocess.check_output(
            "ioreg -l | grep IOPlatformSerialNumber",
            shell=True
        )
        serial = result.decode().split('=')[-1].strip().strip('"')
        return serial
    except Exception as e:
        logger.error(f"Error fetching macOS serial number: {e}")
        return None

def generate_unique_serial_number():
    system = platform.system()
    hostname = get_hostname()

    unique_id = None
    if system == "Linux":
        unique_id = get_linux_machine_id()
    elif system == "Windows":
        unique_id = get_windows_machine_guid()
    elif system == "Darwin":
        unique_id = get_macos_serial_number()

    if unique_id:
        return hashlib.sha256(f"{hostname}-{unique_id}".encode()).hexdigest()
    else:
        logger.warning("Unique ID not found, using hostname fallback.")
        return hashlib.sha256(f"{hostname}".encode()).hexdigest()

def generate_device_name():
    return f"{get_hostname().capitalize()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def load_secrets(secrets_file):
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_secrets(secrets_file, data):
    with open(secrets_file, 'w') as file:
        json.dump(data, file, indent=4)

def register_device(api_url, token, device_name, unique_serial_number):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'device_name': device_name, 'unique_serial_number': unique_serial_number}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info("Device registered successfully.")
        elif response.status_code == 400 and "unique constraint" in response.text:
            logger.info("Device already registered.")
        else:
            logger.error(f"Failed to register device: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while registering the device: {e}")

def get_reporting_time(api_url, token, unique_serial_number, secrets, secrets_file):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'unique_serial_number': unique_serial_number}

    try:
        response = requests.get(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            reporting_time = response.json().get('reporting_time')
            if reporting_time:
                logger.info(f"Device reporting time: {reporting_time} seconds")
                secrets['reporting_time'] = reporting_time
                save_secrets(secrets_file, secrets)
                return reporting_time
            else:
                logger.warning("No reporting time found in the response.")
        else:
            logger.error(f"Failed to get reporting time: {response.status_code}, {response.text}")
            return 30
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while fetching reporting time: {e}")
        return 30

def send_heartbeat(api_url, token, unique_serial_number):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'unique_serial_number': unique_serial_number}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 201:
            logger.debug("Heartbeat sent successfully.")
        elif response.status_code == 404:
            logger.error("Device deleted. Stopping agent.")
            sys.exit(0)
        else:
            logger.error(f"Failed to send heartbeat: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending heartbeat: {e}")

def start_agent(api_token, secrets_dir=None, log_level="NONE", log_file=None, log_to_file=False):
    global SECRETS_FILE

    # Setup logger first
    setup_logger(log_level, log_file, log_to_file)

    # Setup secrets file
    if secrets_dir and secrets_dir != "None":
        if not os.path.exists(secrets_dir):
            os.makedirs(secrets_dir)
        SECRETS_FILE = os.path.join(secrets_dir, "secrets.json")
    else:
        SECRETS_FILE = "secrets.json"

    logger.debug(f"Secrets file path: {SECRETS_FILE}")

    secrets = load_secrets(SECRETS_FILE)

    if 'device_name' not in secrets or 'unique_serial_number' not in secrets:
        device_name = generate_device_name()
        unique_serial_number = generate_unique_serial_number()
        if not unique_serial_number:
            logger.error("Failed to generate unique serial number. Exiting.")
            sys.exit(1)
        secrets.update({
            'api_token': api_token,
            'device_name': device_name,
            'unique_serial_number': unique_serial_number
        })
        save_secrets(SECRETS_FILE, secrets)

    api_register_url = f"{API_SERVER}/api/add_device/"
    api_heartbeat_url = f"{API_SERVER}/api/device_heartbeat/"
    api_reporting_time_url = f"{API_SERVER}/api/get_device_reporting_time/"

    register_device(api_register_url, api_token, secrets['device_name'], secrets['unique_serial_number'])

    # Main loop with error handling
    while True:
        try:
            reporting_time = get_reporting_time(api_reporting_time_url, api_token, secrets['unique_serial_number'], secrets, SECRETS_FILE)
            send_heartbeat(api_heartbeat_url, api_token, secrets['unique_serial_number'])
            
            # Default to 30 seconds if reporting_time is None or invalid
            if not isinstance(reporting_time, (int, float)) or reporting_time <= 0:
                logger.warning("Invalid reporting time received, using default (30s)")
                reporting_time = 30
                
            time.sleep(reporting_time)
        except KeyboardInterrupt:
            logger.info("Agent stopped by user.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            # Sleep for a while before retrying
            time.sleep(30)