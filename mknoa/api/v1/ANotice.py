# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CNotice import CNotice


class ANotice(Resource):
    def __init__(self):
        self.notice = CNotice()

    def post(self, notice):
        apis = {
            "new_notice": self.notice.new_notice,
            "update_notice": self.notice.update_notice,
            "delete_notice": self.notice.delete_notice
        }
        return apis

    def get(self, notice):
        apis = {
            "get_notice_list": self.notice.get_notice_list,
            "get_my_notice": self.notice.get_my_notice,
            "get_notice_message": self.notice.get_notice_message,
            "get_index_message": self.notice.get_index_message
        }
        return apis