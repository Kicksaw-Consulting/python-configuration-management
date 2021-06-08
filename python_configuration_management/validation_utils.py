import json
import re

from pathlib import Path


def validate_key_name(key_name: str):
    assert re.search(
        "^[A-Z0-9]+(?:_[A-Z0-9]+)*$", key_name
    ), f"Invalid key name {key_name}. Keys must consist only of uppercase letters and underscore"


def read_required_vars_file():
    required_vars = Path(".") / "config-required.json"

    try:
        with open(required_vars, "r") as file:
            required_vars = json.load(file)
    except FileNotFoundError:
        return

    return required_vars
