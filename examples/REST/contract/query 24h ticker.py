# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:25
# @Author: Harper
# @File: query 24h ticker.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(gateway='api')
# client1 = Client(gateway='vapi')

# 可查最优挂单
try:
    r = client.query_24h_ticker(constant.Symbol.BTCUSD)
    # r1 = client1.query_24h_ticker(constant.Symbol.BTCUSD)
    print(r)
    # print(r1)

except PhemexAPIException as e:
    print(e)

