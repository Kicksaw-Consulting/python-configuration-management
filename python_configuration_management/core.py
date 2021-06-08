import os
from typing import Callable

from python_configuration_management.utils import (
    load_env,
    normalize_config_data,
)
from python_configuration_management.yml_utils import yml_to_dict


def get_config(environment: str, dotenv_required=True):
    try:
        load_env(environment)
    except AssertionError as error:
        if dotenv_required:
            raise error

    local_secrets = yml_to_dict(environment)
    normalized_local_secrets = normalize_config_data(local_secrets)

    return {**normalized_local_secrets}


def inject_config(environment: str, settings_module, dotenv_required=True):
    config = get_config(environment, dotenv_required)

    for key, value in config.items():
        setattr(settings_module, key, value)
