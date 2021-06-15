import os
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv


from pycm.secrets import decrypt_value, encrypt_value


def load_env(environment: str):
    env_path = Path(".") / f".env-{environment}"
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path, verbose=True)
        return

    raise AssertionError(
        f"env not found: {env_path}. This file is required and must contain your ENC_KEY"
    )


def gather_user_input():
    key_name = input("Enter key name: ")
    key_value = getpass("Enter key value: ")
    return key_name, encrypt_value(key_value)


def normalize_config_data(data: dict):
    normalized = dict()
    for key, meta in data.items():
        if type(meta) == dict:
            value = meta["value"]
            normalized[key] = decrypt_value(value)
        else:
            normalized[key] = meta
    return normalized
