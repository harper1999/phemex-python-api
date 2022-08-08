# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:32
# @Author: Harper
# @File: main&sub universal transfer.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# 通用划转 子母账户互转及不同子账户互转 现货和合约均可
try:
    print(client.universal_transfer({'fromUserId': 940516, 'toUserId': 920430, 'currency': constant.Currency.BTC,
                                     'amountEv': 1000_0000, 'bizType': 'SPOT'}))    # btc的amountEv为10^8

except PhemexAPIException as e:
    print(e)
