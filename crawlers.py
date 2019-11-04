import requests
from collections import deque
from time import time, sleep
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from scrapers import scrape_finn
from queueing import read_from_queue, add_to_queue

scrapers = {
  'www.finn.no' : scrape_finn
}

# 10 seconds delay between fetching page from the same domain
DEFAULT_TIMEOUT = 10  


throttling_times = {}
urls = deque(['https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sub_category=1.86.92&q=elektron'])

def load_urls():
  """
  >>> list(load_urls())
  ['https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sub_category=1.86.92&q=elektron']
  """
  return urls


def get_throttling_time(url):
  """
  >>> throttling_times['url'] = 20
  >>> get_throttling_time("url")
  0
  >>> import time
  >>> throttling_times['url'] = time.time()
  >>> round(get_throttling_time("url"))
  10
  """
  timeout = DEFAULT_TIMEOUT - min([time() - throttling_times.get('url', 0) , DEFAULT_TIMEOUT])
  return timeout

def update_throttling_time(url):
  """
  >>> update_throttling_time('https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP')
  'www.finn.no'
  """
  domain = urlparse(url).netloc
  throttling_times[domain] = time()
  return domain

def get_page(url):
  sleep(get_throttling_time(url))
  page = requests.get(url)
  update_throttling_time(url)
  return page.content

def prepare_report(items):
  # should generate the report and send with email
  pass

def main():
  items = []
  
  while len(urls):
    url = read_from_queue(urls)
    page = get_page(url)
    domain = urlparse(url).netloc
    page_items = scrapers[domain](page)
    items = items + page_items

  prepare_report(items)

if __name__ == "__main__":
  main()
