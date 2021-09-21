# -*- coding: utf8 -*-
import os
import random

import requests
import pandas as pd
import pickle
import requests
import requests_html

from concurrent.futures import ThreadPoolExecutor
from time import sleep
from datetime import datetime

from blog.models import Post, Author, Category, Product

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_headers import Headers
from slugify import slugify
from lxml import html


no_pages = 2


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
            'key': '985e272c8c39f8a6b2533a601d495ac3',
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


def get_data(pageNo):

    headers = Headers(headers=True).generate()
    url = f'https://www.amazon.com/s?k=Power+Chain+Saws&i=lawngarden&rh=n%3A552918&' \
          f'page={pageNo}&_encoding=UTF8&c=ts&qid=1626431119&ts_id=552918&ref=sr_pg_{pageNo}'

    proxy = get_random_proxy()
    print(f'Делаю запрос через прокси {proxy}')
    r = requests.get(url, headers=headers, proxies=proxy)

    r.raise_for_status()
    clean_html = html.fromstring(r.content)

    all_top_asin = clean_html.xpath('//div/@data-asin')

    for each_asin in all_top_asin:
        is_empty = bool(each_asin)
        if is_empty:
            product = {
                'slug': slugify(each_asin),
                'asin': each_asin
            }

            Product.objects.get_or_create(**product)


def run():
    # Post.objects.all().delete()
    for i in range(1, no_pages + 1):
        sleep(2)
        try:
            get_data(i)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    run()
