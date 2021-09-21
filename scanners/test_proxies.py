import os
import requests
import random
import pickle

from itertools import cycle
from requests_html import HTMLSession
from datetime import datetime


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

    if not dump_time or (now_time - date_time_obj).days > 1:

        json_url = 'http://api.best-proxies.ru/proxylist.json'
        query_params = {
            'key': '285caf35b1ca9047c4005046969fa583',
            'limit': 100,
            'type': 'http'
        }

        with HTMLSession() as session:
            response = session.get(json_url, params=query_params)

        proxy_list = response.json()

        with open('proxies.pickle', 'wb') as f:

            pickle.dump((dump_time, proxy_list), f)

    random_proxy = random.choice(proxy_list)

    proxies = {
        'http': f"http://{random_proxy['ip']}:{random_proxy['port']}"
    }

    return proxies


if __name__ == '__main__':
    data = get_random_proxy()


# proxies = {
#   "123.202.219.248:8080",
#   "103.104.122.199:3128",
#   "124.70.103.38:3128",
#   "222.129.44.73:1085",
#   "206.81.2.48:3128",
# }
#
# num = len(proxies)
#
# proxy_cycle = cycle(proxies)
#
# for i in range(num):
#     proxy = next(proxy_cycle)
#     print(proxy)
#     proxies = {
#       "http": proxy,
#     }
#     r = requests.get("https://coderoad.ru/", proxies=proxies)
#     print(proxies, '\n')
#     print(r.text)
#
# breakpoint()