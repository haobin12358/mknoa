from flask import request, current_app
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
            print(approvallevel)
            update_approvalpower = self.s_update_approval_level(approvallevel["approvallevel_id"],
                                                                {
                                                                    "approvallevel_status": 102
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
        data = parameter_required(("approval_name", "approvalmould_list"))
        # 创建发起的审批流主键id
        approvalsub_id = str(uuid.uuid1())

        user_id = token_to_usid(args["token"])
        # TODO 判断是否允许发起

        # 获取用户
        user_message = get_model_return_dict(self.get_user_message(user_id))

        # 获取审批流相关信息
        approval_id = args["approval_id"]
        approval_level_list = get_model_return_list(self.get_approvallevel_by_approvalid(approval_id))
        approval_message = get_model_return_dict(self.get_approval_message_by_approvalid(approval_id))
        mould_id = approval_message["mould_id"]
        mould_message = get_model_return_dict(self.get_mould_message_by_mouldid(mould_id))
        mould_time = int(mould_message["mould_time"])
        if mould_time == 0:
            approvalsov_mouldtime = 0
            mould_time = None
        else:
            approvalsov_mouldtime = mould_time
            pass
        # 优先创建模板关联表数据
        for approval_mould in data.get("approvalmould_list"):
            # 先拿到元素名称和元素顺序
            mouldelement_name_trans = approval_mould["mouldelement_name_trans"]
            mouldelement_index = approval_mould["mouldelement_index"]
            if mouldelement_name_trans == "文本框":
                mouldelement_name = approval_mould["mouldelement_name"]
                element_value = approval_mould["element_value"]
                mouldelement_rank = None
                element_value_name = None
            elif mouldelement_name_trans == "表格":
                mouldelement_name = None
                element_value_name = None
                mouldelement_rank = ""
                for row in approval_mould["mouldelement_rank"]:
                    if mouldelement_rank != "":
                        mouldelement_rank = mouldelement_rank + "#"
                    mouldelement_rank = mouldelement_rank + row
                rank_dict = []
                for rank_left in approval_mould["element_value"]:
                    rank_right_string = ""
                    for rank_right in rank_left:
                        if rank_right_string != "":
                            rank_right_string = rank_right_string + "#"
                        if rank_right == "":
                            rank_right = "&"
                        rank_right_string = rank_right_string + rank_right
                    rank_dict.append(rank_right_string)
                rank_string = ""
                for rank_left in rank_dict:
                    if rank_string != "":
                        rank_string = rank_string + "*"
                    if rank_left == "":
                        rank_left = "&"
                    rank_string = rank_string + rank_left
                element_value = rank_string
            elif mouldelement_name_trans == "图片":
                mouldelement_name = None
                element_value = ""
                element_value_name = None
                mouldelement_rank = None
                for row in approval_mould["element_value"]:
                    if element_value != "":
                        element_value = element_value + "#"
                    element_value = element_value + row
            else:
                mouldelement_name = None
                element_value = ""
                element_value_name = ""
                mouldelement_rank = None
                for row in approval_mould["element_value"]:
                    if element_value != "":
                        element_value = element_value + "#"
                    element_value = element_value + row["url"]
                    if element_value_name != "":
                        element_value_name = element_value_name + "#"
                    element_value_name = element_value_name + row["name"]


            new_approvalmould = ApprovalMould.create({
                "approvalmould_id": str(uuid.uuid1()),
                "element_name": mouldelement_name_trans,
                "mouldelement_name": mouldelement_name,
                "mouldelement_index": mouldelement_index,
                "element_value": element_value,
                "element_value_name": element_value_name,
                "mouldelement_rank": mouldelement_rank,
                "approvalsub_id": approvalsub_id
            })
            db.session.add(new_approvalmould)

        # 创建主审批流数据
        new_approvalsub = ApprovalSub.create({
            "approvalsub_id": approvalsub_id,
            "approval_name": data.get("approval_name"),
            "approvalsub_createtime": datetime.datetime.now(),
            "approvalsub_status": 121,
            "user_id": user_id,
            "user_truename": user_message["user_name"],
            "user_telphone": user_message["user_telphone"],
            "approvalsub_endtime": datetime.datetime.now() + datetime.timedelta(days=mould_time),
            "approval_id": args["approval_id"],
            "approvalsub_num": len(approval_level_list)
        })
        db.session.add(new_approvalsub)

        i = 0
        while i < len(approval_level_list):
            approvalsov_id = str(uuid.uuid1())
            if i == 0:
                approvalsov_suggestion = 131
                approvalsov_first_id = approvalsov_id
                time_continue = int(approvalsov_mouldtime) * 86400
                time_expires = time_continue * (len(approval_level_list))
                # 创建时给第一层审批添加异步处理
                from mknoa.extensions.tasks import auto_agree_task
                auto_agree_task.apply_async(args=[approvalsov_first_id], countdown=approvalsov_mouldtime,
                                            expires=time_expires, )
            else:
                approvalsov_suggestion = 134
            new_approvalsov = ApprovalSov.create({
                "approvalsov_id": approvalsov_id,
                "approvalsov_suggestion": approvalsov_suggestion,
                "approvalsov_message": None,
                "approvalsov_createtime": None,
                "user_truename": None,
                "approvalsub_id": approvalsub_id,
                "approvalsub_index": 0,
                "tag_id": approval_level_list[i]["tag_id"],
                "approvalsov_mouldtime": approvalsov_mouldtime
            })
            db.session.add(new_approvalsov)
            i = i + 1

        return Success("发起审批流成功")

    @get_session
    def delete_approval(self):
        data = parameter_required(("approval_list", ))
        for approval_id in data.get("approval_list"):
            update_approval = self.s_update_approval(approval_id,
                                                     {
                                                         "approval_status": 92,
                                                         "approval_updatetime": datetime.datetime.now()
                                                     })
        return Success("删除审批流成功")

    @get_session
    def get_relaunch_approval(self):
        args = request.args.to_dict()
        if "approval_id" not in args:
            return ParamsError("参数缺失，请检查approval_id合法性")

        approval_message = get_model_return_dict(self.get_approval_message_by_approvalid(args["approval_id"]))
        mould_id = approval_message["mould_id"]
        mould_message = get_model_return_dict(self.get_mould_message_by_mouldid(mould_id))
        mould_elements = get_model_return_list(self.get_mould_element_by_mouldid(mould_id))
        for element in mould_elements:
            if element["mouldelement_rank"]:
                element["mouldelement_rank"] = element["mouldelement_rank"].split("#")
            element["mouldelement_name_trans"] = \
                get_model_return_dict(self.get_elementname_by_elementid(element["element_id"]))["element_name"]

            if element["mouldelement_name_trans"] == "图片" or element["mouldelement_name_trans"] == "文件":
                element_value = []
            elif element["mouldelement_name_trans"] == "文本框":
                element_value = ""
            elif element["mouldelement_name_trans"] == "表格":
                a = []
                while len(a) < int(element["mouldelement_rank"][1]):
                    a.append("")
                element_value = []
                while len(element_value) < int(element["mouldelement_rank"][0]):
                    element_value.append(a)
            else:
                element_value = ""
            element["element_value"] = element_value

        mould_message["mould_list"] = mould_elements
        approval_message["mould_message"] = mould_message

        return Success("获取审批流样式成功", data=approval_message)

    @get_session
    def approve_approval(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        token = args["token"]
        user_id = token_to_usid(token)
        if "approvalsub_id" not in args:
            return ParamsError("参数缺失，请检查approvalsub_id合法性")
        approvalsub_id = args["approvalsub_id"]
        data = json.loads(request.data)
        if "approvalsov_suggestion" not in data:
            return ParamsError("参数缺失，请检查approvalsov_suggestion合法性")
        if data["approvalsov_suggestion"] == "通过":
            approvalsov_suggestion = 132
        else:
            approvalsov_suggestion = 133
        if "approvalsov_message" not in data:
            approvalsov_message = None
        else:
            approvalsov_message = data["approvalsov_message"]

        user = get_model_return_dict(self.get_username_by_userid(user_id))
        user_name = user["user_name"]
        self.deal(approvalsub_id, user_name, approvalsov_suggestion, approvalsov_message)

        return Success("审批成功")

    @get_session
    def approval_list(self):
        args = request.args.to_dict()
        if "page_num" not in args.keys() or "page_size" not in args.keys():
            return ParamsError("参数缺失，请检查page_num和page_size的合法性")
        approval_list = get_model_return_list(self.get_approval_list_by_page(int(args["page_num"]), int(args["page_size"])))
        for approval in approval_list:
            approval_level_list = get_model_return_list(self.get_approvallevel_by_approvalid(approval["approval_id"]))
            if len(approval_level_list) > 1:
                approval["approval_level"] = "是"
            elif len(approval_level_list) == 1:
                approval["approval_level"] = "否"
            else:
                approval["approval_level"] = "异常状态"
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
        print(approval_power_list)
        approval_list_id = []
        for approval_power in approval_power_list:
            approval_list_id.append(approval_power["tag_id"])
        approval_message["approval_level_list"] = approval_level_list
        approval_message["approval_power_list"] = approval_list_id

        return Success("获取审批流详情成功", data=approval_message)

    @get_session
    def my_approve_approval_list(self):
        args = request.args.to_dict()

        if "token" not in args:
            return TokenError("未登录")
        token = args["token"]
        if "approvalsov_suggestion" not in args:
            return ParamsError("参数缺失，请检查approvalsov_suggestion合法性")
        if "page_size" not in args or "page_num" not in args:
            return ParamsError("参数缺失，请检查页码参数合法性")
        user_id = token_to_usid(token)
        approvalsub_list = get_model_return_list(self.get_approvalsub_by_userid_status(user_id, args["approvalsov_suggestion"]))

        for approval in approvalsub_list:
            approval["approvalsub_createtime"] = approval["approvalsub_createtime"].strftime("%Y-%m-%d %H:%M:%S")
            approval["approvalsub_endtime"] = approval["approvalsub_endtime"].strftime("%Y-%m-%d %H:%M:%S")
            approval["approvalsub_status"] = self.due_approval(approval["approvalsub_status"])
        total_count = len(approvalsub_list)
        total_page = int(total_count / int(args["page_size"])) + 1
        page_start = int(args["page_size"]) * (int(args["page_num"]) - 1)
        page_end = int(args["page_size"]) * int(args["page_num"])
        approvalsub_list = approvalsub_list[page_start:page_end]

        return {
            "status": 200,
            "message": "获取我发起的审批流列表成功",
            "data": approvalsub_list,
            "total_count": total_count,
            "total_page": total_page
        }

    @get_session
    def approve_approval_list(self):
        args = request.args.to_dict()

        if "token" not in args:
            return TokenError("未登录")
        token = args["token"]
        if "approvalsov_suggestion" not in args:
            return ParamsError("参数缺失，请检查approvalsov_suggestion合法性")
        if "page_size" not in args or "page_num" not in args:
            return ParamsError("参数缺失，请检查页码参数合法性")
        user_id = token_to_usid(token)
        tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
        tag_list = []
        for tag_id in tag_ids:
            tag_list.append(tag_id["tag_id"])
        current_app.logger.info("tag_list:" + str(tag_list))
        approval_sov = []
        for tag in tag_list:
            approval_sov = get_model_return_list(self.get_approvalsov_by_tagid_status(tag, args["approvalsov_suggestion"])) + approval_sov
        page_start = int(args["page_size"]) * (int(args["page_num"]) - 1)
        page_end = int(args["page_size"]) * int(args["page_num"])
        total_count = len(approval_sov)
        total_page = int(total_count / int(args["page_size"])) + 1
        approval_sov = approval_sov[page_start: page_end]

        for approval in approval_sov:
            approvalsub_id = approval["approvalsub_id"]
            approvalsub_message = get_model_return_dict(self.get_approvalsub_by_subid(approvalsub_id))
            approvalsub_message["approvalsub_createtime"] = approvalsub_message["approvalsub_createtime"].strftime("%Y-%m-%d %H:%M:%S")
            approvalsub_message["approvalsub_endtime"] = approvalsub_message["approvalsub_endtime"].strftime("%Y-%m-%d %H:%M:%S")
            approvalsub_message["approvalsub_status"] = self.due_approval(approvalsub_message["approvalsub_status"])
            approval.update(approvalsub_message)

        return {
            "status": 200,
            "message": "获取收到的审批流列表成功",
            "data": approval_sov,
            "total_count": total_count,
            "total_page": total_page
        }

    def due_approval(self, approvalsub_status):
        if approvalsub_status == 121:
            return "审批中"
        elif approvalsub_status == 122:
            return "审批通过"
        elif approvalsub_status == 123:
            return "已驳回"
        else:
            return "未知状态"

    def due_approvalsov(self, approvalsov_suggestion):
        if approvalsov_suggestion == 131:
            return "待审批"
        elif approvalsov_suggestion == 132:
            return "审批通过"
        elif approvalsov_suggestion == 133:
            return "已驳回"
        elif approvalsov_suggestion == 134:
            return "上级未审批"
        else:
            return "未知状态"

    @get_session
    def approve_approval_message(self):
        args = request.args.to_dict()

        if "token" not in args:
            return TokenError("未登录")
        token = args["token"]
        user_id = token_to_usid(token)
        # 判断当前用户是否可以审批
        tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
        tag_list = []
        for tag_id in tag_ids:
            tag_list.append(tag_id["tag_id"])

        if "approvalsub_id" not in args:
            return ParamsError("参数缺失，请检查approvalsub_id合法性")
        approvalsub_id = args["approvalsub_id"]
        # 根据sub id找到131状态的审批流对应的tag id
        tag_id_sql = get_model_return_dict(self.get_tagid_by_approvalsub_suggestion(approvalsub_id))

        approvalsub_message = get_model_return_dict(self.get_approvalsub_message_by_subid(approvalsub_id))
        if "tag_id" not in tag_id_sql or tag_id_sql["tag_id"] not in tag_list:
            approvalsub_message["is_approval"] = 162
        else:
            approvalsub_message["is_approval"] = 161
        approvalsub_list = get_model_return_list(self.get_approval_message(approvalsub_id))
        for approvalsub in approvalsub_list:
            if approvalsub["element_name"] == "图片":
                approvalsub["element_value"] = approvalsub["element_value"].split("#")
            elif approvalsub["element_name"] == "文件":
                approvalsub["element_value"] = approvalsub["element_value"].split("#")
                approvalsub["element_value_name"] = approvalsub["element_value_name"].split("#")
                approvalsub_value_list = []
                i = 0
                while i < len(approvalsub["element_value"]):
                    approvalsub_value_dict = {}
                    approvalsub_value_dict["url"] = approvalsub["element_value"][i]
                    approvalsub_value_dict["name"] = approvalsub["element_value_name"][i]
                    approvalsub_value_list.append(approvalsub_value_dict)
                    i = i + 1
                approvalsub["element_value"] = approvalsub_value_list
            elif approvalsub["element_name"] == "表格":
                approvalsub["mouldelement_rank"] = approvalsub["mouldelement_rank"].split("#")
                approvalsub["element_value"] = approvalsub["element_value"].split("*")
                approvalsub_test_list = []
                for element_value in approvalsub["element_value"]:
                    element_value = element_value.split("#")
                    approvalsub_test_list.append(element_value)
                approvalsub["element_value"] = approvalsub_test_list
                i = 0
                while i < int(approvalsub["mouldelement_rank"][0]):
                    j = 0
                    while j < int(approvalsub["mouldelement_rank"][1]):
                        if approvalsub["element_value"][i][j] == "&":
                            approvalsub["element_value"][i][j] = ""
                        j = j + 1
                    i = i + 1

        approvalsov_list = get_model_return_list(self.get_approvalsov_message_by_subid(approvalsub_id))
        for approvalsov in approvalsov_list:
            tag_message = get_model_return_dict(self.get_tagname_by_tagid(approvalsov["tag_id"]))
            approvalsov["tag_name"] = tag_message["tag_name"]
            approvalsov["approvalsov_suggestion"] = self.due_approvalsov(approvalsov["approvalsov_suggestion"])
        response = {}
        response["approvalsub_message"] = approvalsub_message
        response["approvalsub_list"] = approvalsub_list
        response["approvalsov_list"] = approvalsov_list

        return Success("获取审批流信息成功", data=response)

    @get_session
    def get_my_approval_list(self):
        args = request.args.to_dict()

        if "token" not in args:
            return TokenError("未登录")
        token = args["token"]
        user_id = token_to_usid(token)
        print(user_id)
        tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
        print(tag_ids)
        tag_list = []
        for tag_id in tag_ids:
            tag_list.append(tag_id["tag_id"])

        # 完成身份list的创建
        approval_list = get_model_return_list(self.get_approval_list_by_none())
        print(approval_list)
        approval_list_return = []
        for approval in approval_list:
            tag_power = get_model_return_list(self.get_approvalpower_by_approvalid(approval["approval_id"]))
            for tag in tag_power:
                if tag["tag_id"] in tag_list:
                    approval_list_return.append(approval)

        return Success("获取可创建审批流成功", data=approval_list_return)

    def deal(self, approvalsub_id, user_name, approvalsov_suggestion, approvalsov_message):
        from mknoa.extensions.tasks import auto_agree_task
        approvalsov = get_model_return_dict(self.get_approvalsov_now_by_subid(approvalsub_id))
        index = int(approvalsov["approvalsub_index"])
        approvalsov_id = approvalsov["approvalsov_id"]


        # 更新当前的审批情况
        update_approvalsov = self.s_update_approvalsov(approvalsov_id,
                                                       {
                                                           "approvalsov_suggestion": approvalsov_suggestion,
                                                           "approvalsov_message": approvalsov_message,
                                                           "approvalsov_createtime": datetime.datetime.now(),
                                                           "user_truename": user_name
                                                       })
        if approvalsov_suggestion == 132:
            # 如果审批通过，查找下一级的审批
            approvalsov_next = get_model_return_dict(self.get_approvalsov_now_by_subid_index(approvalsub_id, index + 1))
            if not approvalsov_next:
                """
                没有下一级
                """
                update_approvalsub = self.s_update_approvalsub(approvalsub_id,
                                                               {
                                                                   "approvalsub_status": 122
                                                               })
            else:
                """
                有下一级
                """
                approvalsov_next_id = approvalsov_next["approvalsov_id"]
                update_approvalsov = self.s_update_approvalsov(approvalsov_next_id,
                                                               {
                                                                   "approvalsov_suggestion": 131
                                                               })
                # todo 增加异步处理
                approvalsub = ApprovalSub.query.filter_by_(approvalsub_id=approvalsub_id).first()
                time_continue = int(approvalsov_next['approvalsov_mouldtime']) * 86400
                time_expires = time_continue * (approvalsub.approvalsub_num - approvalsov_next['approvalsub_index'])
                auto_agree_task.apply_async(args=[approvalsov_next_id], countdown=time_continue, expires=time_expires,)

        elif approvalsov_suggestion == 133:
            update_approvalsub = self.s_update_approvalsub(approvalsub_id,
                                                           {
                                                               "approvalsub_status": 123
                                                           })