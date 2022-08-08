# -*- coding=utf-8 -*-
# @Time: 2022/3/30 14:57
# @Author: Harper
# @File: query withdrawal history.py
# @Software: PyCharm

import pandas as pd
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_rows', None)  # 显示所有行

client = Client(True)

try:
    r = client.withdrawal_history(
        {'currency': constant.Currency.USDT, 'withcount': True, 'limit': 50, 'offset': 0})
    withdrawal_history = r['data']
    print(pd.DataFrame(withdrawal_history))

except PhemexAPIException as e:
    print(e)
