# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:23
# @Author: Harper
# @File: set leverage.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client('testnet')

# Set leverage
try:
    # Set 0 to change back to cross margin
    # Set to 10x
    r = client.change_leverage(constant.Symbol.BTCUSD, 10)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)
