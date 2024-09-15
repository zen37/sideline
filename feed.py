import ssl
import certifi
import feedparser
import urllib.request

from email.utils import parsedate_tz, mktime_tz
from datetime import datetime, timezone


def get_feed(feed_url, author, retrieve_by, date=None, max_count=None, txt_writer=None, delimiter=","):
    # Create an SSL context using certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        # Use urllib to open the URL with the SSL context
        with urllib.request.urlopen(feed_url, context=ssl_context) as response:
            data = response.read()

        # Parse the downloaded feed data
        feed = feedparser.parse(data)
        entry_count = 0

        # Loop through feed entries (articles/items)
        for entry in feed.entries:

            rec = delimiter.join([
                entry.author, 
                entry.id,
                entry.title, 
                entry.published
            ])
            #print(rec)

            # Parse the published date from RFC 822 format
            entry_date_tuple = parsedate_tz(entry.published)
            if entry_date_tuple:
                entry_date = datetime.fromtimestamp(mktime_tz(entry_date_tuple)).date()
                if retrieve_by == 'date' and date and entry_date < date:
                    print(f"Skipping entry with date: {entry_date} (older than {date})")
                    continue
            if author in entry.author:
                # Prepare a single line entry with fields separated by the delimiter
                line = delimiter.join([
                    author, 
                    entry.link, 
                    entry.title, 
                    entry.summary, 
                    entry.published
                ]) + "\n"

                # Write the line to the text file
                txt_writer.write(line)

                # Increment the entry count
                entry_count += 1

            # Stop processing if max_count is reached
            if retrieve_by == 'count' and entry_count >= max_count:
                print(f"Reached {max_count} entries. Exiting...")
                break

    except Exception as e:
        print(f"Failed to fetch the feed from {feed_url}. Error: {e}")


def read_feed_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()

    return [(line.split(',', 1)[0].strip(), line.split(',', 1)[1].strip()) for line in urls if ',' in line]


def process_feeds(config):

    # Get the current UTC timestamp using timezone-aware datetime
    timestamp = datetime.now(timezone.utc).strftime('_%Y%m%d-%H%M%S')
    output = f"{config.file_output.rstrip('.txt')}{timestamp}.txt"

    # Open the file to write in plain text mode
    with open(output, mode='w', encoding='utf-8') as file:
        # Write a header manually if needed
        file.write("Author | Link | Title | Summary | Published\n")
        #file.write("-" * 80 + "\n")

        # Loop through the feed URLs and fetch the feed for each one
        for author, url in read_feed_urls(config.file_feeds):
            print(f"FEED {url} by {author}")
            get_feed(url, author, config.retrieve_by, date=config.date, max_count=config.count, txt_writer=file, delimiter=config.file_output_delimiter)
            print("=" * 40)
