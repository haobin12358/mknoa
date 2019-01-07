# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CUsers import CUsers


class AUser(Resource):
    def __init__(self):
        self.user = CUsers()

    def post(self, user):
        apis = {
            "login": self.user.login,
            "new_tags": self.user.new_tags,
            "update_tag": self.user.update_tag,
            "delete_tag": self.user.delete_tag,
            "new_user": self.user.new_user,
            "update_user_info": self.user.update_user_info,
            "update_password": self.user.update_password
        }
        return apis

    def get(self, user):
        apis = {
            "get_user_tag_level_list": self.user.get_user_tag_level_list,
            "get_tag_list": self.user.get_tag_list,
            "get_tag_message": self.user.get_tag_message,
            "get_my_message": self.user.get_my_message,
            "get_all_user": self.user.get_all_user,
            "get_tags_all": self.user.get_tags_all,
            "get_all_user_easy": self.user.get_all_user_easy
        }
        return apis