from pprint import pprint

from pycm import get_config

config = get_config("test", use_dotenv=True)

pprint(config)
