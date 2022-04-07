import hmac
import hashlib
import json
import requests
import time
from math import trunc
from .exceptions import PhemexAPIException
import phemex.constant as constant
import logging


class Client(object):
    def __init__(self, on_mainnet=False):
        if on_mainnet:
            self.api_URL = constant.URL.mainnet_api
            self.api_key = '4e9794b2-8644-4fd4-973f-f0a5be6c6763'
            self.api_secret = 'e8dfd4Gtm8D7vuO9CJrBJuLpzC2v0MyFQqoXeNgGc-ZjMzdiOThjOS1lOGU0LTRmMDEtODAxYi1lMmUyMzc0ZDA1YzA'
        else:
            self.api_URL = constant.URL.testnet_api
            self.api_key = "abeb540f-076d-4be7-886b-221b1001a573"
            self.api_secret = "eh_m1m0KZ3KXRIHIWCp7lhmIcsDOK4MNzdcsmLCNZwQ1MzkxYjU3NC1mM2UzLTRlOWQtYmU0Ny04Njg3MTU1ZTgyYmM"
        self.session = requests.session()

    def _send_request(self, method, endpoint, params=None, body=None):
        query_string = ''
        if params:
            query_string = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        expiry = str(trunc(time.time()) + 60)
        message = endpoint + query_string + expiry
        body_str = ""
        if body:
            body_str = json.dumps(body, separators=(',', ':'))  # separators参数以元组(值分隔符，键分隔符)的形式指定分隔符
            message += body_str
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
        # 利用哈希256算法，输入一个密钥和一个消息(待加密的字符串)，输出一个消息摘要
        url = self.api_URL + endpoint
        if query_string:
            url += '?' + query_string

        self.session.headers.update({
            'x-phemex-request-signature': signature.hexdigest(),  # 以十六进制格式输出加密后的字符串
            'x-phemex-request-expiry': expiry,
            'x-phemex-access-token': self.api_key,
            'Content-Type': 'application/json',
            'x-phemex-request-tracing': '',  # 用户端携带uuid(要求小于40字节)来追溯延迟问题
        })
        response = self.session.request(method, url, data=body_str.encode())
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s')
        # :%(lineno)s 以格式化输出程序执行的行号
        # logging.debug(response.headers)
        if 'x-ratelimit-remaining' in response.headers:
            sub_dict = {a: response.headers[a] for a in
                        ['x-phemex-request-tracing', 'x-ratelimit-remaining', 'x-ratelimit-capacity']}
            logging.debug(sub_dict)  # 输出响应头中的请求查询号，单轮最大请求数和剩余可用请求数

        if not str(response.status_code).startswith('2'):  # 如果响应体中的状态码不是以2开头
            raise PhemexAPIException(response)
        try:
            res_json = response.json()  # 接口响应都是json格式的数据 以反序列化返回response对象中的二进制流content
        except ValueError:
            raise PhemexAPIException('Invalid Response: %s' % response.text)
        if "code" in res_json and res_json["code"] != 0:
            raise PhemexAPIException(response)
        if "error" in res_json and res_json["error"]:
            raise PhemexAPIException(response)
        return res_json

    def query_account_and_positions(self, currency: str):  # 指定参数currency的类型为字符串
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-trading-account-and-positions
        """
        return self._send_request("get", "/accounts/accountPositions", {'currency': currency})

    def quotation(self, params: dict):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Transfer-API-en.md#convert
        """
        return self._send_request("get", "/assets/quote", params=params)

    def convert_asset(self, body: dict):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Transfer-API-en.md#convert
        """
        return self._send_request("post", "/assets/convert", body=body)

    def place_contract_order_by_post(self, body):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#placeorder
        """
        return self._send_request("post", "/orders", body=body)

    def place_spot_order_by_post(self, body):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#place-order
        """
        return self._send_request("post", "/spot/orders", body=body)

    def place_order_by_put(self, params: dict):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#placeorder
        """
        return self._send_request("put", "/orders/create", params=params)

    def amend_order(self, params: dict):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#622-amend-order-by-orderid
        """
        return self._send_request("put", "/orders/replace", params=params)

    def cancel_order(self, symbol, orderID):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#623-cancel-single-order
        """
        return self._send_request("delete", "/orders/cancel", params={"symbol": symbol, "orderID": orderID})

    def _cancel_all(self, endpoint, symbol, untriggered_order: bool):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#625-cancel-all-orders
        """
        return self._send_request("delete", endpoint,
                                  params={"symbol": symbol, "untriggered": str(untriggered_order).lower()})

    def cancel_all_normal_orders(self, symbol):
        self._cancel_all(endpoint='', symbol=symbol, untriggered_order=False)

    def cancel_all_untriggered_conditional_orders(self, symbol):
        self._cancel_all(endpoint='', symbol=symbol, untriggered_order=True)

    def cancel_all_contract_orders(self, symbol):
        self._cancel_all("/orders/all", symbol, untriggered_order=False)
        self._cancel_all("/orders/all", symbol, untriggered_order=True)

    def cancel_all_spot_orders(self, symbol):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#cancel-all-order-by-symbol
        self._cancel_all("/spot/orders/all", symbol, untriggered_order=False)
        self._cancel_all("/spot/orders/all", symbol, untriggered_order=True)

    def change_leverage(self, symbol, leverage=0):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#627-change-leverage
        """
        return self._send_request("PUT", "/positions/leverage", params={"symbol": symbol, "leverage": leverage})

    def change_risklimit(self, symbol, risk_limit=0):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#628-change-position-risklimit
        """
        return self._send_request("PUT", "/positions/riskLimit", params={"symbol": symbol, "riskLimit": risk_limit})

    def query_open_spot_orders(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#query-all-open-orders-by-symbol
        """
        return self._send_request("GET", "/spot/orders", params={"symbol": symbol})

    def query_open_contract_orders(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#6210-query-open-orders-by-symbol
        """
        return self._send_request("GET", "/orders/activeList", params={"symbol": symbol})

    def query_closed_orders(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#6210-query-open-orders-by-symbol
        """
        return self._send_request("GET", "/exchange/order/list", params={"symbol": symbol})

    def query_spot_orderbook(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#query-order-book-1
        """
        return self._send_request('get', '/v1/md/orderbook', params={'symbol': symbol})

    def query_contract_orderbook(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#query-order-book-1
        """
        return self._send_request('get', '/md/orderbook', params={'symbol': symbol})

    def query_24h_ticker(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#633-query-24-hours-ticker
        """
        return self._send_request("GET", "/md/ticker/24hr", params={"symbol": symbol})

    def query_client_and_wallet(self, offset, limit, withCount):  # offset分页 limit限制查询账号数量  withCount是否查询所有账号
        return self._send_request('get', '/phemex-user/users/children',
                                  params={'offset': offset, 'limit': limit, 'withCount': withCount})

    def query_trading_account(self, currency):  # offset分页 limit限制查询账号数量  withCount是否查询所有账号
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-client-and-wallets
        return self._send_request('get', '/accounts/accountPositions', params={'currency': currency})

    def spot_transfer_from_sub_to_main(self, amountEv, currency: str):
        return self._send_request('post', '/assets/spots/sub-accounts/transfer',
                                  body={'amountEv': amountEv, 'currency': currency})

    def universal_transfer(self, body: dict):
        return self._send_request('post', '/assets/universal-transfer', body=body)

    def query_transfer_hisotry(self, params: dict):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Transfer-API-en.md#query-transfer-history
        return self._send_request('get', '/assets/transfer', params=params)

    def query_sub_to_main_spot_transfer(self, params: dict):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Transfer-API-en.md#query-transfer-history
        return self._send_request('get', '/assets/spots/sub-accounts/transfer', params=params)

    def query_kline(self, symbol, start_time, end_time, resolution):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-kline
        return self._send_request('get', '/exchange/public/md/kline',
                                  params={'symbol': symbol, 'from': start_time, 'to': end_time,
                                          'resolution': resolution})

    def query_recent_trades(self, symbol):
        return self._send_request('get', '/md/trade', params={'symbol': symbol})

    def query_historical_trades(self, market, since: str):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-history-trades-by-symbol
        return self._send_request('get', '/exchange/public/nomics/trades', params={'market': market, 'since': since})

    def query_user_trades(self, params: dict):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-history-trades-by-symbol
        return self._send_request('get', '/exchange/order/trade', params=params)

    def query_history_trades(self, symbol, start, end):
        return self._send_request('get', '/api-data/spots/trades',
                                  params={'symbol': symbol, 'start': start, 'end': end})

    def query_spot_order_history(self, params: dict):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#query-orders-history
        return self._send_request('get', '/api-data/spots/orders', params=params)

    def query_pnl(self, start=None, end=None):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#spotDataPnls
        return self._send_request('get', '/api-data/spots/pnls', params={'start': start, 'end': end})

    def query_trading_fee_history(self, params):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-trading-fees-history
        return self._send_request('get', '/api-data/futures/trading-fees', params=params)

    def chain_name(self, currency: str):
        return self._send_request('get', '/exchange/public/cfg/chain-settings', {'currency': currency})

    def query_deposit_address(self, currency, chainName):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Spot-API-en.md#query-deposit-address-by-currency
        return self._send_request('get', '/exchange/wallets/v2/depositAddress',
                                  params={'currency': currency, 'chainName': chainName})

    def withdrawal_history(self, params):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#query-trading-fees-history
        return self._send_request('get', '/exchange/wallets/withdrawList', params=params)

    def request_withdrawal(self, params: dict, body: dict):
        # https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#request-withdraw
        return self._send_request('post', '/exchange/wallets/v2/createWithdraw', params=params, body=body)
