from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SApproval import SApproval
from mknoa.service.SMoulds import SMoulds
from mknoa.service.SUsers import SUsers
from mknoa.common.success_response import Success
from mknoa.common.error_response import TokenError, ParamsError, AuthorityError
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.approval import ApprovalLevel, ApprovalMould, Approvals, ApprovalSov, ApprovalPower, ApprovalSub

import uuid, datetime, json

class CApproval(SApproval, SMoulds, SUsers):

    @get_session
    def new_approval(self):
        data = parameter_required(("approval_name", "mould_id", "approval_level_list", "approval_power_list"))
        approval_level_list = data.get("approval_level_list")
        approval_id = str(uuid.uuid1())
        for approval_level in approval_level_list:
            if "tag_id" not in approval_level.keys() or "approvallevel_index" not in approval_level.keys():
                return ParamsError("参数缺失，请检查tag_id和approvallevel_index的合法性")
            new_approvallevel = ApprovalLevel.create({
                "approvallevel_id": str(uuid.uuid1()),
                "approvallevel_status": 101,
                "approvallevel_index": approval_level["approvallevel_index"],
                "approval_id": approval_id,
                "tag_id": approval_level["tag_id"]
            })
            db.session.add(new_approvallevel)
        for approval_power in data.get("approval_power_list"):
            new_approvalpower = ApprovalPower.create({
                "approvalpower_id": str(uuid.uuid1()),
                "approvalpower_status": 111,
                "approvalpower_createtime": datetime.datetime.now(),
                "approvalpower_updatetime": datetime.datetime.now(),
                "tag_id": approval_power,
                "approval_id": approval_id
            })
            db.session.add(new_approvalpower)
        new_approval = Approvals.create({
            "approval_id": approval_id,
            "approval_name": data.get("approval_name"),
            "mould_id": data.get("mould_id"),
            "approval_status": 91,
            "approval_createtime": datetime.datetime.now(),
            "approval_updatetime": datetime.datetime.now()
        })
        db.session.add(new_approval)
        return Success("创建审批流成功")

    @get_session
    def update_approval(self):
        data = parameter_required(("approval_name", "mould_id", "approval_level_list", "approval_power_list"))
        args = request.args.to_dict()
        if "approval_id" not in args:
            return ParamsError("参数缺失，请检查approval_id合法性")

        approvallevel_list = get_model_return_list(self.get_approvallevelid_by_approvalid(args["approval_id"]))
        for approvallevel in approvallevel_list:
            update_approvalpower = self.s_update_approval_power(approvallevel["approvallevel_id"],
                                                                {
                                                                    "approvalpower_status": 102,
                                                                    "approvalpower_updatetime": datetime.datetime.now()
                                                                })

        approval_level_list = data.get("approval_level_list")
        for approval_level in approval_level_list:
            if "tag_id" not in approval_level.keys() or "approvallevel_index" not in approval_level.keys():
                return ParamsError("参数缺失，请检查tag_id和approvallevel_index的合法性")
            new_approvallevel = ApprovalLevel.create({
                "approvallevel_id": str(uuid.uuid1()),
                "approvallevel_status": 101,
                "approvallevel_index": approval_level["approvallevel_index"],
                "approval_id": args["approval_id"],
                "tag_id": approval_level["tag_id"]
            })
            db.session.add(new_approvallevel)

        approvalpower_list = get_model_return_list(self.get_approvalpowerid_by_approvalid(args["approval_id"]))
        for approvalpower in approvalpower_list:
            update_approvalpower = self.s_update_approval_power(approvalpower["approvalpower_id"],
                                                                {
                                                                    "approvalpower_status": 112,
                                                                    "approvalpower_updatetime": datetime.datetime.now()
                                                                })

        for approval_power in data.get("approval_power_list"):
            new_approvalpower = ApprovalPower.create({
                "approvalpower_id": str(uuid.uuid1()),
                "approvalpower_status": 111,
                "approvalpower_createtime": datetime.datetime.now(),
                "approvalpower_updatetime": datetime.datetime.now(),
                "tag_id": approval_power,
                "approval_id": args["approval_id"]
            })
            db.session.add(new_approvalpower)

        update_approval = self.s_update_approval(args["approval_id"],
                                                 {
                                                     "approval_name": data.get("approval_name"),
                                                     "mould_id": data.get("mould_id"),
                                                     "approval_updatetime": datetime.datetime.now()
                                                 })
        return Success("更新审批流成功")

    @get_session
    def launch_approval(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        if "approval_id" not in args.keys():
            return ParamsError("参数缺失，请查看approval_id的合法性")

        pass

    @get_session
    def delete_approval(self):
        data = json.loads(request.data)
        for approval_id in data:
            update_approval = self.s_update_approval(approval_id,
                                                     {
                                                         "approval_status": 92,
                                                         "approval_updatetime": datetime.datetime.now()
                                                     })
        return Success("删除审批流成功")

    @get_session
    def approve_approval(self):
        pass

    @get_session
    def approval_list(self):
        args = request.args.to_dict()
        if "page_num" not in args.keys() or "page_size" not in args.keys():
            return ParamsError("参数缺失，请检查page_num和page_size的合法性")
        approval_list = get_model_return_list(self.get_approval_list_by_page(int(args["page_num"]), int(args["page_size"])))
        approval_count = get_model_return_list(self.get_approval_list_count())
        return {
            "status": 200,
            "message": "获取审批流列表成功",
            "data": approval_list,
            "total_count": len(approval_count),
            "total_page": int(len(approval_count) / int(args["page_size"])) + 1
        }

    @get_session
    def approval_message(self):
        args = request.args.to_dict()
        if "approval_id" not in args.keys():
            return ParamsError("参数缺失， 请检查approval_id的合法性")
        approval_message = get_model_return_dict(self.get_approval_message_by_approvalid(args["approval_id"]))
        mould_message = get_model_return_dict(self.get_mould_message_by_mouldid(approval_message["mould_id"]))
        approval_message["mould_name"] = mould_message["mould_name"]

        approval_level_list = get_model_return_list(self.get_approvallevel_by_approvalid(args["approval_id"]))
        for approval_level in approval_level_list:
            tag_name = get_model_return_dict(self.get_tagname_by_tagid(approval_level["tag_id"]))["tag_name"]
            approval_level["tag_name"] = tag_name
        approval_power_list = get_model_return_list(self.get_approvalpower_by_approvalid(args["approval_id"]))
        for approval_power in approval_power_list:
            tag_name = get_model_return_dict(self.get_tagname_by_tagid(approval_power["tag_id"]))["tag_name"]
            approval_power["tag_name"] = tag_name
        approval_message["approval_level_list"] = approval_level_list
        approval_message["approval_power_list"] = approval_power_list

        return Success("获取审批流详情成功", data=approval_message)

    @get_session
    def approve_approval_list(self):
        pass

    @get_session
    def approve_approval_message(self):
        pass