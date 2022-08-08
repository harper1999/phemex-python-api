# -*- coding=utf-8 -*-
# @Time: 2022/3/30 14:53
# @Author: Harper
# @File: request withdrawal.py
# @Software: PyCharm

from phemex.client import Client
from phemex.exceptions import PhemexAPIException
import phemex.constant as constant
import pyotp

client = Client(constant.Gateway.testnet)

# 该接口目前仅供内部使用
try:
    google_secret = ''
    totp = pyotp.TOTP(google_secret)  # Time-based One-Time Password，表示基于时间戳算法的一次性密码
    otpCode = totp.now()
    r = client.request_withdrawal({'otpCode': otpCode},
                                  {'address': 'TFSjunMkCds1Nqz68UedJQPhVthdvqUE2D', 'amountEv': 100_0000_0000,
                                   'currency': constant.Currency.USDT})
    print(r)

except PhemexAPIException as e:
    print(e)
