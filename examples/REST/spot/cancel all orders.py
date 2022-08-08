# -*- coding=utf-8 -*-
# @Time: 2022/3/31 16:58
# @Author: Harper
# @File: cancel all orders.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# # Cancel all orders
try:
    client.cancel_all_spot_orders(constant.Symbol.sBTCUSDT)

except PhemexAPIException as e:
    print(e)
