import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import logging
import datetime
from pymongo import MongoClient
import pprint
href_addr = 'https://www.metro-cc.ru/assortiment/catalog'

client = MongoClient('localhost', 27017)
db = client["D-cather"]

logging.basicConfig(filename="metro.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='w', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.ERROR)
ua = UserAgent()
headers = {'User-Agent': str(ua.random)}


def switcher(href_addr):
    while True:
        try:
            ip = requests.get(href_addr, headers=headers, timeout=10).content
            break
        except Exception as errors:
            # print(errors)
            logging.info('{}'.format(errors))
            continue
    return ip


main_page = switcher(href_addr)
file = open("res.txt", "w")
file.write(str(main_page))
main_page_soup = BeautifulSoup(main_page, 'html.parser')
# print(main_page_soup)
page_categories_names_blocks = main_page_soup.find_all("div", class_="h4 field-title")
page_categories_links_blocks = main_page_soup.find_all("a", class_="btn-link")
page_categories_links = []
page_categories_names = []
for name in page_categories_names_blocks:
    page_categories_names.append(name.get_text())
for link in page_categories_links_blocks:
    page_categories_links.append(link['href'])

rez = dict(zip(page_categories_names, page_categories_links))
# pprint.pprint(rez)



prices = []
names = []

def check_page(href_addr):
    page = switcher(href_addr)
    page_soup = BeautifulSoup(page, "html.parser")
    array = page_soup.find_all("p", class_="error-page__illustration-text")
    if len(array) == 0:
        return True
    return False

def parse_final_page(href_addr):
    # print(href_addr)
    page = switcher(href_addr)
    page_soup = BeautifulSoup(page, "html.parser")
    # print(page_soup)
    goods_blocks = page_soup.find_all("div", class_="product-card__content")
    # print(goods_blocks)
    for block in goods_blocks:
        name = block.find_all("span", class_="product-card-name__text")[0]
        n = name.text
        n = n.replace("\n", "")
        if str(n) == "Раскупили":
            continue
        price_arr = block.find_all("span", class_="product-price__sum-rubles")
        if len(price_arr) == 0:
            continue
        price = price_arr[0]
        p = price.text
        names.append(n)
        prices.append(p)
        time.sleep(3)

def parse_metro(href_addr):
    category_page = switcher(href_addr)
    category_page_soup = BeautifulSoup(category_page, 'html.parser')
    # print(category_page_soup)
    page_subcategories_blocks = category_page_soup.find_all("a", class_="catalog-heading-link reset-link slider-main-block__heading-link style--catalog-1-level-products")
    # print(page_subcategories_blocks)
    for el in page_subcategories_blocks:
        parse_final_page("https://online.metro-cc.ru" + str(el['href']))
        i = 2
        while True:
            if not check_page("https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?page=" + str(i)):
                parse_final_page("https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?page=" + str(i))
            if check_page("https://online.metro-cc.ru/category/rybnye/ohlazhdennaya-ryba?page=" + str(i)):
                break
        time.sleep(3)

    # pprint.pprint(dict(zip(names, prices)))
    return dict(zip(names, prices))


date = datetime.datetime.now()
for category_name, category_href in rez.items():
    if category_name not in ["Овощи и фрукты", "Рыба и морепродукты", "Мясо, птица", "Мясная гастрономия", "Сыр, масло", "Безалкогольные напитки", "Чай, кофе, какао, цикорий", "Молоко, яйца", "Хлеб, выпечка, сладкое"]:
        continue
    rez = {
        "category_name": category_name,
        "market": "metro",
        "goods": parse_metro(category_href),
        "update_time": date
    }
    db.metro.insert_one(rez)
    prices.clear()
    names.clear()
    time.sleep(3)


# print(check_page("https://online.metro-cc.ru/category/chaj-kofe-kakao/chay?page=12"))

# f = open('res.txt', 'w')
# f.write(str(switcher('https://online.metro-cc.ru/category/chaj-kofe-kakao/chay?page=12')))




