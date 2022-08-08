# -*- coding=utf-8 -*-
# @Time: 2022/4/4 13:30
# @Author: Harper
# @File: query order history.py
# @Software: PyCharm

import time
import pandas as pd
import phemex.constant as constant
from phemex.client import Client
from phemex.exceptions import PhemexAPIException

# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
# pd.set_option('display.max_colwidth', 1000)
# pd.set_option('display.height', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

client = Client(constant.Gateway.testnet)

try:
    start = int(time.mktime(time.strptime('2022-03-01 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    end = int(time.mktime(time.strptime('2022-04-11 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    now = int(time.time() * 1000)
    r = client.query_spot_order_history(
        {'symbol': constant.Symbol.sFEIUSDT, 'start': start, 'end': now, 'offset': 0, 'limit': 200})
    order_history = r['data']['rows']

    if order_history:
        order_history = pd.DataFrame(order_history)
        order_history['createTimeNs'] = pd.to_datetime(order_history['createTimeNs'], unit='ns')
        order_history.replace({'qtyType': {'ByBase': r'ByBase(BTC)'}}, inplace=True)
        # 通过指定条件替换元素  r 转义字符无效化
        filled_order_history = order_history.loc[order_history['ordStatus'] == 'Filled']
        print(filled_order_history)

    else:
        print(f'没有获取到现货历史挂单')

except PhemexAPIException as e:
    print(e)
