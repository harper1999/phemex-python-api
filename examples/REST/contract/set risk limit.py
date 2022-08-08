# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:23
# @Author: Harper
# @File: set risk limit.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# Set risk limit for 150 BTC
try:
    r = client.change_risklimit(constant.Symbol.BTCUSD, 150)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)