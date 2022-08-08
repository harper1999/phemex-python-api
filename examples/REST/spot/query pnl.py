# -*- coding=utf-8 -*-
# @Time: 2022/4/4 12:18
# @Author: Harper
# @File: query pnl.py
# @Software: PyCharm

import time
import pandas as pd
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
    start = int(time.mktime(time.strptime('2022-3-10 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    end = int(time.mktime(time.strptime('2022-4-1 00:03:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    now = int(time.time() * 1000)
    r = client.query_pnl(start, now)
    pnl = r['data']['rows']

    if pnl:
        pnl = pd.DataFrame(pnl)
        pnl['collectTime'] = pd.to_datetime(pnl['collectTime'], unit='ms')
        print(pnl)

    else:
        print(f'没有获取到盈亏数据')

except PhemexAPIException as e:
    print(e)
