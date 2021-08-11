import os
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv

from pycm.root import PYCM_ROOT
from pycm.secrets import decrypt_value, encrypt_value


def load_env(environment: str):
    """
    Attempts to load environment variables from a .env file, if it exists

    Exits silently if not
    """
    env_path = Path(PYCM_ROOT) / f".env-{environment}"
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path, verbose=True)


def gather_user_input():
    key_name = input("Enter key name: ")
    key_value = getpass("Enter key value: ")
    return key_name, encrypt_value(key_value)


def normalize_config_data(data: dict, use_secrets: bool):
    normalized = dict()
    for key, meta in data.items():
        if type(meta) == dict:
            if not use_secrets:
                continue
            value = meta["value"]
            normalized[key] = decrypt_value(value)
        else:
            normalized[key] = meta
    return normalized
