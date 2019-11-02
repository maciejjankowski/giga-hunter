import requests
from bs4 import BeautifulSoup

url = 'https://www.finn.no/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sub_category=1.86.92&q=elektron'


def load_urls():
  return [url]


def get_page(url):
  page = requests.get(url)
  return page.content


def scrape_page(page_content):
  soup = BeautifulSoup(page_content, 'html.parser')
  items = []
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
  urls = load_urls()
  for url in urls:
    page = get_page(url)
    page_items = scrape_page(page)
  items = items + page_items
  prepare_report(items)

if __name__ == "__main__":
  main()