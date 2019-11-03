from bs4 import BeautifulSoup
from queueing import add_to_queue

def scrape_finn(page_content):
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