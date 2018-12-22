# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CPowers import CPowers


class APowers(Resource):
    def __init__(self):
        self.power = CPowers()

    def post(self, power):
        apis = {
            "new_power": self.power.new_power,
            "update_power_status": self.power.update_power_status,
            "update_power": self.power.update_power
        }
        return apis

    def get(self, power):
        apis = {
            "get_power_list": self.power.get_power_list,
            "get_power_list_easy": self.power.get_power_list_easy
        }
        return apis