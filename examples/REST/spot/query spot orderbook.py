# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:36
# @Author: Harper
# @File: query spot orderbook.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# 查询订单薄
try:
    print(client.query_spot_orderbook(constant.Symbol.BTCUSD))
except PhemexAPIException as e:
    print(e)
