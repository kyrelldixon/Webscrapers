from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import random
from time import sleep

def get_categories(base_url):
  response = get(base_url)
  homepage = BeautifulSoup(response.text, 'html.parser')

  categories_container = homepage.find('div', class_='cate_menu').ul
  categories_tags = categories_container.find_all('li')
  categories = [(category_tag.a.get('href'), category_tag.a.get('title')) for category_tag in categories_tags]
  return categories

def get_num_pages(page):
  return int(page.find(class_='page_last').find_previous_sibling('li').a.get_text())

def get_scraper_data(url):
  """This function is meant to grab info for page number and category types"""
  response = get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  num_pages = get_num_pages(soup)
  
  return num_pages

def scraper(base_url, categories, num_pages=1):
  url = base_url + categories[0]
  names = []
  prices = []
  links = []
  codes = []
  image_sources = []
  
  for i in range(num_pages):
    response = get(f"{url}{i}.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    prod_containers = soup.find_all('div', class_="prod_box")
    prod_info = [prod.find('div', class_="prod_box_inner") for prod in prod_containers]
    prod_pics = [prod.find('a', class_="pic_box") for prod in prod_containers]

    # Would it be better to use a list comprehension here?
    num_products = len(prod_info)
    for i in range(num_products):
      names.append(prod_info[i].find(class_="prod_name").get_text())
      prices.append(prod_info[i].find(class_="price_data").get_text())
      links.append(prod_info[i].find(class_="prod_name").a.get('href'))
      codes.append(prod_info[i].find(class_="prod_price").find_next_sibling().get_text()[7:])
      image_sources.append(prod_pics[i].img.get('src'))

  sleep(random.uniform(0,2))

  products_df = pd.DataFrame({'name': names,
                              'price': prices,
                              'link': links,
                              'code': codes,
                              'image_source': image_sources})
  
  return products_df

if __name__ == "__main__":
  # products = scraper("http://www.anime-star.com/c/action-figures_0520/", 1)
  # print(len(products))
  categories = get_categories('http://www.anime-star.com/')
  print(len(categories))
