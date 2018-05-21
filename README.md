# Webscrapers

A collection of web scrapers built in python

## Louisiana Business Scraper

This webscraper uses Selenium and Chromedriver to automate a headless browser and BeautifulSoup to parse the html. It scrapes data from [here]("https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx") and outputs it to both a csv and excel file.

## Anime Star Scraper

This scraper uses requests, beautifulsoup, and pandas to scrape Anime Star's [ecommerce site](www.anime-star.com) to get some product info based on user input. Saves the list of categories to csv after first run to minimize unnecessary requests (site categories shouldn't change often).