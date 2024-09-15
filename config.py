import yaml

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Config:
    retrieve_by: str
    date: datetime.date = None
    count: int = None
    file_feeds: str = 'feed_urls.txt'
    file_urls: str = 'input/urls.txt'
    file_output: str = 'feed_data.txt'
    file_output_delimiter: str = ','


def get_config(file_path):
    # Load the configuration from the YAML file
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Get the values from the YAML file
    retrieve_by = config.get('retrieve_by', 'count')
    date_str = config.get('date', None)
    count = config.get('count', None)
    file_feeds = config.get('file_feeds', 'feed_urls.txt')
    file_urls = config.get('file_urls', 'input/urls.txt')
    file_output = config.get('file_output', 'feed_data.txt')
    file_output_delimiter = config.get('file_output_delimiter', ',')

    # Initialize date variable
    date = None

    # If the 'retrieve_by' is date and date_str is provided, parse the date
    if retrieve_by == 'date' and isinstance(date_str, str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Date format error: {date_str}. Expected format is YYYY-MM-DD.")
    elif retrieve_by == 'count' and count is not None:
        try:
            count = int(count)
        except ValueError:
            print(f"Count value error: {count}. It should be an integer.")

    # Return a Config object
    return Config(retrieve_by, date, count, file_feeds, file_urls, file_output, file_output_delimiter)
