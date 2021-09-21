# -*- coding: utf8 -*-
import os
import random
import requests
import pandas as pd
import pickle
import requests

from concurrent.futures import ThreadPoolExecutor
from time import sleep
from datetime import datetime

from blog.models import Post, Author, Category, Product

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_headers import Headers
from slugify import slugify
from lxml import html


def get_random_proxy():

    now_time = datetime.now()

    if 'proxies.pickle' in os.listdir('.'):
        with open('proxies.pickle', 'rb') as f:
            proxies_dump = pickle.load(f)
            dump_time = proxies_dump[1][1]['last_check']
            proxy_list = proxies_dump[1]
            date_time_obj = datetime.strptime(dump_time, '%Y-%m-%d %H:%M:%S')

    else:
        dump_time = None

    if not dump_time or (now_time - date_time_obj).days > 2:
        print('Делаю запрос к серверу best-proxies')
        json_url = 'http://api.best-proxies.ru/proxylist.json'
        query_params = {
            'key': '285caf35b1ca9047c4005046969fa583',
            'limit': 0,
            'type': 'http'
        }

        with HTMLSession() as session:
            response = session.get(json_url, params=query_params)

        proxy_list = response.json()

        with open('proxies.pickle', 'wb') as f:

            pickle.dump((dump_time, proxy_list), f)

    random_proxy = random.choice(proxy_list)

    proxies = {
        'http': f"https://{random_proxy['ip']}:{random_proxy['port']}"
    }

    return proxies


def get_product_data(product_asin):

    product_url = f'https://www.amazon.com/dp/{product_asin}/'

    headers = Headers(headers=True).generate()

    proxy = get_random_proxy()

    print(f'Делаю запрос через прокси {proxy}')

    r = requests.get(product_url,
                         headers=headers, proxies=proxy)

    r.raise_for_status()

    is_none_check = bool(product_asin)

    if is_none_check:

        soup = BeautifulSoup(r.content, features='lxml')

        name = soup.find('h1', attrs={'id':'title'}).find_next('span', attrs={'id':'productTitle'})
        rating = soup.find('span', attrs={'class':'a-icon-alt'})
        users_rated = soup.find('span', attrs={'id':'acrCustomerReviewText'})
        tag = soup.find_all('a', attrs={'class':'a-link-normal a-color-tertiary'})

        if name is not None:
            name = name.text.strip()

        if rating is not None:
            rate = rating.text.split()[0]
        else:
            rate = '-1'

        if users_rated is not None:
            users_rate = users_rated.text.split()[0]
        else:
            users_rate = '0'

        update_fields_product = {
                'name': name,
                'rating': rate,
                'users_rated': users_rate,
                'status': '1',
            }

        one_product = Product.objects.filter(asin=product_asin).update(**update_fields_product)

    else:
        print('Empty ASIN')


def run():
    all_entries = Product.objects.all()
    for product in all_entries:
        print(f'Проверяю товар с ASIN={product.asin}')
        if product is not None:
            try:
                get_product_data(product_asin=product.asin)
            except requests.exceptions.HTTPError as err:
                print(err)
                continue


if __name__ == '__main__':
    run()
