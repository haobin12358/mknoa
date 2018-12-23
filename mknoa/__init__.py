# -*- coding: utf-8 -*-
import json
from datetime import datetime, date

from flask import current_app, Blueprint, Flask as _Flask, Request as _Request
from werkzeug.exceptions import HTTPException
from flask.json import JSONEncoder as _JSONEncoder
from flask_cors import CORS

from mknoa.api.v1.AUsers import AUser
from mknoa.api.v1.APowers import APowers
from mknoa.api.v1.AMoulds import AMoulds
from mknoa.api.v1.ANotice import ANotice
from mknoa.common.request_handler import error_handler, request_first_handler
from mknoa.config.secret import DefaltSettig
from mknoa.extensions.register_ext import register_ext
from mknoa.extensions.loggers import LoggerHandler

class JSONEncoder(_JSONEncoder):
    """重写对象序列化, 当默认jsonify无法序列化对象的时候将调用这里的default"""
    def default(self, o):

        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            res = dict(o)
            new_res = {k.lower(): v for k, v in res.items()}
            return new_res
        if isinstance(o, datetime):
            # 也可以序列化时间类型的对象
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, type):
            raise o()
        if isinstance(o, HTTPException):
            raise o
        raise TypeError(repr(o) + " is not JSON serializable")


class Request(_Request):
    def on_json_loading_failed(self, e):
        from mknoa.common.error_response import ParamsError
        if current_app is not None and current_app.debug:
            raise ParamsError('Failed to decode JSON object: {0}'.format(e))
        raise ParamsError('参数异常')

    def get_json(self, force=False, silent=False, cache=True):
        data = self.data
        if not data:
            return
        try:
            rv = json.loads(data)
        except ValueError as e:
            if silent:
                rv = None
                if cache:
                    normal_rv, _ = self._cached_json
                    self._cached_json = (normal_rv, rv)
            else:
                rv = self.on_json_loading_failed(e)
                if cache:
                    _, silent_rv = self._cached_json
                    self._cached_json = (rv, silent_rv)
        else:
            if cache:
                self._cached_json = (rv, rv)
        return rv

    @property
    def detail(self):
        res = {
            'path': self.path,
            'method': self.method,
            'data': self.data.decode(),
            'query': self.args.to_dict(),
            'address': self.remote_addr
        }
        if self.files:
            res.setdefault('form', dict(self.files))
        return res

    @property
    def remote_addr(self):
        if 'X-Real-Ip' in self.headers:
            return self.headers['X-Real-Ip']
        return super(Request, self).remote_addr


class Flask(_Flask):
    json_encoder = JSONEncoder
    request_class = Request


def register_v1(app):
    v1 = Blueprint(__name__, 'v1', url_prefix='/api/v1')
    v1.add_url_rule('/user/<string:user>', view_func=AUser.as_view('user'))
    v1.add_url_rule('/power/<string:power>', view_func=APowers.as_view('power'))
    v1.add_url_rule("/mould/<string:mould>", view_func=AMoulds.as_view('mould'))
    v1.add_url_rule("/notice/<string:notice>", view_func=ANotice.as_view('notice'))
    # v1.add_url_rule.....
    app.register_blueprint(v1)


def create_app():
    app = Flask(__name__)
    app.config.from_object(DefaltSettig)
    register_v1(app)
    CORS(app, supports_credentials=True)
    request_first_handler(app)
    register_ext(app)
    return app

