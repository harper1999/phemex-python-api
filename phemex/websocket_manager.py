# -*- coding=utf-8 -*-
# @Time: 2022/2/24 0:01
# @Author: Harper
# @File: websocket_manager.py
# @Software: PyCharm

import hmac
import hashlib
import time
from math import trunc
import websocket as ws
import json
import phemex.constant as constant
import threading
import pprint


class WebsocketManager():
    def __init__(self, on_mainnet=False):
        if on_mainnet:
            self.api_URL = constant.URL.highratelimit_wsapi
            self.api_key = ''
            self.api_secret = ''
            # 创建WebSocket连接 协议的建立需要先借助HTTP协议，在服务器返回101状态码之后，就可以进行websocket全双工双向通信了
            # self.ws = ws.create_connection(self.api_URL)  # 短连接
        else:
            self.api_URL = constant.URL.testnet_wsapi
            self.api_key = 'abeb540f-076d-4be7-886b-221b1001a573'
            self.api_secret = 'eh_m1m0KZ3KXRIHIWCp7lhmIcsDOK4MNzdcsmLCNZwQ1MzkxYjU3NC1mM2UzLTRlOWQtYmU0Ny04Njg3MTU1ZTgyYmM'

        ws.enableTrace(True)
        self.ws = ws.WebSocketApp(self.api_URL,
                                  on_message=self.on_message,
                                  on_error=self.on_error,
                                  on_close=self.on_close,
                                  on_open=self.on_open)
        self.ws.run_forever(ping_interval=5, ping_timeout=2)
        # ping_interval 自动发送ping, 设置心跳发送间隔时间
        # ping_timeout 设置从发出ping到收到pong的超时时间
        # Set dispatcher to automatic reconnection  执行中跳转执行on_open
        # rel.signal(2, rel.abort)  # Keyboard Interrupt  返回<Signal Object | Callback:"abort">
        # rel.dispatch()  # 执行中跳转执行on_message

    def on_message(ws, message):  # 在接收到服务器返回的消息时调用。有两个参数，一个是该类本身，一个是从服务器获取的utf-8字符串
        message = json.loads(message)
        # pprint.pprint(message)
        # subscriber(ws)

    def on_error(ws, error):  # 在遇到错误时调用，有两个参数，第一个是该类本身，第二个是异常对象
        print(error)

    def on_close(ws, close_status_code, close_msg):  # 在遇到连接关闭的情况时调用
        print("### closed ###")

    @staticmethod
    def on_open():  # 用于保持连接
        # rel.safe_read()
        print("### connected ###")
        # return self.user_auth()

    def send_heartbeat(self, id, params):  # id必须为int
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#websocket-api-list
        return self.ws.send(json.dumps({'id': id, 'method': 'server.ping', 'params': params}))
        # print(self.ws.recv())
        # self.ws.close()

    def user_auth(self):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#api-user-authentication
        expiry = trunc(time.time()) + 60
        message = self.api_key + str(expiry)
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        request = {'method': 'user.auth', 'params': ['API', self.api_key, signature, expiry], 'id': 1234}
        return self.ws.send(json.dumps(request))

    def subscribe_orderbook(self, id: int, symbol: str):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#subscribe-orderbook
        return self.ws.send(json.dumps({'id': id, 'method': 'orderbook.subscribe', 'params': [symbol]}))
        # print(self.ws.recv())
