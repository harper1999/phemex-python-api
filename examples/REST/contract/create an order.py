# -*- coding=utf-8 -*-
# @Time: 2022/2/20 23:01
# @Author: Harper
# @File: create an order.py
# @Software: PyCharm

import time

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant

# Create a client
client = Client(False)

# place a new order by post, priceEp is scaled price, check our API doc for more info about scaling
# https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#scalingfactors0
try:
    r = client.place_contract_order_by_post({
        "symbol": constant.Symbol.uBTCUSD,
        "clOrdID": "JackTest1" + str(time.time()),
        # "clOrdID": str(uuid.uuid4()),
        "side": constant.Trade.SIDE_BUY,
        "orderQty": 1,
        "priceEp": 3_5000_0000,     # 限价      price scale 10^4
        # "stopPxEp": 3_6000_0000,    # 触发价    与设定价存在大小关系和订单方向限制
        "ordType": constant.Trade.ORDER_TYPE_Limit,    # 订单类型
        # "triggerType": constant.Trade.TriggerType_ByMarkPrice,    # 直接用字符串
        "triggerType": constant.Trade.TriggerType.ByMarkPrice.name,  # 枚举
        "timeInForce": constant.Trade.TIF_GOOD_TILL_CANCEL})
    print("response:" + str(r))
    ordid = r["data"]["orderID"]
except PhemexAPIException as e:
    print(e)

# #  Place a order with stop-loss and take-profit by put
# try:
#     r = client.place_order_by_put({
#         # "actionBy": "FromOrderPlacement",
#         "clOrdID": "order-with-take-profit-stop-loss",
#         "symbol": constant.Symbol.BTCUSD,
#         "side": constant.Trade.SIDE_BUY,
#         "priceEp": 85_0000,
#         "orderQty": 1,
#         "ordType": constant.Trade.ORDER_TYPE_Limit,
#         "takeProfitEp": 120_0000,
#         "tpTrigger": "ByLastPrice",
#         "stopLossEp": 80_0000,
#         "slTrigger": "ByMarkPrice",})
#     print("response:" + str(r))
#     ordid = r["data"]["orderID"]
# except PhemexAPIException as e:
#     print(e)
