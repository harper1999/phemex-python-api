# -*- coding=utf-8 -*-
# @Time: 2022/6/18 15:59
# @Author: Harper
# @File: query user order history.py
# @Software: PyCharm

import time
import pandas as pd
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_rows', None)  # 显示所有行

# Create a client
client_prod = Client(constant.Gateway.api)
client_testnet = Client(constant.Gateway.testnet)

try:
    r_tesenet = client_testnet.query_order_by_id({'symbol': constant.Symbol.BTCUSD,
                                                  'orderID': '8b9bd24b-7fd3-4134-94b0-1dd61a507cf6',
                                                  'clOrdID': 'JackTest11653527655.0854807'})
    print(r_tesenet)
    print('_' * 100)
    r_prod = client_prod.query_order_by_id({'symbol': constant.Symbol.DOGEUSD,
                                            'orderID': '43daeac3-5216-47d7-80cf-63f00a2cd5d0',
                                            'clOrdID': 'de9d9721-3a73-a426-d1e4-66345e1cdbed'})
    print(r_prod)

except PhemexAPIException as e:
    print(e)
