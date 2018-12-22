# -*-coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
import datetime, base64
from .error_response import AuthorityError, TokenError


def usid_to_token(id):
    """生成令牌
    id: 用户id
    model: 用户类型(User 或者 Admin, Supplizer)
    expiration: 过期时间, 在config/secret中修改
    """
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token_with_base = id + "#" + time_now
    token_with_base = token_with_base.encode(encoding="utf-8")
    token_with_base = base64.b64encode(token_with_base)
    token_with_base = token_with_base.decode()
    return token_with_base

def token_to_usid(token):
    token_without_base = base64.b64decode(token)
    token_without_base = token_without_base.decode()
    usid_time = token_without_base.split("#")
    return usid_time[0]

def is_admin():
    """是否是管理员"""
    return hasattr(request, 'user') and request.user.model == 'Admin'


def is_supplizer():
    return hasattr(request, 'user') and request.user.model == 'Supplizer'


def is_tourist():
    """是否是游客"""
    return not hasattr(request, 'user')


def common_user():
    """是否是普通用户, 不包括管理员"""
    return hasattr(request, 'user') and request.user.model == 'User'


def is_shop_keeper():
    """是否是店主 todo"""
    return common_user() and request.user.level == 2


def is_hign_level_admin():
    """超级管理员"""
    return is_admin() and request.user.level == 1


def admin_required(func):
    def inner(self, *args, **kwargs):
        if not is_admin():
            raise AuthorityError()
        return func(self, *args, **kwargs)
    return inner


def token_required(func):
    def inner(self, *args, **kwargs):
        if not is_tourist():
            return func(self, *args, **kwargs)
        raise TokenError()
    return inner








