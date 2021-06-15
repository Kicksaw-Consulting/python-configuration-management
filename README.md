# Quick start

This package features an opinionated, python configuration management system, focused on combining both secret
and non-secret keys in the same configuration file. The values for secret keys are encrypted and can
be committed to the repo, but since each key is separated on a line-by-line basis, merge conflicts
shouldn't cause much trouble.

## Install

`pip install python-configuration-management`

## cli

### Generate a key

In a terminal, enter:

```bash
pycm generate-key
```

Follow the instructions printed to the console. For example, if you're setting up a production configuration,
make a file called `.env-production` in the root of your project. Inside of it, save the key generated
above to a variable called `ENC_KEY`.

### Upsert a secret

To insert or update a secret, enter:

```bash
pycm upsert --environment <your environment>
```

And follow the prompts.

### Insert a non-secret

Simply open the .yml file for the generated stage (the naming scheme is `config-<environment>.yaml`),
and insert a row. It should look like this:

```yaml
USERNAME: whatsup1994 # non-secret
PASSWORD:
  secret: true
  value: gAAAAABf2_kxEgWXQzJ0SlRmDy6lbXe-d3dWD68W4aM26yiA0EO2_4pA5FhV96uMWCLwpt7N6Y32zXQq-gTJ3sREbh1GOvNh5Q==
```

### Manually editing the file

You can change the values of non-secrets by hand, as well as the keynames, but clearly you must
not change the value of secrets by hand, as they're encrypted. Changing the order of any of the
keys is perfectly fine.

### Print secrets to the console

To show the decrypted values of all the secrets in the console, enter:

```bash
pycm reveal --environment <your-environment>
```

### Re-encrypt a config file

To re-encrypt all secret values for a given environment's config file, pass

```bash
pycm reencrypt --environment <your-environment> --new-key <your-new-key>
```

If you do not provide a key, a new one will be generated for you.

## Extras

In the root of your project, you can create a file called `config-required.json`.

The JSON object can be a list or a dictionary. This is useful for validating the presence of your
keys on start-up.

# Using the config in your python code

There are two ways to use this library. You can either have a dotenv file with your `ENC_KEY`,
or you can place the `ENC_KEY` in your environment variables. If you use a dotenv, make sure
the file follows this naming scheme: `.env-[environment]`.

As for accessing the config, if you don't mind a little magic, you can use `inject_config`.

```python
# settings.py
from pycm import inject_config

# development is the environment name
inject_config("development", sys.modules[__name__], use_dotenv=True)
```

If you want more verbosity, you can import the following function which will return
the config as a normalized dictionary that's flat and has all secrets decrypted.

```python
# settings.py
from pycm import get_config

# config = {"USERNAME": "helloworld", "PASSWORD": "im decrypted}
config = get_config("development", use_dotenv=True)

USERNAME = config["USERNAME"]
# ...
```

---

This project uses [poetry](https://python-poetry.org/) for dependency management
and packaging.
