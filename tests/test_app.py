from python_configuration_management import get_config


def test_get_config():
    local = get_config("test")
    assert local == {
        "PASSWORD": "123password",
        "USERNAME": "testusername",
    }
