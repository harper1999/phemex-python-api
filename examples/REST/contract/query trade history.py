# -*- coding=utf-8 -*-
# @Time: 2022/6/10 16:07
# @Author: Harper
# @File: query trade history.py
# @Software: PyCharm


import time
import pandas as pd
from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)  # 横向最多显示多少个字符
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', False)  # False表示不允许换行
pd.set_option('display.max_rows', None)  # 显示所有行

# Create a client
client = Client(constant.Gateway.testnet)

try:
    start_time = int(time.mktime(time.strptime('2022-05-10 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    end_time = int(time.mktime(time.strptime('2022-6-20 08:20:33', '%Y-%m-%d %H:%M:%S'))) * 1000
    now = int(time.time())
    r = client.query_user_trades({'symbol': constant.Symbol.LINKUSD,
                                  'tradeType': 'Funding',
                                  'start': start_time,
                                  'end': end_time,
                                  'limit': 50,  # default 50
                                  'offset': 0,
                                  'withCount': True})
    user_trades = r['data']['rows']

    if user_trades:
        user_trades = pd.DataFrame(user_trades)
        user_trades.columns = ['transactTimeNs', 'symbol', 'currency', 'action', 'side', 'tradeType', 'execQty',
                               'execPriceEp', 'orderQty', 'priceEp', 'execValueEv', 'feeRateEr', 'execFeeEv',
                               'closedSize', 'closedPnlEv', 'ordType',
                               'execID', 'orderID', 'clOrdID', 'execStatus']
        user_trades['transactTimeNs'] = pd.to_datetime(user_trades['transactTimeNs'], unit='ns')
        user_trades.rename(columns={'transactTimeNs': 'TransactTime'}, inplace=True)
        print(user_trades)    # 需要关掉pycharm的soft-warp
    else:
        print(f'获取到的历史成交订单为: {user_trades}')

except PhemexAPIException as e:
    print(e)
