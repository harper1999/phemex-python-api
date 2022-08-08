# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:10
# @Author: Harper
# @File: replace an order.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant


# Send replace if this order not filled yet
client = Client(constant.Gateway.testnet)

try:
    r = client.replace_order({
        'symbol': constant.Symbol.LINKUSD,
        'orderID': 'b933ee27-d1c5-4b9a-9d94-75e107c86ee6',
        'priceEp': 85000})
    print("response:" + str(r))


# client = Client('api')
# try:
#     r = client.replace_order({
#         'symbol': constant.Symbol.LINKUSD,
#         'orderID': 'bb2fe060-aa9a-4afe-9d24-5a86943ae962',
#         'priceEp': 85000})
#     print("response:" + str(r))

except PhemexAPIException as e:
    print(e)

