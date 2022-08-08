# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:16
# @Author: Harper
# @File: cancel all active orders.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# Cancel all active orders
try:
    client.cancel_all_normal_orders(constant.Symbol.uBTCUSD)
except PhemexAPIException as e:
    print(e)
