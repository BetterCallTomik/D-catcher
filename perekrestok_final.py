# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import itertools
from pymongo import MongoClient
import datetime
import re
import pprint
import logging
from itertools import cycle
import time
import lxml

client = MongoClient('192.168.149.192', 27017)
db = client.shop_prices
final_perekrestok = db.final_perekrestok

href_addr = 'https://www.perekrestok.ru/cat/'
user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36']


logging.basicConfig(filename="perekrestok_2.log",
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)

user_agent_list_pool = cycle(user_agent_list)


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, timeout=20).text
            break
        except Exception as errors:
            # print('Ошибка:\n', errors)
            logging.exception('Connection error!  {}'.format(errors))
            continue
    return ip


perekrestok_main_page = switcher(href_addr)
perekrestok_main_soup = BeautifulSoup(perekrestok_main_page, 'html.parser')
perekrestok_heading_1_catogories = perekrestok_main_soup.find_all(
    class_='sc-dQoVA fvoiIk')
arr = []
# print(perekrestok_heading_1_catogories)
for i in perekrestok_heading_1_catogories:
    j = i.text.strip().split('\n')
    arr.append(j)
arr_1 = []
for i in arr:
    for j in i:
        arr_1.append(j)
arr_name_submenu = []
arr_1 = [x for x in arr_1 if x]
names = arr_1
# print(names)
hrefs = []

links = []
for n in perekrestok_heading_1_catogories:
        hrefs.append(n['href'])
for i in hrefs:
    links.append('https://www.perekrestok.ru'+i)
# print(links)
result = dict(
    zip(names, links))
pprint.pprint(result)

logging.info('The length of array with categories_names 1 level is: ' +
             str(len(names)))
logging.info('The length of array with categories_href 1 level is: ' +
             str(len(links)))


logging.info('Category: {:<11}'.format(str(names)))

def parse_single_html(href_addr):
    names = []
    prices = []

    # Fetch HTML content from the URL
    page = switcher(href_addr)
    # Parse the HTML content
    # print(page)
    page_soup = BeautifulSoup(page, 'html.parser')
    print(page_soup)
    page_categories_swipers = page_soup.find_all("div",{'class': 'swiper-slide' 'swiper-slide-visible' 'swiper-slide-next' 'category__slide'})
    # page_categories = page_soup.find_all("a", class_="sc-dQoVA dsEnQi sc-jYCGPb")
    print(page_categories_swipers)
    for category in page_categories_swipers:
        print(category)
        new_page = switcher("https://www.perekrestok.ru" + category['href'])
        new_page_soup = BeautifulSoup(new_page, 'html.parser')
        names_blocks = new_page_soup.find_all(class_="product-card__link-text")
        price_blocks = new_page_soup.find_all(class_="price-new")
        for name in names_blocks:
            names.append(name.get_text())
        for price in price_blocks:
            s = price.get_text()[:-2]
            s = s.replace(',', '.')
            # print(s)
            prices.append(float(s))
        break
        time.sleep(2)
    # print(names)
    # print(prices)

    rez = dict(zip(names, prices))
    pprint.pprint(rez)

    return rez



# counter_1 = 1
# date = datetime.datetime.now().strftime("%d-%m-%Y")
#
# g = open('result_2_level.txt', 'w')
# counter_2 = 1
# dict_1 = {}
# for i, j in result.items():
#     arr_href_category_2_level_without_https = []
#     arr_href_category_2_level = []
#     arr_name_category_2_level = []
#     perekrestok_main_page_2_ = switcher(j)
#     perekrestok_main_soup_2_ = BeautifulSoup(
#         perekrestok_main_page_2_, 'html.parser')
#     perekrestok_heading_2_catogories = perekrestok_main_soup_2_.find_all(
#         class_='xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray')
#     for m in perekrestok_heading_2_catogories:
#         k = m.text.strip()
#         arr_name_category_2_level.append(k)
#     for n in perekrestok_heading_2_catogories:
#         arr_href_category_2_level_without_https.append(n.get('href'))
#     for k in arr_href_category_2_level_without_https:
#         h = 'https://www.perekrestok.ru'+k
#         arr_href_category_2_level.append(h)
#     dict_1[i] = dict(zip(arr_name_category_2_level, arr_href_category_2_level))
#
# f = open('resul.txt', 'w')
# final_perekrestok = {}
# for i, j in dict_1.items():
#     final_p = {}
#     for k, m in j.items():
#         final_p = {
#             'link': m,
#             'category_name': k,
#             date: parse_single_html(m)
#         }
#         logging.info('#Category_2_name:  {:<11} Counter_2_level: {:<11} #href_2_level:{:<11}'.format(
#             str(k), str(counter_2), str(m)))
#         logging.info('--------------------------------------------------------------------------------------------------------------------------------------------------')
#         counter_2 += 1
#         print(final_p)
#         db.final_perekrestok.update_one({'category_name': k, 'link': m}, {
#                                         '$set': {date: final_p[date]}}, upsert=True)
#         g.write(str(final_perekrestok))

for i, j in result.items():
    print(i)
    parse_single_html(j)
    break