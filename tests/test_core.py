from python_configuration_management import get_config
from python_configuration_management.yml_utils import yml_to_dict


def test_yml_to_dict():
    config = yml_to_dict("test")
    assert config == {
        "PASSWORD": {
            "secret": True,
            "value": "gAAAAABgPsL6dJtRSNdwf2lIV4xVZaBZl1ZTTA6TEriYouHt-IMh1fIxf18GPsqzxfaSyFNXiMMJ5xL2DwlQc8QdwPTOlhJGKQ==",
        },
        "USERNAME": "testusername",
    }


def test_get_config():
    config = get_config("test")
    assert config == {
        "PASSWORD": "123password",
        "USERNAME": "testusername",
    }
