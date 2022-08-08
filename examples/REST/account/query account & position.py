# -*- coding=utf-8 -*-
# @Time: 2022/2/20 22:49
# @Author: Harper
# @File: query account & position.py
# @Software: PyCharm

import pprint
import json
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(constant.Gateway.testnet)

# Get account and positions
try:
    response = client.query_account_and_positions(constant.Currency.BTC)  # 非实时 保存上一次仓位变动快照
    # response = client.query_account_and_positions(constant.Symbol.DOGEUSD)
    pprint.pprint(response)
    # with open('query_account_and_positions.txt', 'w') as fp:
    #     fp.write(json.dumps(response, indent=4))

except PhemexAPIException as e:
    print(e)

