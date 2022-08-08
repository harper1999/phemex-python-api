# -*- coding=utf-8 -*-
# @Time: 2022/3/29 10:38
# @Author: Harper
# @File: query transfer history.py
# @Software: PyCharm

import pandas as pd
import time
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_rows', None)  # 显示所有行

client = Client(constant.Gateway.testnet)

# 查询主账户划转历史
try:
    start = int(time.mktime(time.strptime('2021-1-1 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    end = int(time.mktime(time.strptime('2022-4-1 00:03:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    now = int(time.time() * 1000)
    r = client.query_transfer_hisotry(
        {'currency': constant.Currency.USD, 'start': start, 'end': now, 'limit': 50, 'offset': 0})
    transfer_history = pd.DataFrame(r['data']['rows'])
    print(transfer_history)

except PhemexAPIException as e:
    print(e)
