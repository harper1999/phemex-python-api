# -*- coding=utf-8 -*-
# @Time: 2022/3/11 18:04
# @Author: Harper
# @File: query history trades.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant
import time

# Create a client
client = Client(constant.Gateway.testnet)

try:
    start_time = int(time.mktime(time.strptime('2022-3-10 00:00:00', '%Y-%m-%d %H:%M:%S'))*1000)  # 要求毫秒级即需要*1000
    end_time = int(time.mktime(time.strptime('2022-3-13 00:00:00', '%Y-%m-%d %H:%M:%S'))*1000)
    print(client.query_history_trades(constant.Symbol.sBTCUSDT, start_time, end_time))
except PhemexAPIException as e:
    print(e)

