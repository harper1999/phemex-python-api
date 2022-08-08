# -*- coding=utf-8 -*-
# @Time: 2022/3/28 16:55
# @Author: Harper
# @File: conversion.py
# @Software: PyCharm
import pytest

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant


def setup_module():
    print('\n...初始化模块')


def teardown_module():
    print('\n...清除模块')


def test_main():
    # Create a client
    client = Client(constant.Gateway.testnet)

    try:
        # value scale 10^8
        quotation = client.quotation({'fromCurrency': 'BTC', 'toCurrency': 'USDT', 'fromAmountEv': 10_0000})
        conversion = client.convert_asset({'fromCurrency': 'BTC', 'toCurrency': 'USDT', 'fromAmountEv': 10_0000,
                                           'code': quotation['data']['code']})  # code取自/assets/quote的返回值code
        print(conversion)

    except PhemexAPIException as e:
        print(e)


if __name__ == '__main__':
    pytest.main(['-v'])
