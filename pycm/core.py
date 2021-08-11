import os

from pycm.utils import (
    load_env,
    normalize_config_data,
)
from pycm.yml_utils import yml_to_dict


def get_config(environment: str, use_secrets=True):
    load_env(environment)

    # If we're using secrets, we need an encryption key
    if use_secrets:
        assert os.getenv("ENC_KEY"), "ENC_KEY not present in environment variables"

    config = yml_to_dict(environment)
    normalized_config = normalize_config_data(config, use_secrets)

    return {**normalized_config}


def inject_config(environment: str, settings_module, use_secrets=True):
    config = get_config(environment, use_secrets=use_secrets)

    for key, value in config.items():
        setattr(settings_module, key, value)
