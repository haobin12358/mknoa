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
