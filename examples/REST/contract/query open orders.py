# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:24
# @Author: Harper
# @File: query open orders.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

#  query open orders
try:
    r = client.query_open_contract_orders(constant.Symbol.uBTCUSD)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)
