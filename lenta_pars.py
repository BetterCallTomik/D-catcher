import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from urllib.parse import unquote
import random
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

def get_html(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url=url)
        time.sleep(3)

        element = driver.find_element_by_class_name("brands-block")
        with open('brand_blocks.txt', 'w') as f:
                f.write(f"{element}\n")

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_links(file_path):
    with open(file_path) as file:
        f = file.read()

    soup = BeautifulSoup(f, 'lxml')
    elements = soup.find_all('div', class_ = "brands-block__item")

    urls = []
    for el in elements:
        el_url = el.find('a', class_ = 'brand-block__link')
        urls.append(el_url)

    with open('urls.txt', 'w') as file:
        for url in urls:
            file.write(f"{url}\n")

def view_elements(url):
    driver = webdriver.Chrome()
    with open('urls.txt', 'w') as u:
        for need_url in u:
            driver.get(need_url)
            elements = driver.find_elements_by_class_name('lui-sku-product-card')
            with open('result.txt', 'w'):
                for el in elements:
                    soup = BeautifulSoup(el, 'lxml')
                    s = soup.find('div', 'lui-priceTex')




def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    urls_count = len(urls_list)
    count = 1
    for url in urls_list:
        view_elements(url)

def main():
    pass

if __name__ == '__main__':
    main()