# -*- coding=utf-8 -*-
# @Time: 2022/3/26 12:37
# @Author: Harper
# @File: query closed orders.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

#  query open orders
try:
    r = client.query_closed_orders(constant.Symbol.ETHUSD)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)
