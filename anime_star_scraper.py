'''This application scrapes products from www.anime-star.com'''

import random
import csv
import sys
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

def get_categories(base_url):
  '''Gets categories from csv file if present or scrapes the site for a list of categories
     Returns a list of tuples containing a category and a link to the category page'''
  categories_fname = 'categories.csv'
  categories = []
  try:
    f = open(categories_fname, 'r')
    with f:
      reader = csv.reader(f)
      for row in reader:
        categories.append((row[0], row[1]))
      return categories
  except IOError:
    print(f'Could not read file or file does not exist for: {categories_fname}')
    print(f'Getting categories from: {base_url}\n')

  response = get(base_url)
  homepage = BeautifulSoup(response.text, 'html.parser')

  categories_container = homepage.find('div', class_='cate_menu').ul
  categories_tags = categories_container.find_all('li')
  categories = [(category_tag.a.get('href'), category_tag.a.get('title')) for category_tag in categories_tags]

  with open(categories_fname, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for category in categories:
      writer.writerow(category)

  return categories

def get_num_pages(page):
  '''Scrapes the total number of pages for any category
     Returns the number of pages'''
  return int(page.find(class_='page_last').find_previous_sibling('li').a.get_text())

def scraper(base_url, categories=None, num_pages=1):
  '''Processes the actual scraping of the website based on the categories selected
     Returns a dataframe containing the product data'''
  if categories is None or len(categories) == 0:
    print("No categories to scrape. Exiting")
    sys.exit()
  
  url = base_url + categories[0][0]
  names = []
  prices = []
  links = []
  codes = []
  image_sources = []
  
  print(f'scraping: {categories[0][1]} from {url}')
  for i in range(num_pages):
    response = get(f"{url}/{i}.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    prod_containers = soup.find_all('div', class_="prod_box")
    prod_info = [prod.find('div', class_="prod_box_inner") for prod in prod_containers]
    prod_pics = [prod.find('a', class_="pic_box") for prod in prod_containers]

    num_products = len(prod_info)
    for i in range(num_products):
      names.append(prod_info[i].find(class_="prod_name").get_text())
      prices.append(prod_info[i].find(class_="price_data").get_text())
      links.append(prod_info[i].find(class_="prod_name").a.get('href'))
      codes.append(prod_info[i].find(class_="prod_price").find_next_sibling().get_text()[7:])
      image_sources.append(prod_pics[i].img.get('src'))

  sleep(random.uniform(0,2)) # Adds some randomisation to lower chances of being blocked

  products_df = pd.DataFrame({'name': names,
                              'price': prices,
                              'link': links,
                              'code': codes,
                              'image_source': image_sources})
  
  return products_df

def handle_category_input(all_categories):
  '''Determines the categories to scrape based on user input from a menu.
     Returns a list of tuples for each category selected.'''
  menu = '''Choose a category from the list below'''
  print(menu)
  display_categories(all_categories)
  
  user_categories = []
  while True:
    user_input = input('Enter category number (enter "d" when finished): ')
    if user_input == 'd':
      break
    elif int(user_input) <= len(all_categories):
      user_categories.append(all_categories[int(user_input) - 1])
      print(f'Adding {all_categories[int(user_input) - 1][1]} to list of categories')
    else:
      print(f'{user_input} is not in the list of categories')

  return user_categories
    

def display_categories(categories):
  '''Displays the categories for the user to select'''
  for i, category in enumerate(categories):
    print(f'{i + 1}. {category[1]}')

if __name__ == "__main__":
  categories = get_categories('http://www.anime-star.com')
  user_categories = handle_category_input(categories)
  print(user_categories)
  products = scraper('http://www.anime-star.com', user_categories, 1)
  print(products)
