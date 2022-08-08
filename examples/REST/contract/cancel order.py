# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:12
# @Author: Harper
# @File: cancel one order.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# Cancel one order
try:
    orderID = 'afa3f05c-c94c-4f3c-8fb1-39c055ef11d5'
    r = client.cancel_order(constant.Symbol.SOLUSD, orderID)
    print("response:" + str(r))

except PhemexAPIException as e:
    print(e)
