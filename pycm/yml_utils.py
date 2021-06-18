import yaml

from logging import getLogger
from pathlib import Path

from pycm.root import PYCM_ROOT
from pycm.validation_utils import (
    read_required_vars_file,
)

logger = getLogger(__name__)


def _validate_yml(data, skip_required_checks=False):
    if not skip_required_checks:
        _check_required_keys(data)

    for key, meta in data.items():
        if type(meta) == dict:
            secret = meta.get("secret")
            if secret is not None:
                assert (
                    secret
                ), f"{key} is structured like a secret value, but you've marked it as 'secret: false'. The value of this key can simply be the plain text value."
                assert (
                    type(meta.get("value")) == str
                ), f"{key} has an invalid row. Missing 'value'"
            else:
                raise AssertionError(f"{key} has an invalid row. Missing 'secret_name'")


def _check_required_keys(data):
    required_vars = read_required_vars_file()
    if not required_vars:
        return

    missing_keys = []
    for key in required_vars:
        if key not in data:
            missing_keys.append(key)

    assert (
        len(missing_keys) < 1
    ), f"The following keys are required. {missing_keys}. Halting"


def yml_to_dict(environment: str, skip_required_checks=False):
    config_file = ""

    yaml_file = Path(PYCM_ROOT) / f"config-{environment}.yaml"
    yml_file = Path(PYCM_ROOT) / f"config-{environment}.yml"

    if yaml_file.exists():
        config_file = yaml_file
    elif yml_file.exists():
        config_file = yml_file

    if not config_file:
        logger.warning(f"No file found for config-{environment}.yml|yaml")

    try:
        with open(config_file, "r") as yml:
            config: dict = yaml.safe_load(yml)
    except FileNotFoundError:
        config = {}

    _validate_yml(config, skip_required_checks)
    return config


def dict_to_yml(data: dict, environment: str) -> str:
    with open(f"config-{environment}.yaml", "w+") as yml:
        dumped = yaml.dump(data, yml)
    return dumped
