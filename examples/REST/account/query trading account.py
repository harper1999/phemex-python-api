# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:32
# @Author: Harper
# @File: query trading account.py
# @Software: PyCharm

import pprint
import json
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant


# Create a client
client = Client(constant.Gateway.testnet)

# 查询交易账户资产信息
try:
    trading_account = client.query_trading_account('USD')
    pprint.pprint(trading_account)
    # with open('query_trading_account.txt', 'w') as fp:
    #     fp.write(json.dumps(trading_account, indent=4))

except PhemexAPIException as e:
    print(e)
