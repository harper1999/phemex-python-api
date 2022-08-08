# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:38
# @Author: Harper
# @File: query recent trades.py
# @Software: PyCharm

import json
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(True)

try:
    print(client.query_recent_trades(constant.Symbol.SOLUSD))
except PhemexAPIException as e:
    print(e)