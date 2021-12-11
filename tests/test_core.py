import os

from pathlib import Path

from pycm import PYCM


def test_get_config():
    pycm = PYCM("test")
    assert pycm.config == {
        "PASSWORD": "123password",
        "USERNAME": "testusername",
    }


def test_get_secretless_config():
    pycm = PYCM("test", use_secrets=False)
    assert pycm.config == {
        "USERNAME": "testusername",
    }


def test_get_config_weird_root():
    pycm_root = Path(os.path.dirname(os.path.abspath(__file__)))
    pycm = PYCM("nested", use_secrets=False, pycm_root=pycm_root)
    assert pycm.config == {
        "PASSWORD": "idk",
        "USERNAME": "testusername",
    }