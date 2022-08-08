# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:26
# @Author: Harper
# @File: query asset.py
# @Software: PyCharm

import pprint
import phemex.constant as constant
from phemex.client import Client
from phemex.exceptions import PhemexAPIException

client = Client(constant.Gateway.testnet)

# 查询所有账户资产信息
try:
    asset = client.query_client_and_wallet(0, 50, True)
    pprint.pprint(asset)
    # with open('query asset.txt', 'w') as fp:
    #     fp.write(json.dumps(asset, indent=4))

except PhemexAPIException as e:
    print(e)

