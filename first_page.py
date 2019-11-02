import requests
from collections import deque
from time import time, sleep
from bs4 import BeautifulSoup

# 10 seconds delay between fetching page from the same domain
DEFAULT_TIMEOUT = 10  

urls = deque(['https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sub_category=1.86.92&q=elektron'])

throttling_times = {}

def load_urls():
  """
  >>> load_urls()
  deque(['https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sub_category=1.86.92&q=elektron'])
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

def update_throttling_times(url):
  throttling_times[domain_name] = time()

def get_page(url):
  sleep(get_throttling_time(url))
  page = requests.get(url)
  update_throttling_times(url)
  return page.content

def add_to_queue(urls, url):
  """
  >>> urls = deque([])
  >>> list(add_to_queue(urls, 'test'))
  ['test']
  """
  urls.append(url)
  return urls

def read_from_queue(urls):
  """
  >>> urls = deque(['test', 'dwa', 'trzey'])
  >>> read_from_queue(urls)
  'test'
  """
  return urls.popleft()

def scrape_page(page_content):
  soup = BeautifulSoup(page_content, 'html.parser')
  items = []
  
  next_page = soup.find("a", {'rel': 'next'}).attrs['href']
  add_to_queue(urls, next_page)

  for article in soup.find_all('article'):
      link = article.find("a", {'class': 'ads__unit__link'}).attrs['href']
      image = article.find("img").attrs['src']
      price = article.find("div", {'class': 'ads__unit__img__ratio__price'}).text.replace('\xa0', '').strip()
      title = article.find("h2", {'class': 'ads__unit__content__title'}).text.replace('\xa0', '').strip()
      city = article.find("span", {'class': 'ads__unit__content__details'}).find('span').find_next().text
      item = {
        'link': link, 
        'image' : image,
        'price' : price,
        'title' : title,
        'city' : city
      }
      items.append(item)
  return items

def prepare_report(items):
  # should generate the report and send with email
  pass


def main():
  items = []
  
  while len(urls):
    url = read_from_queue(urls)
    page = get_page(url)
    page_items = scrape_page(page)
    items = items + page_items

  prepare_report(items)

if __name__ == "__main__":
  main()