# Import necessary libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
# from fake_useragent import UserAgent
from random import random, randint
from faker import Faker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import datetime
import time
from pymongo import MongoClient
import logging

# Define the URL to scrape
href_addr = 'https://lenta.com/catalog/'

# Create a UserAgent object
ua = UserAgent()

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Create a WebDriver object
browser = webdriver.Chrome(options=chrome_options)

# Try to find and click on the element with the specified CSS selector
try:
    browser.find_element_by_css_selector(
        'body > div.scroll-lock > div.modals-container > div > div > div > div.store-notification.current-store__tooltip-content > div > div.store-notification__buttons > button.button.button--primary.button--small.store-notification__button.store-notification__button--submit').click()
    time.sleep(2)
    browser.find_element_by_css_selector(
        'body > div.scroll-lock > div.modals-container > div > div > div > div.store-notification.current-store__tooltip-content > div > div.store-notification__buttons > button.button.button--primary.button--small.store-notification__button.store-notification__button--submit').click()
except:
    pass

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.shop_prices
final_lenta = db.final_lenta

# Set up logging
logging.basicConfig(filename="lenta.log",
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

# Set up headers for requests
headers = {'User-Agent': str(ua.random)}

# Create a Faker object
faker = Faker()

# Generate random ports and IP addresses
ports = [randint(1001, 9999) for i in range(9000)]
ips_arr = [faker.ipv4() for i in range(3000)]

# Define a function to switch proxies
def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, proxies={"http": "http://" + str(ips_arr[randint(1, 3000)]) + ":" + str(
                ports[randint(0, 9000)])}, headers=headers, cookies={'one': str(ua.random)}, timeout=10)
            print(ip)
            break
        except Exception as err:
            print(err)
            logging.exception('Connection error!  {}'.format(err))
            continue
    return ip

# Define a function to click on elements
def clicker(href_addr):
    while True:
        try:
            last_height = browser.execute_script(
                "return window.scrollTo(0, 5000)")
            time.sleep(3)
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.button--primary'))).click()
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        except TimeoutException:
            break
    return browser.page_source

# Scrape the main page
main_page = switcher(href_addr)
main_soup = BeautifulSoup(main_page.content, "html.parser")
main_headings_bad = main_soup.find_all(class_="catalog-groups-page__grid")
main_headings = []
main_hrefs = []
first_level_category = {}
for i in main_headings_bad:
    for j in i.find_all(class_='group-card__title'):
        main_headings.append(j.text.strip())
    for k in i.find_all(class_='group-card'):
        main_hrefs.append("https://lenta.com" + k['href'])
first_level_category = dict(zip(main_headings, main_hrefs))

# Write the results to a file
f = open('res.txt', 'w')
dict_res = {}
for a, b in first_level_category.items():
    subcategory_main_name = []
    subcategory_main_name_bad = []
    subcategory_sub_name = []
    subcategory_sub_href = []
    sub = switcher(b)
    sub_soup = BeautifulSoup(sub.content, "html.parser")
    sub_headings_all = sub_soup.find_all(class_="catalog-page__main")
    for j in sub_headings_all:
        # Extract the main category names and subcategory names and links
        for k in j.find_all(class_="link--black"):
            subcategory_main_name.append(
                k.text.strip().replace('\n', '').replace('\r', ''))
        for l in j.find_all(class_="link--gray"):
            subcategory_sub_name.append(l.text.strip())
            subcategory_sub_href.append("https://lenta.com"+l['href'])
    # Create a dictionary with subcategory names as keys and their links as values
    dict_res[a] = dict(zip(subcategory_sub_name, subcategory_sub_href))
# Write the dictionary to the file
f.write(str(dict_res))

# Define a function to parse a single HTML page
def parsing_single_html(href_addr):
    result = {}
    soup = BeautifulSoup(clicker(href_addr), "html.parser")
    names = []
    rouble = []
    penny = []
    all_page = soup.find_all(class_='catalog-grid-container__grid')
    for i in all_page:
        for j in i.find_all(class_='sku-card-small__title'):
            names.append(j.text.strip().replace('.', ','))
        for k in i.find_all(class_='sku-price--primary'):
            for l in k.find_all(class_='sku-price__integer'):
                rouble.append(l.text.strip().replace('\xa0', ''))
            for m in k.find_all(class_="sku-price__fraction"):
                penny.append(m.text.strip())
    # Combine the rouble and penny lists to get the full price
    cost_str = [i+'.'+j for i, j in zip(rouble, penny)]
    cost_float = [float(i) for i in cost_str]
    # Check for duplicate names and append a number to the duplicates
    dict_checker_double_names = {}
    for i in range(len(names)):
        z = names[i]
        if z not in dict_checker_double_names:
            dict_checker_double_names[z] = 1
        else:
            names[i] += '_'+str(dict_checker_double_names[z])
            dict_checker_double_names[z]+=1
            logging.info(
                '--------------------------------------------------------------------------------------------------------')
            logging.error(
                'We have similar {} <<name={}>>!!!!!!!!!!!!!'.format(names[i], i))
    # Create a dictionary with product names as keys and their prices as values
    dict_main = dict(zip(names, cost_float))
    result = {**result, **dict_main}
    logging.info(
        '-------------------------------------------------------------------------------------------------------')
    logging.info('{:<11} #Goods:{:<11}'.format(
        str(href_addr), str(len(result))))
    return result

# Get the current date
date = datetime.datetime.now().strftime("%d-%m-%Y")
counter = 1
final_lenta = {}
# Loop through the dictionary of subcategories
for i, j in dict_res.items():
    final_a = {}
    for k, m in j.items():
        # Open the subcategory page
        browser.get(m)
        time.sleep(2)
        try:
            # Try to click on the element with the specified CSS selector
            browser.find_element_by_css_selector(
                'body > div.scroll-lock > div.modals-container > div > div > div > div.store-notification.current-store__tooltip-content > div > div.store-notification__buttons > button.button.button--primary.button--small.store-notification__button.store-notification__button--submit').click()
            time.sleep(2)
            browser.find_element_by_css_selector(
                'body > div.scroll-lock > div.modals-container > div > div > div > div.store-notification.current-store__tooltip-content > div > div.store-notification__buttons > button.button.button--primary.button--small.store-notification__button.store-notification__button--submit').click()
        except:
            pass
        # Scroll down and click on the button to load more products
        clicker(m)
        time.sleep(3)
        # Parse the page and add the results to the database
        final_a = {
            'link': m,
            'category_name': k,
            date: parsing_single_html(m)
        }
        counter += 1
        db.final_lenta.update_one({'category_name': k, 'link': m}, {
            '$set': {date: final_a[date]}}, upsert=True)

