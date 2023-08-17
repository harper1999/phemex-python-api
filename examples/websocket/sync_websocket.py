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
    # reference: https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#apiuserauth
    expiry = trunc(time.time()) + 60
    message = test_api_key + str(expiry)
    signature = hmac.new(test_api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    auth_msg = {'method': 'user.auth', 'params': ['API', test_api_key, signature, expiry], 'id': 0}
    sub__aop = json.dumps({"id": 7, "method": "aop.subscribe", "params": []})
    ws.send(sub__aop)


if __name__ == "__main__":
    websocket.enableTrace(True)  
    ws = websocket.WebSocketApp(test_ws, on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever(ping_interval=5, ping_timeout=15)
    # Set dispatcher to automatic reconnection 

