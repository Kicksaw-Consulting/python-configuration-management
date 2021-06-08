from python_configuration_management.yml_utils import yml_to_dict


def test_yml_to_dict():
    local = yml_to_dict("test")
    assert local == {
        "PASSWORD": {
            "secret": True,
            "value": "gAAAAABgPsL6dJtRSNdwf2lIV4xVZaBZl1ZTTA6TEriYouHt-IMh1fIxf18GPsqzxfaSyFNXiMMJ5xL2DwlQc8QdwPTOlhJGKQ==",
        },
        "USERNAME": "testusername",
    }
