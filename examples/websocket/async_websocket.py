# -*- coding=utf-8 -*-
# @Time: 2022/5/11 22:56
# @Author: Harper
# @File: async_websocket.py
# @Software: PyCharm

import asyncio
import logging
import time
from aiowebsocket.converses import AioWebSocket
import json
import hmac
import hashlib
import math

test_ws = "wss://testnet.phemex.com/ws"
main_ws = 'wss://phemex.com/ws'
qa_ws = 'wss://qa.phemex.com/ws'
api_key = '8e0e1e93-c8d0-485f-91ea-b0db6c275db8'
api_secret = '30nQNogHer5kaUYR2tjSX9KQBbwXa2RqCZayf2LHtAI1MWFlNzExYi1kODNhLTQwMTEtYjhiNi1kOWUzZjA0YTZlNjY'
test_api_key = "abeb540f-076d-4be7-886b-221b1001a573"
test_api_secret = "eh_m1m0KZ3KXRIHIWCp7lhmIcsDOK4MNzdcsmLCNZwQ1MzkxYjU3NC1mM2UzLTRlOWQtYmU0Ny04Njg3MTU1ZTgyYmM"
prod_api_key = '5452620b-ba54-418f-966b-a704c766349d'  # by HK IP
prod_api_secret = '-fApQHC2HTQL_JAUE-JeNCFpBL3HMVLr9QW6vfcpiQZkNDUxZWM2Yi1hM2MzLTQzYjMtYWI4Zi1jYWZmM2VlZjFkNTI'


# async协程本质上还是单进程单线程，并不能提升运算速度，但是适合处理需要等待的任务
async def startup(url):  # 定义协程函数 coroutine function
    async with AioWebSocket(url) as aws:  # 异步上下文管理器 必须嵌套在协程函数内 aws为AioWebSocket类对象
        converse = aws.manipulator
        # 客户端给服务端发送验证消息，观察网页接口数据动态获取
        # await converse.send('{"id":0,"method":"orderbook.subscribe","params":["BTCUSD"]}')
        # await converse.send('{"id":4,"method":"user.auth","params":["PC","eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHRyYSI6ImVkMmVkYTJjLWZlOTYtNDA5NS1hNmVkLTNjYmI0ODFhYmRlNi0xNjUxNzM2MTc1NTUwIiwiaXNzIjoiUEhFTUVYIiwiZXhwIjoxNjUzMTIxOTI5LCJzdWJqIjoyMTMwMDEsImJvZHkiOiLltZrhiJDlg7fno4rwkISY8KWWo_Cfk53ruJHrl4LlgLroi6TjkqsiLCJpYXQiOjE2NTE5MTIzMjl9.rz9HKWbjzBDjcN9snkUFmvQ7zs_vbmMq3YsLo3uFapc"]}')
        tasks = [asyncio.create_task(send_heartbeat(converse)), asyncio.create_task(authentication(converse)),
                 asyncio.create_task(sub_aop(converse))]  # ,  asyncio.create_task(sub_orderbook(converse))
        # task = (asyncio.current_task())
        # await asyncio.wait(tasks, timeout=10)
        try:
            for task in tasks:
                await asyncio.wait_for(task, timeout=5)
                # udp_socket.close()
            # for task in tasks:
            #     task.cancel()
            #     try:
            #         await task
        #     #     except asyncio.CancelledError:
        #     #         print("all tasks has been cancelled")
        except asyncio.TimeoutError:
            print(f'timeout: {time.ctime(time.time())}')


async def send_heartbeat(ws):
    heartbeat_msg = json.dumps({'id': 0, 'method': 'server.ping', 'params': []})
    while True:
        await asyncio.sleep(5)  # 每隔5秒发一次心跳包
        await ws.send(heartbeat_msg)
        # heartbeat_res = (await ws.receive()).decode('utf-8')
        # print(f'ping: {time.ctime(time.time())}    msg: {str(heartbeat_res)}')


async def authentication(ws):
    expiry = math.trunc(time.time()) + 60
    message = test_api_key + str(expiry)
    signature = hmac.new(test_api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    auth_msg = json.dumps({'method': 'user.auth', 'params': ['API', test_api_key, signature, expiry], 'id': 100})
    await ws.send(auth_msg)
    auth_res = (await ws.receive()).decode('utf-8')  # 从服务端接收字节型数据并解码为字符串
    print(f'auth-time: {time.ctime(time.time())}    msg: {str(auth_res)}')
    print('_' * 100)


async def sub_aop(ws):
    aop_msg = json.dumps({"id": 200, "method": "aop.subscribe", "params": []})
    while True:
        await asyncio.sleep(1)
        await ws.send(aop_msg)
        aop_res = (await ws.receive()).decode('utf-8')
        print(aop_res)


async def sub_orderbook(ws):
    print(f'orderbook_sub_time: {time.ctime(time.time())}')
    orderbook_msg = json.dumps({"id": 300, "method": "orderbook.subscribe", "params": ['BTCUSD']})
    while True:
        await ws.send(orderbook_msg)
        await asyncio.sleep(0.5)
        orderbook_res = (await ws.receive()).decode('utf-8')
        print(orderbook_res)
        # await unsub_orderbook(ws, task)


async def unsub_orderbook(ws):
    await asyncio.sleep(5)
    unsub_orderbook_msg = json.dumps({"id": 301, "method": "orderbook.unsubscribe", "params": []})
    await ws.send(unsub_orderbook_msg)
    unsub_orderbook_res = (await ws.receive()).decode('utf-8')
    print(f'unsub-time: {time.ctime(time.time())}    msg: {str(unsub_orderbook_res)}')


# await converse.send('{"method": "tick.subscribe", "params": [".BTC"], "id": 2}')
# await converse.send('{"id":1,"method":"trade.subscribe","params":["BTCUSD"]}')
# await converse.send('{"id":2,"method":"tick.subscribe","params":[".BTC"]}')
# await converse.send('{"id":3,"method":"tick.subscribe","params":[".MBTC"]}')
# await converse.send('{"id":6,"method":"server.ping","params":[]}')

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        # 运行协程需要进入异步模式(即进入event_loop)，开始控制整个程序的状态，然后把协程对象转为任务task
        asyncio.run(startup(test_ws))
        # loop = asyncio.get_event_loop()  # 生成事件循环对象
        # loop.run_until_complete(startup(test_ws))  # 检测异步对象任务的状态

    except KeyboardInterrupt as exc:
        logging.info('Quit.')
