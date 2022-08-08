# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:36
# @Author: Harper
# @File: query kline.py
# @Software: PyCharm

import time
import pandas as pd
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
# pd.set_option('display.max_colwidth', 1000)
# pd.set_option('display.height', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

# Create a client
client = Client(constant.Gateway.testnet)

# 查询K线数据  现货合约均可用
try:
    start_time = int(time.mktime(time.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))
    end_time = int(time.mktime(time.strptime('2022-05-02 08:20:33', '%Y-%m-%d %H:%M:%S')))
    now = int(time.time())
    # print(datetime.datetime.fromtimestamp(now))
    # kline = client.query_kline(constant.Symbol.BTCUSD, start_time, end_time, 60)
    r = client.query_kline(constant.Symbol.ZECUSD, now-1200, now, 60)  # 最新上一分的价格
    kline = r['data']['rows']

    if kline:
        kline = pd.DataFrame(kline)
        kline.columns = ['timestamp', 'interval', 'last close', 'open', 'high', 'low', 'close', 'volume',
                         'turnover']
        kline['timestamp'] = pd.to_datetime(kline['timestamp'], unit='s')  # 时间戳转换为UTC
        print(kline)  # close是第60秒价格  # open是第61秒价格
        # with open('kline.txt', 'w') as fp:
        #     fp.write(json.dumps(kline, indent=4))

    else:
        print(f'没有获取到K线数据')

except PhemexAPIException as e:
    print(e)
