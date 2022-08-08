# -*- coding=utf-8 -*-
# @Time: 2022/3/30 21:05
# @Author: Harper
# @File: query deposit address.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

client = Client(constant.Gateway.testnet)

try:
    # print(client.chain_name('USDT')['data']['USDT'])  # 查询币种的链信息
    deposit_address = client.query_deposit_address(constant.Currency.USDT, constant.Currency.TRX)
    print(deposit_address)

except PhemexAPIException as e:
    print(e)
