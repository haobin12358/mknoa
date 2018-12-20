# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CUsers import CUsers


class AUser(Resource):
    def __init__(self):
        self.user = CUsers()

    def post(self, user):
        apis = {
            "login": self.user.login,
        }
        return apis

    def get(self, user):
        apis = {


        }
        return apis