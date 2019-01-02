# -*- coding: utf-8 -*-
from mknoa.common.base_resource import Resource
from mknoa.control.CApproval import CApproval


class AApproval(Resource):
    def __init__(self):
        self.approval = CApproval()

    def post(self, approval):
        apis = {
            "new_approval": self.approval.new_approval,
            "update_approval": self.approval.update_approval,
            "launch_approval": self.approval.launch_approval,
            "delete_approval": self.approval.delete_approval,
            "approve_approval": self.approval.approve_approval
        }
        return apis

    def get(self, approval):
        apis = {
            "approval_list": self.approval.approval_list,
            "approval_message": self.approval.approval_message,
            "approve_approval_list": self.approval.approve_approval_list,
            "approve_approval_message": self.approval.approve_approval_message,
            "get_my_approval_list": self.approval.get_my_approval_list,
            "get_relaunch_approval": self.approval.get_relaunch_approval,
            "my_approve_approval_list": self.approval.my_approve_approval_list
        }
        return apis