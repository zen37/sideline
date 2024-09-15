from feed import *
from config import get_config


if __name__ == "__main__":
    config = get_config('config.yaml')
    #print(config)
    process_feeds(config)
