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

# api_key = ""
# api_secret = ""
test_api_key = ''
test_api_secret = '
main_api_key = ''  
main_api_secret = ''

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
    websocket.enableTrace(True)  
    ws = websocket.WebSocketApp(test_ws, on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever(ping_interval=5, ping_timeout=2, dispatcher=rel)
    # Set dispatcher to automatic reconnection 
    rel.signal(2, rel.abort)  
    rel.dispatch()  
