import os

from pycm.utils import (
    load_env,
    normalize_config_data,
)
from pycm.yml_utils import yml_to_dict


def get_config(environment: str, use_dotenv=False, use_secrets=True):
    if use_secrets:
        if use_dotenv:
            load_env(environment)
        else:
            assert os.getenv("ENC_KEY"), "ENC_KEY not present in environment variables"

    config = yml_to_dict(environment)
    normalized_config = normalize_config_data(config)

    return {**normalized_config}


def inject_config(
    environment: str, settings_module, use_dotenv=False, use_secrets=True
):
    config = get_config(environment, use_dotenv=use_dotenv, use_secrets=use_secrets)

    for key, value in config.items():
        setattr(settings_module, key, value)
