import threading
import rel
import websocket
import time
import sys
import json
from math import trunc
import hmac
import hashlib
import pprint

# api_key = "2dfd9f1a-ff73-462a-8f69-0274e043b323"
# api_secret = "6b9XnreinDMCNNlaNxfeoblIXiRcALtco35KcholPx5iMjI0ZTY5NS00MWY5LTRiOGMtYWZmMC1lZDc3ZjdmMTgzYjQ"
test_api_key = 'd351ce2d-10b4-4692-b9c4-390fa688e839'
test_api_secret = 'nOPiUHr5_VQ_rSbNkiOp7Ef-9EdBVsL1BG6eVAGE2ok5ZjEwZjJjMS03ZTZmLTQzNTktYWE1Yi0xNzI0YzNjODI0MDk'
main_api_key = '1f31da3c-3747-4b88-b423-e8b524b44de9'  # 主账户
main_api_secret = 'ZLRKwDte6zdOlQAA4nsPUu1b9x_OiOGzjhnc-xFjWlEzYmJhZGJlNy1kNzljLTRiZjctOGQxMS1iNDI0MjA4YWM3NmI'

test_ws = "wss://testnet.phemex.com/ws"
main_ws = 'wss://phemex.com/ws'
qa_ws = 'wss://qa.phemex.com/ws'


def on_message(ws, message):
    message = json.loads(message)
    pprint.pprint(message)


def on_error(ws, error):
    # error = json.loads(error)
    pprint.pprint(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ### ")
    # setp 2: send auth message


def on_open(ws):
    rel.safe_read()
    print("### connected ###")
    # step 2 : send auth message;
    # reference: https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#apiuserauth
    expiry = trunc(time.time()) + 60
    message = test_api_key + str(expiry)
    signature = hmac.new(test_api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    auth_msg = {'method': 'user.auth', 'params': ['API', test_api_key, signature, expiry], 'id': 0}
    # ws.send(json.dumps(auth_msg))
    # time.sleep(0.5)

    # sub__24h_ticker = json.dumps({"id": 300, "method": "market24h.subscribe", "params": ["BTCUSD"]})
    # ws.send(sub__24h_ticker)

    # sub__aop = json.dumps({"id": 7, "method": "aop.subscribe", "params": []})
    # ws.send(sub__aop)

    # sub__index_tick = json.dumps({"id": 9, "method": "tick.subscribe", "params": ['.MBTC']})
    # sub__mark_tick = json.dumps({"id": 9, "method": "tick.subscribe", "params": ['.BTC']})
    # sub__prf_tick = json.dumps({"id": 9, "method": "tick.subscribe", "params": ['.BTCFR']})
    # sub__funding_rate_tick = json.dumps({"id": 9, "method": "tick.subscribe", "params": ['.BTCFR8H']})
    # ws.send(sub__index_tick)
    # time.sleep(1)

    # sub__trade = json.dumps({"id": 100, "method": "trade.subscribe", "params": ["BTCUSD"]})
    # ws.send(sub__trade)   # 市场实时交易数据
    # time.sleep(1)
    # sub_orderbook = json.dumps({"id": 200, "method": "orderbook.subscribe", "params": ["SOLUSD"]})
    # ws.send(sub_orderbook)
    # time.sleep(3)
    # unsub_orderbook = json.dumps({"id": 201, "method": "orderbook.unsubscribe", "params": ["SOLUSD"]})
    # ws.send(unsub_orderbook)


if __name__ == "__main__":
    websocket.enableTrace(True)  # 开启运行状态追踪
    ws = websocket.WebSocketApp(test_ws, on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever(ping_interval=5, ping_timeout=2, dispatcher=rel)
    # Set dispatcher to automatic reconnection  执行中跳转执行on_open
    rel.signal(2, rel.abort)  # Keyboard Interrupt  返回<Signal Object | Callback:"abort">
    rel.dispatch()  # 执行中跳转执行on_message
