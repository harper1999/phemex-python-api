# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:38
# @Author: Harper
# @File: query market trade history.py
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
client = Client(constant.Gateway.api)

# 查询市场数据 历史成交订单
try:
    # r = client.query_historical_trades(constant.Symbol.BTCUSD, '0-0-0')
    # r = client.query_historical_trades(constant.Symbol.BTCUSD, '1341-2-1')
    r = client.query_historical_trades(constant.Symbol.uBTCUSD, '0-0-0')
    # r = client.query_historical_trades(constant.Symbol.cETHUSD, '0-0-0')
    data = r['data']

    if data:
        historical_trades = pd.DataFrame(r['data'])  # pd会自动把列表中的字典键作为列名
        print(historical_trades)
        #  z: zero 表示UTC0  T: 时间分隔符 无实际意义
    else:
        print(f'获取到的历史成交订单为: {data}')

except PhemexAPIException as e:
    print(e)

