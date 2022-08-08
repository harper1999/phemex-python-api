# -*- coding=utf-8 -*-
# @Time: 2022/3/30 14:31
# @Author: Harper
# @File: query trading fee history.py
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

client = Client(constant.Gateway.testnet)

try:
    r = client.query_trading_fee_history({'symbol': constant.Symbol.BTCUSD, 'offset': '0', 'limit': 50})
    trading_fee_history = r['data']['rows']
    if trading_fee_history:
        print(pd.DataFrame(trading_fee_history))

    else:
        print(f'没有任何记录')

except PhemexAPIException as e:
    print(e)

