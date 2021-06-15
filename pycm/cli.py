import click

from pycm.secrets import (
    decrypt_value,
    encrypt_value,
    generate_fernet_key,
)
from pycm.utils import gather_user_input, load_env
from pycm.yml_utils import dict_to_yml, yml_to_dict


@click.group(chain=True)
def pycm(**kwargs):
    pass


@pycm.command("upsert")
@click.option("-e", "--environment", default="development", help="Your environment")
def upsert(environment):
    load_env(environment)

    data = yml_to_dict(environment, skip_required_checks=True)
    key_name, key_value = gather_user_input()
    data[key_name] = {"value": key_value, "secret": True}

    dict_to_yml(data, environment)


@pycm.command("reveal")
@click.option("-e", "--environment", default="development", help="Your environment")
def reveal(environment):
    load_env(environment)
    config = yml_to_dict(environment, skip_required_checks=True)

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
    load_env(environment)

    if not new_key:
        new_key = generate_fernet_key()

    data, _ = yml_to_dict(environment, skip_required_checks=True)

    for key, meta in data.items():
        # Skip non-secret values
        if type(meta) != dict:
            continue

        value = meta["value"]
        decrypted_value = decrypt_value(value)
        meta["value"] = encrypt_value(decrypted_value, enc_key=new_key)

        data[key] = meta

    dict_to_yml(data, environment)

    print(f"Your new key is: \n\n{new_key}\n")
    print(
        f"config-{environment}.yaml has been re-encrypted. Please be sure to update your .env-{environment} with the new key you used!"
    )
