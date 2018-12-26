# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CMoulds import CMoulds


class AMoulds(Resource):
    def __init__(self):
        self.mould = CMoulds()

    def post(self, mould):
        apis = {
            "new_elements": self.mould.new_elements,
            "new_mould": self.mould.new_mould,
            "update_mould": self.mould.update_mould,
            "delete_mould": self.mould.delete_mould
        }
        return apis

    def get(self, mould):
        apis = {
            "get_mould_list": self.mould.get_mould_list,
            "get_mould_message": self.mould.get_mould_message,
            "get_mould_list_choose": self.mould.get_mould_list_choose
        }
        return apis