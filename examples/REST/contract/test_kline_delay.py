# -*- coding=utf-8 -*-
# @Time: 2022/5/25 15:04
# @Author: Harper
# @File: test_kline_delay.py
# @Software: PyCharm


import time
import pandas as pd
import requests
import json
import logging
from phemex.exceptions import PhemexAPIException

# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
# pd.set_option('display.max_colwidth', 1000)
# pd.set_option('display.height', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

now = int(time.time())
r = json.loads(requests.get('https://api.phemex.com/public/products').content)
products = r['data']['products'][:100]
url = 'https://api.phemex.com/exchange/public/md/kline?'
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
logging.info(msg='start requesting')


def test_kline_delay():
    container = []
    for product in products:
        symbol = product['symbol']
        data = {'symbol': symbol, 'from': now - 60 * 30, 'to': now, 'resolution': 60}
        query_string = '&'.join(['{}={}'.format(k, v) for k, v in data.items()])
        res = requests.get(url + query_string)

        ratelimit_left = res.headers['X-RateLimit-Remaining']
        if int(ratelimit_left) <= 2:  # 每分钟限流100次
            logging.info(
                msg={'x-ratelimit-remaining': ratelimit_left, 'symbol': symbol, 'index': products.index(product)})
            quit()

        content = json.loads(res.content)
        if not content.get('data'):
            get_unsent_kline(ratelimit_left, symbol, content)
            continue

        kline = content.get('data').get('rows')
        if kline:
            delayed_kline = get_delayed_kline(kline, symbol, ratelimit_left)
            container.append(delayed_kline)
        else:
            get_unsent_kline(ratelimit_left, symbol, content)

    while None in container:
        container.remove(None)
    return container


def get_unsent_kline(ratelimit_left, symbol, content):
    logging.warning(msg={'x-ratelimit-remaining': ratelimit_left, symbol: content})


def get_delayed_kline(kline, symbol, ratelimit_left):
    delayed_kline = kline[-1]
    last_minute = delayed_kline[0]
    if now - last_minute <= 60 or now - last_minute >= 120:  # 时间差正常在60-120秒内
        delayed_kline.insert(2, symbol)
        last_minute = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(last_minute))
        logging.warning(msg={'x-ratelimit-remaining': ratelimit_left, symbol: f"k线延迟至 {last_minute}"})
        return delayed_kline
    else:
        logging.info(msg={'x-ratelimit-remaining': ratelimit_left, symbol: f'没有延迟k线'})


def diaplay_delayed_klines(delayed_klines):
    if delayed_klines:
        delayed_klines = pd.DataFrame(delayed_klines)  # 最后一分延迟k线  .T 转置数据结构
        delayed_klines.columns = ['timestamp', 'interval', 'symbol', 'last close', 'open', 'high', 'low', 'close',
                                  'volume', 'turnover', ]
        delayed_klines['timestamp'] = pd.to_datetime(delayed_klines['timestamp'], unit='s')  # 时间戳转换为UTC
        print(delayed_klines)
    else:
        logging.info(msg=f'无延迟k线')


if __name__ == '__main__':
    try:
        delayed_set = test_kline_delay()
        diaplay_delayed_klines(delayed_set)

    except PhemexAPIException as e:
        print(e)
