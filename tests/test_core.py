import os

from pathlib import Path

from pycm import get_config
from pycm.yml_utils import yml_to_dict


def test_yml_to_dict():
    config = yml_to_dict("test")
    assert config == {
        "PASSWORD": {
            "secret": True,
            "value": "gAAAAABhtLMzwTq2ruUfXw9o_J4UqpUZrMBXbnrvb0fcoVcb9Tt2wsqqqW5Cd7q2DufHSSfZ2GkyYJ2AI1IG34yrZ-HVyFXjyg==",
        },
        "USERNAME": "testusername",
    }


def test_get_config():
    config = get_config("test")
    assert config == {
        "PASSWORD": "123password",
        "USERNAME": "testusername",
    }


def test_get_secretless_config():
    config = get_config("test", use_secrets=False)
    assert config == {
        "USERNAME": "testusername",
    }


def test_get_config_weird_root():
    pycm_root = Path(os.path.dirname(os.path.abspath(__file__)))
    config = get_config("nested", use_secrets=False, pycm_root=pycm_root)
    assert config == {
        "PASSWORD": "idk",
        "USERNAME": "testusername",
    }