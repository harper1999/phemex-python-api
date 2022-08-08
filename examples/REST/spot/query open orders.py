# -*- coding=utf-8 -*-
# @Time: 2022/3/31 16:22
# @Author: Harper
# @File: query open orders.py
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

try:
    r = client.query_open_spot_orders(constant.Symbol.sBTCUSDT)
    if r['data']:
        open_orders = pd.DataFrame(r['data'])
        print(open_orders)
    else:
        print('已无挂单')

except PhemexAPIException as e:
    print(e)
