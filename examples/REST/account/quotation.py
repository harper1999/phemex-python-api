# -*- coding=utf-8 -*-
# @Time: 2022/3/28 17:25
# @Author: Harper
# @File: quotation.py
# @Software: PyCharm


from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant


client = Client(constant.Gateway.testnet)

try:
    quotation = client.quotation({'fromCurrency': 'BTC', 'toCurrency': 'USD', 'fromAmountEv': 1_0000})
    print(quotation)

except PhemexAPIException as e:
    print(e)

