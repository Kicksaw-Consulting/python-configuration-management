import click

from pycm.core import PYCM
from pycm.secrets import (
    decrypt_value,
    encrypt_value,
    generate_fernet_key,
)
from pycm.utils import gather_user_input


@click.group(chain=True)
def pycm(**kwargs):
    pass


@pycm.command("upsert")
@click.option("-e", "--environment", default="development", help="Your environment")
def upsert(environment):
    pycm = PYCM(environment)
    data = pycm.yml_to_dict(skip_required_checks=True)
    key_name, key_value = gather_user_input()
    data[key_name] = {"value": key_value, "secret": True}
    pycm.dict_to_yml(data)


@pycm.command("reveal")
@click.option("-e", "--environment", default="development", help="Your environment")
def reveal(environment):
    pycm = PYCM(environment)
    config = pycm.yml_to_dict(skip_required_checks=True)

    for key, meta in config.items():
        # Skip non-secret values
        if type(meta) != dict:
            continue

        value = meta["value"]
        secret = decrypt_value(value)
        print(f"{key}={secret}")


@pycm.command("generate-key")
def generate_key():
    key = generate_fernet_key()

    print(f"Your key is: \n\n{key}\n")
    print(
        "Please store this in whichever .env-[environment] file you generated it for under the variable ENC_KEY"
    )


@pycm.command("reencrypt")
@click.option("-e", "--environment", default="development", help="Your environment")
@click.option(
    "-k",
    "--new-key",
    help="The new key with which you'd like to re-encrypt your secrets",
)
def reencrypt(environment, new_key):
    pycm = PYCM(environment)

    if not new_key:
        new_key = generate_fernet_key()

    data = pycm.yml_to_dict(skip_required_checks=True)

    for key, meta in data.items():
        # Skip non-secret values
        if type(meta) != dict:
            continue

        value = meta["value"]
        decrypted_value = decrypt_value(value)
        meta["value"] = encrypt_value(decrypted_value, enc_key=new_key)

        data[key] = meta

    pycm.dict_to_yml(data)

    print(f"Your new key is: \n\n{new_key}\n")
    print(
        f"config-{environment}.yaml has been re-encrypted. Please be sure to update your .env-{environment} with the new key you used!"
    )
