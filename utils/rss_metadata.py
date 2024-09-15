import ssl
import certifi
import feedparser
import urllib.request

from pprint import pprint

def print_metadata(feed_url):

    # Create an SSL context using certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        # Use urllib to open the URL with the SSL context
        with urllib.request.urlopen(feed_url, context=ssl_context) as response:
            data = response.read()
            #print(data)
        
        #return

        # Parse the downloaded feed data
        feed = feedparser.parse(data)
    
        pprint(feed.feed)
        print("-" * 80)
        
        if feed.entries:
            
            first_entry = feed.entries[0]
                
            # Print the fields (keys) of the first entry
            print("Fields in the first entry:")
            
            for field in first_entry.keys():
                    print(field)
            print("-" * 80)
            pprint(first_entry)

    except Exception as e:
        print(f"Failed to fetch the feed. Error: {e}")


#print_metadata("https://www.standard.co.uk/sport/football/rss")
print_metadata("https://www.nytimes.com/athletic/rss/author/liam-twomey/")