class PhemexAPIException(Exception):    # 自定义异常PhemexAPIException，基类为Exception
    def __init__(self, response):
        self.code = 0
        try:
            json_res = response.json()  # request库内置的json解码方法
        except ValueError:
            self.message = 'Invalid error message: {}'.format(response.text)  # 服务端返回的错误消息存在response.text
        else:
            if 'code' in json_res:
                self.code = json_res['code']
                self.message = json_res['msg']
            else:
                self.code = json_res['error']['code']
                self.message = json_res['error']['message']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)  # 返回response对象的request属性的值

    def __str__(self):  # pragma: no cover  重写__str__函数 类对象被调用时会自动执行该方法
        return 'HTTP(code=%s), API(errorcode=%s): %s' % (self.status_code, self.code, self.message)
