import json
import os
import yaml

from logging import getLogger
from pathlib import Path

from dotenv import load_dotenv
from pycm.secrets import decrypt_value

logger = getLogger(__name__)


class PYCM:
    def __init__(
        self, environment: str, use_secrets: bool = True, pycm_root: Path = Path(".")
    ) -> None:
        self.environment = environment
        self.use_secrets = use_secrets
        self.pycm_root = pycm_root

        self.config = self._get_config()

    def _get_config(self):
        self._load_env()

        # If we're using secrets, we need an encryption key
        if self.use_secrets:
            assert os.getenv("ENC_KEY"), "ENC_KEY not present in environment variables"

        config = self.yml_to_dict()
        normalized_config = self.normalize_config_data(config, self.use_secrets)

        return {**normalized_config}

    def _load_env(self):
        """
        Attempts to load environment variables from a .env file, if it exists

        Exits silently if not
        """
        env_path = Path(self.pycm_root) / f".env-{self.environment}"
        if os.path.isfile(env_path):
            load_dotenv(dotenv_path=env_path, verbose=True)

    def yml_to_dict(self, skip_required_checks=False):
        config_file = ""

        yaml_file = self.pycm_root / f"config-{self.environment}.yaml"
        yml_file = self.pycm_root / f"config-{self.environment}.yml"

        if yaml_file.exists():
            config_file = yaml_file
        elif yml_file.exists():
            config_file = yml_file

        if not config_file:
            logger.warning(f"No file found for config-{self.environment}.yml|yaml")

        try:
            with open(config_file, "r") as yml:
                config: dict = yaml.safe_load(yml)
        except FileNotFoundError:
            config = {}

        self._validate_yml(config, skip_required_checks)
        return config

    def normalize_config_data(self, data: dict, use_secrets: bool):
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

    def dict_to_yml(self, data: dict) -> str:
        with open(f"config-{self.environment}.yaml", "w+") as yml:
            dumped = yaml.dump(data, yml)
        return dumped

    def _validate_yml(self, data, skip_required_checks=False):
        if not skip_required_checks:
            self._check_required_keys(data)

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
                    raise AssertionError(
                        f"{key} has an invalid row. Missing 'secret_name'"
                    )

    def _check_required_keys(self, data):
        required_vars = self._read_required_vars_file()
        if not required_vars:
            return

        missing_keys = []
        for key in required_vars:
            if key not in data:
                missing_keys.append(key)

        assert (
            len(missing_keys) < 1
        ), f"The following keys are required. {missing_keys}. Halting"

    def _read_required_vars_file(self):
        required_vars = Path(self.pycm_root) / "config-required.json"

        try:
            with open(required_vars, "r") as file:
                required_vars = json.load(file)
        except FileNotFoundError:
            return

        return required_vars

    def inject_config(
        self,
        settings_module,
    ):
        for key, value in self.config.items():
            setattr(settings_module, key, value)
