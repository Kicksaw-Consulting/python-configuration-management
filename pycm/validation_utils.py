import json

from pathlib import Path

from pycm.root import PYCM_ROOT


def read_required_vars_file():
    required_vars = Path(PYCM_ROOT) / "config-required.json"

    try:
        with open(required_vars, "r") as file:
            required_vars = json.load(file)
    except FileNotFoundError:
        return

    return required_vars
