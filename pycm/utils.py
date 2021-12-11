from getpass import getpass

from pycm.secrets import encrypt_value


def gather_user_input():
    key_name = input("Enter key name: ")
    key_value = getpass("Enter key value: ")
    return key_name, encrypt_value(key_value)
