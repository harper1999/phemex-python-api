# -*- coding=utf-8 -*-
# @Time: 2022/5/17 11:07
# @Author: Harper
# @File: query_aop_with_upnl.py
# @Software: PyCharm

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
client = Client(True)

# Get account and positions with unrealised pnl
try:
    response = client.query_account_and_positions(constant.Currency.USD)
    positions = response['data']['positions']
    for position in positions:
        if position['symbol'] == 'DOGEUSD':
            contract_size = 100
            size = position['size']
            avgEntryPrice = position['avgEntryPrice']
            markPrice = position['markPrice']
            positionMargin = position['positionMargin']
            value = position['value']
            unrealised_pnl = size * contract_size * (markPrice - avgEntryPrice)
            cross_leverage = value / (positionMargin + unrealised_pnl)
            pprint.pprint(position)
            print(unrealised_pnl)
            print(cross_leverage)

    # with open('query_account_and_positions.txt', 'w') as fp:
    #     fp.write(json.dumps(response, indent=4))

except PhemexAPIException as e:
    print(e)
