# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:17
# @Author: Harper
# @File: cancel all conditional orders.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# Cancel all conditional orders
try:
    client.cancel_all_untriggered_conditional_orders(constant.Symbol.BTCUSD)
except PhemexAPIException as e:
    print(e)