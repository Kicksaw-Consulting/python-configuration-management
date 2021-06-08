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
make a file called `.env-production` in the root of your django project. Inside of it, save the key generated
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

In the root of your django project, you can create a file called `config-required.json`.

The JSON object can be a list or a dictionary. This is useful for validating the presence of your
keys on start-up.

## Settings

There are two ways to use this library, if you don't mind a little magic, you can
simply inject the config by importing the following function in your django settings file,
and passing in the current module.

```python
# settings.py
from django_configuration_management import inject_config

# development is the environment name
inject_config("development", sys.modules[__name__])
```

See the example project for a demonstration of this.

If you want more verbosity, you can import the following function which will return
the config as a normalized dictionary that's flat and has all secrets decrypted.

```python
# settings.py
from django_configuration_management import get_config

# config = {"USERNAME": "helloworld", "PASSWORD": "im decrypted}
config = get_config("development")

USERNAME = config["USERNAME"]
# ...
```

### Using without a .env

If you want to skip using the .env, you can set the optional argument `dotenv_required` to `False`
when invoking either of the above two methods. Doing so means it then becomes your responsibility
to load an environment variable called `ENC_KEY` that stores the relevant encryption key for the
stage you're trying to load.

```python
# settings.py
from django_configuration_management import get_config

# Will error out if you didn't load ENC_KEY correctly
config = get_config("development", dotenv_required=False)
```

---

This project uses [poetry](https://python-poetry.org/) for dependency management
and packaging.
