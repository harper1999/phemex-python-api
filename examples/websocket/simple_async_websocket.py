#encoding:utf-8
import asyncio
import logging
import time
import random
from datetime import datetime
from aiowebsocket.converses import AioWebSocket
import json
from math import trunc
import hmac
import hashlib


async def startup(url):
    main_api_key = '5452620b-ba54-418f-966b-a704c766349d'
    main_api_secret = '-fApQHC2HTQL_JAUE-JeNCFpBL3HMVLr9QW6vfcpiQZkNDUxZWM2Yi1hM2MzLTQzYjMtYWI4Zi1jYWZmM2VlZjFkNTI'
    expiry = trunc(time.time()) + 60
    message = main_api_key + str(expiry)
    signature = hmac.new(main_api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    # 连接websocket
    async with AioWebSocket(url) as aws:
        converse = aws.manipulator
        # 客户端给服务端发送验证消息，观察网页接口数据动态获取
        # await converse.send('{"id":0,"method":"orderbook.subscribe","params":["BTCUSD"]}')
        #await converse.send('{"id":4,"method":"user.auth","params":["PC","eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHRyYSI6ImVkMmVkYTJjLWZlOTYtNDA5NS1hNmVkLTNjYmI0ODFhYmRlNi0xNjUxNzM2MTc1NTUwIiwiaXNzIjoiUEhFTUVYIiwiZXhwIjoxNjUzMTIxOTI5LCJzdWJqIjoyMTMwMDEsImJvZHkiOiLltZrhiJDlg7fno4rwkISY8KWWo_Cfk53ruJHrl4LlgLroi6TjkqsiLCJpYXQiOjE2NTE5MTIzMjl9.rz9HKWbjzBDjcN9snkUFmvQ7zs_vbmMq3YsLo3uFapc"]}')
        auth_msg = {'method': 'user.auth', 'params': ['API', main_api_key, signature, expiry], 'id': 0}
        await converse.send(json.dumps(auth_msg))
        print((await converse.receive()).decode())
        print('______________')
        #await converse.send('{"method": "tick.subscribe", "params": [".BTC"], "id": 2}')
        await converse.send('{"id":7,"method":"aop.subscribe","params":[]}')
        # await converse.send('{"id":1,"method":"trade.subscribe","params":["BTCUSD"]}')
        # await converse.send('{"id":2,"method":"tick.subscribe","params":[".BTC"]}')
        # await converse.send('{"id":3,"method":"tick.subscribe","params":[".MBTC"]}')

        await asyncio.sleep(1)

        # await converse.send('{"id":5,"method":"aop.subscribe","params":[]}')
        # await converse.send('{"id":6,"method":"server.ping","params":[]}')

        while True:
            mes = await converse.receive()
            # 拿到的是byte类型数据，解码为字符串数据
            rec1 = mes.decode()
            print(rec1)
            #
            # try:
            #     millis = int(round(time.time() * 1000))  # 毫秒级时间戳
            #     res = json.loads(rec1)  # 读取字符串
            #     print("res:", res)
            #     a = random.randint(0, 20)  # 随机产生a-b之间的整数，包括a和b
            #     server_time = res["timestamp"] / 1000000
            #     time_diff = millis - server_time
            #     # if a == 10 :
            #     #     await converse.send('{"id":6,"method":"server.ping","params":[]}')
            #
            #     print('localTime:{time}, serverTime: {rec}, time diff: {diff}'
            #           .format(time=millis, rec=server_time, diff=time_diff))
            # except:
            #     logging.info('skip.')


if __name__ == '__main__':
    remote = 'wss://qa.phemex.com/ws'
    testnet_ws = 'wss://testnet.phemex.com/ws'
    main_ws = 'wss://phemex.com/ws'
    i = 0
    # while True:
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
        time.sleep(2)
        i = i + 1
        print("i:", i)
    except KeyboardInterrupt as exc:
        logging.info('Quit.')