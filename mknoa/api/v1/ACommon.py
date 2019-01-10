# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CCommon import CCommon


class ACommon(Resource):
    def __init__(self):
        self.common = CCommon()

    def post(self, common):
        apis = {
            "upload_files": self.common.upload_files
        }
        return apis

    def get(self, common):
        apis = {
            "get_product_list": self.common.get_product_list,
            "get_qyt_list": self.common.get_qyt_list,
            "get_file": self.common.get_file
        }
        return apis
