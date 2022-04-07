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
api_key = 'abeb540f-076d-4be7-886b-221b1001a573'
api_secret = 'eh_m1m0KZ3KXRIHIWCp7lhmIcsDOK4MNzdcsmLCNZwQ1MzkxYjU3NC1mM2UzLTRlOWQtYmU0Ny04Njg3MTU1ZTgyYmM'

test_ws = "wss://testnet.phemex.com/ws"


def on_message(ws, message):
    message = json.loads(message)
    pprint.pprint(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ### ")
    # setp 2: send auth message


def on_open(ws):
    rel.safe_read()
    print("### connected ###")
    # step 2 : send auth message;
    # reference: https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#apiuserauth
    expiry = trunc(time.time()) + 60
    message = api_key + str(expiry)
    signature = hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    request = {'method': 'user.auth', 'params': ['API', api_key, signature, expiry], 'id': 1234}

    ws.send(json.dumps(request))
    sub__aop = json.dumps({"id": 1234, "method": "aop.subscribe", "params": ["BTC"]})
    sub_orderbook = json.dumps({"id": 1234, "method": "orderbook.subscribe", "params": ["SOLUSD"]})
    ws.send(sub_orderbook)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://testnet.phemex.com/ws/", on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection  执行中跳转执行on_open
    rel.signal(2, rel.abort)  # Keyboard Interrupt  返回<Signal Object | Callback:"abort">
    rel.dispatch()  # 执行中跳转执行on_message
