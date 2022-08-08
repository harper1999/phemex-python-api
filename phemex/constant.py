# -*- coding=utf-8 -*-
# @Time: 2022/2/24 14:03
# @Author: Harper
# @File: constant.py
# @Software: PyCharm

from enum import Enum


class Gateway:
    testnet = 'testnet'
    api = 'api'
    vapi = 'vapi'
    highratelimit_restapi = 'https://vapi.phemex.com'
    mainnet_api = 'https://api.phemex.com'
    testnet_api = 'https://testnet-api.phemex.com'
    wsapi = "wss://coinsecure.in/websocket"
    highratelimit_wsapi = 'wss://vapi.phemex.com/ws'
    testnet_wsapi = 'wss://testnet.phemex.com/ws'


class Currency:
    BTC = "BTC"
    USD = "USD"
    USDT = "USDT"
    TRX = 'TRX'


class Symbol:
    u1000RSRUSD = 'u1000RSRUSD'
    APEUSD = 'APEUSD'
    BTCUSD = "BTCUSD"
    ETHUSD = "ETHUSD"
    XRPUSD = "XRPUSD"
    LINKUSD = "LINKUSD"
    MKRUSD = "MKRUSD"
    GOLDUSD = "GOLDUSD"  # deprecated
    SOLUSD = "SOLUSD"
    DOGEUSD = 'DOGEUSD'
    GLMRUSD = 'GLMRUSD'
    ZECUSD = 'ZECUSD'
    uBTCUSD = 'uBTCUSD'
    sBTCUSDT = 'sBTCUSDT'
    sDAIUSDT = 'sDAIUSDT'
    sSOLUSDT = 'sSOLUSDT'
    sFEIUSDT = 'sFEIUSDT'
    cETHUSD = 'cETHUSD'


class Trade:
    SIDE_BUY = "Buy"
    SIDE_SELL = "Sell"

    ORDER_TYPE_Market = "Market"
    ORDER_TYPE_Limit = "Limit"
    ORDER_TYPE_Stop = "Stop"
    ORDER_TYPE_LimitIfTouched = "LimitIfTouched"
    ORDER_TYPE_MarketIfTouched = "MarketIfTouched"

    qtyType_ByBase = 'ByBase'
    qtyType_ByQuote = 'ByQuote'
    TriggerType_ByMarkPrice = "ByMarkPrice"
    TriggerType_ByLastPrice = "ByLastPrice"
    TriggerType = Enum('TriggerType', ('ByMarkPrice', 'ByLastPrice'))

    TIF_IMMEDIATE_OR_CANCEL = "ImmediateOrCancel"
    TIF_GOOD_TILL_CANCEL = "GoodTillCancel"
    TIF_FOK = "FillOrKill"
    PostOnly = 'PostOnly'

    ORDER_STATUS_NEW = "New"
    ORDER_STATUS_PFILL = "PartiallyFilled"
    ORDER_STATUS_FILL = "Filled"
    ORDER_STATUS_CANCELED = "Canceled"
    ORDER_STATUS_REJECTED = "Rejected"
    ORDER_STATUS_TRIGGERED = "Triggered"
    ORDER_STATUS_UNTRIGGERED = "Untriggered"
