from pprint import pprint

from python_configuration_management import get_config

config = get_config("test", use_dotenv=True)

pprint(config)
