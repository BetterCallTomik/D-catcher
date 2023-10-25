import requests
import lxml
import bs4
from collections import namedtuple
from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup

def get_categories_links(url):
    class_name = 'sc-clhTte dXujXr'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    elements = soup.find_all(class_=class_name)
    links = [tag.get('href') for tag in elements]

    print(response.content)
    print(links)

def get_blocks_in_category(url):
    class_name = 'sc-bQdRvg brgELu product-card'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    elements = soup.find_all(class_=class_name)

    return elements

class Item:
    def __init__(self, name=None, cost=None):
        self.name = name
        self.cost = cost

    def show(self):
        print('{', self.name, self.cost, '}')

def get_inf_about_items(elements):
    array = []
    for el in elements:
        name = el.find(class_='product-card__title')
        name_text = name.get_text()
        cost = el.find(class_='price_new')
        if cost is not None:
            cost_text = cost.get_text()
            cost_text = int(cost_text)
            i = Item(name_text, cost_text)
            array.append(i)

    for item in array:
        item.show()

    # return array

def main():
    url = "https://www.perekrestok.ru/cat/mc/113/moloko-syr-ajca"
    elements = get_blocks_in_category(url)
    get_inf_about_items(elements)

if __name__ == '__main__':
    main()