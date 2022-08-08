# -*- coding=utf-8 -*-
# @Time: 2022/2/24 22:56
# @Author: Harper
# @File: test.py
# @Software: PyCharm


import hashlib
import hmac
import json
import threading
import time
from math import trunc
import websocket

api_key = 'abeb540f-076d-4be7-886b-221b1001a573'
api_secret = 'eh_m1m0KZ3KXRIHIWCp7lhmIcsDOK4MNzdcsmLCNZwQ1MzkxYjU3NC1mM2UzLTRlOWQtYmU0Ny04Njg3MTU1ZTgyYmM'


def on_message(ws, message):  # 在接收到服务器返回的消息时调用。有两个参数，一个是该类本身，一个是从服务器获取的字符串（utf-8格式）
    print(message)


def on_error(ws, error):  # 在遇到错误时调用，有两个参数，第一个是该类本身，第二个是异常对象
    print(error)


def on_close(ws, close_status_code, close_msg):  # 在遇到连接关闭的情况时调用
    print("### closed ###")


def on_open(ws):  # 用于保持连接
    def run(*args):
        # send the message, then wait so thread doesn't exit and socket isn't closed
        ws.send(json.dumps({'id': 0, 'method': 'orderbook.subscribe', 'params': ['BTCUSD']}))
        # ws.send(json.dumps({'id': 1234, 'method': 'aop.subscribe', 'params': []}))
        time.sleep(0.1)  # 挂起线程 单位为秒
        # print('当前程序的线程为：%s' % threading.enumerate())

        print("Thread terminating...")

    expiry = trunc(time.time()) + 60
    message = api_key + str(expiry)
    signature = hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    request = {'method': 'user.auth', 'params': ['API', api_key, signature, expiry], 'id': 1234}
    ws.send(json.dumps(request))
    t = threading.Thread(target=run)
    t.start()
    t.join()  # 使被调用的该线程执行完毕后，才能继续执行


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://testnet.phemex.com/ws',
                                on_message=on_message,
                                on_error=on_error,
                                on_open=on_open,
                                on_close=on_close)

    ws.run_forever()
