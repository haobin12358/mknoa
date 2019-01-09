from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SNotice import SNotice
from mknoa.service.SApproval import SApproval
from mknoa.common.success_response import Success
from mknoa.service.SUsers import SUsers
from mknoa.service.SMoulds import SMoulds
from mknoa.common.error_response import TokenError, ParamsError, AuthorityError
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.notice import Notice
from mknoa.common.due_power import user_can_use

import uuid, datetime, json

class CNotice(SNotice, SApproval, SUsers, SMoulds):

    @get_session
    def new_notice(self):
        data = json.loads(request.data)
        if "notice_title" not in data:
            return ParamsError("请填写标题")
        if "notice_message" not in data:
            return ParamsError("请填写内容")
        if "tag_list" in data and data["tag_list"]:
            tag_list = data["tag_list"]
            tag = ""
            for row in tag_list:
                if tag != "":
                    tag = tag + "#"
                tag = tag + row
        else:
            tag = None
        if "user_list" in data and data["user_list"]:
            user_list = data["user_list"]
            user = ""
            for row in user_list:
                if user != "":
                    user = user + "#"
                user = user + row
        else:
            user = None

        new_notice = Notice.create({
            "notice_id": str(uuid.uuid1()),
            "notice_title": data["notice_title"],
            "notice_message": data["notice_message"],
            "notice_createtime": datetime.datetime.now(),
            "notice_updatetime": datetime.datetime.now(),
            "notice_status": 141,
            "tag_id": tag,
            "user_id": user
        })
        db.session.add(new_notice)
        return Success("发布公告成功")

    @get_session
    def update_notice(self):
        data = json.loads(request.data)
        if "notice_title" not in data:
            return ParamsError("请填写标题")
        if "notice_message" not in data:
            return ParamsError("请填写内容")
        if "tag_list" in data and data["tag_list"]:
            tag_list = data["tag_list"]
            tag = ""
            for row in tag_list:
                if tag != "":
                    tag = tag + "#"
                tag = tag + row
        else:
            tag = None
        if "user_list" in data and data["user_list"]:
            user_list = data["user_list"]
            user = ""
            for row in user_list:
                if user != "":
                    user = user + "#"
                user = user + row
        else:
            user = None
        args = request.args.to_dict()
        if "notice_id" not in args:
            return ParamsError("参数缺失，请检查notice_id合法性")
        update_notice = self.s_update_notice(args["notice_id"],
                                             {
                                                 "notice_title": data.get("notice_title"),
                                                 "notice_message": data.get("notice_message"),
                                                 "notice_updatetime": datetime.datetime.now(),
                                                 "tag_id": tag,
                                                 "user_id": user
                                             })
        return Success("更新公告成功")

    @get_session
    def delete_notice(self):
        data = parameter_required(("notice_list", ))
        for notice_id in data.get("notice_list"):
            update_notice = self.s_update_notice(notice_id,
                                                 {
                                                     "notice_status": 142,
                                                     "notice_updatetime": datetime.datetime.now()
                                                 })
        return Success("删除公告成功")

    @get_session
    def get_notice_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        user_tree = user_can_use(args["token"], "notice")
        user_id = user_tree["user_id"]
        if "page_size" not in args or "page_num" not in args:
            return ParamsError("参数异常，请检查page_size和page_num合法性")
        page_size = int(args["page_size"])
        page_num = int(args["page_num"])
        if user_id != "1":
            tag_list = user_tree["tag_dict"]
            notice_list = []
            notice_id_list = []
            for tag in tag_list:
                notice_message = get_model_return_list(self.get_notice_list_three_item(user_id, tag))
                for row in notice_message:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
                notice_message_public = get_model_return_list(self.get_notice_list_by_none())
                for row in notice_message_public:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
            total_count = len(notice_list)
            total_page = int(total_count / page_size) + 1
            notice_list = notice_list[(page_num - 1) * page_size: page_num * page_size]
            return {
                "status": 200,
                "message": "获取公告列表成功",
                "total_page": total_page,
                "total_count": total_count,
                "notice_list": notice_list
            }
        else:
            notice_message_public = get_model_return_list(self.get_notice_list_by_none())
            total_count = len(notice_message_public)
            total_page = int(total_count / page_size) + 1
            notice_list = notice_message_public[(page_num - 1) * page_size: page_num * page_size]
            return {
                "status": 200,
                "message": "获取公告列表成功",
                "total_page": total_page,
                "total_count": total_count,
                "notice_list": notice_list
            }

    @get_session
    def get_my_notice(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        user_tree = user_can_use(args["token"], "notice")
        user_id = user_tree["user_id"]
        if "page_size" not in args or "page_num" not in args:
            return ParamsError("参数异常，请检查page_size和page_num合法性")
        page_size = int(args["page_size"])
        page_num = int(args["page_num"])
        if user_id != "1":
            tag_list = user_tree["tag_dict"]
            notice_list = []
            notice_id_list = []
            for tag in tag_list:
                notice_message = get_model_return_list(self.get_notice_list_three_item(user_id, tag))
                for row in notice_message:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
                notice_message_public = get_model_return_list(self.get_notice_list_by_none())
                for row in notice_message_public:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
            total_count = len(notice_list)
            total_page = int(total_count / page_size) + 1
            notice_list = notice_list[(page_num - 1) * page_size: page_num * page_size]
            return {
                "status": 200,
                "message": "获取公告列表成功",
                "total_page": total_page,
                "total_count": total_count,
                "notice_list": notice_list
            }
        else:
            notice_message_public = get_model_return_list(self.get_notice_list_by_none())
            total_count = len(notice_message_public)
            total_page = int(total_count / page_size) + 1
            notice_list = notice_message_public[(page_num - 1) * page_size: page_num * page_size]
            return {
                "status": 200,
                "message": "获取公告列表成功",
                "total_page": total_page,
                "total_count": total_count,
                "notice_list": notice_list
            }

    @get_session
    def get_notice_message(self):
        args = request.args.to_dict()
        if "notice_id" not in args.keys():
            return ParamsError("参数缺失，请检查notice_id的合法性")
        notice_message = get_model_return_dict(self.get_notice_message_by_noticeid(args["notice_id"]))
        if notice_message["user_id"]:
            notice_message["user_list"] = notice_message["user_id"].split("#")
            del (notice_message["user_id"])
        else:
            notice_message["user_list"] = ""
            del (notice_message["user_id"])
        if notice_message["tag_id"]:
            notice_message["tag_list"] = notice_message["tag_id"].split("#")
            del(notice_message["tag_id"])
        else:
            notice_message["tag_list"] = ""
            del (notice_message["tag_id"])
        return Success("获取公告详情成功", data=notice_message)

    @get_session
    def get_index_message(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        user_tree = user_can_use(args["token"], "notice")
        user_id = user_tree["user_id"]
        if user_id != "1":
            # 我发起的待审核
            len_wait_my_suggest = len(get_model_return_list(self.get_approvalsub_by_userid_status(user_id, "未审批")))
            # 我发起的已审核
            len_sov_my_suggest = len(get_model_return_list(self.get_approvalsub_by_userid_status(user_id, "已审批")))
            tag_list = user_tree["tag_dict"]
            wait_my_resove_suggest = []
            sov_my_resove_suggest = []
            notice_list = []
            notice_id_list = []
            for tag in tag_list:
                wait_my_resove_suggest = get_model_return_list(self.get_approvalsov_by_tagid_status(tag, "未审批")) + wait_my_resove_suggest
                sov_my_resove_suggest = get_model_return_list(self.get_approvalsov_by_tagid_status(tag, "已审批")) + sov_my_resove_suggest
                notice_message = get_model_return_list(self.get_notice_list_three_item(user_id, tag))
                for row in notice_message:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
                notice_message_public = get_model_return_list(self.get_notice_list_by_none())
                for row in notice_message_public:
                    if row["notice_id"] not in notice_id_list:
                        notice_id_list.append(row["notice_id"])
                        notice_list.append(row)
            # 我收到的待审核
            len_wait_my_resove_suggest = len(wait_my_resove_suggest)
            # 我收到的已审核
            len_sov_my_resove_suggest = len(sov_my_resove_suggest)

            # 身份数目
            len_tag_list = len(get_model_return_list(self.get_taglist_count(user_id)))
            # 通知
            notice_list = notice_list[0:3]
            response = {}
            response["len_wait_my_suggest"] = len_wait_my_suggest
            response["len_sov_my_suggest"] = len_sov_my_suggest
            response["len_wait_my_resove_suggest"] = len_wait_my_resove_suggest
            response["len_sov_my_resove_suggest"] = len_sov_my_resove_suggest
            response["len_tag_list"] = len_tag_list
            response["notice_list"] = notice_list
            return Success("获取用户首页成功", data=response)
        else:
            # 身份数目
            len_tag_list = len(get_model_return_list(self.get_taglist_count(user_id)))
            # 账号数目
            len_user_list = len(get_model_return_list(self.get_userlist()))
            # 公告列表
            notice_message_public = get_model_return_list(self.get_notice_list_by_none())
            notice_message_public = notice_message_public[0:2]
            # 模板列表
            mould_list = get_model_return_list(self.get_mould_count())
            mould_list = mould_list[0:9]
            # 审批流列表
            approval_list = get_model_return_list(self.get_approval_list_count())
            for approval in approval_list:
                approval_level_list = get_model_return_list(
                    self.get_approvallevel_by_approvalid(approval["approval_id"]))
                if len(approval_level_list) > 1:
                    approval["approval_level"] = "已设置多级审批"
                elif len(approval_level_list) == 1:
                    approval["approval_level"] = "未设置多级审批"
                else:
                    approval["approval_level"] = "异常状态"
            approval_list = approval_list[0:6]
            response = {}
            response["len_tag_list"] = len_tag_list
            response["len_user_list"] = len_user_list
            response["notice_message_public"] = notice_message_public
            response["mould_list"] = mould_list
            response["approval_list"] = approval_list

            return Success("获取超级管理员首页成功", data=response)

    @get_session
    def send_message(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        data = json.loads(request.data)
        if "telphone" not in data:
            return ParamsError("请输入手机号")
        if "message" not in data:
            return ParamsError("请输入要发送的内容")
        user = get_model_return_dict(self.get_user_by_usertelphone(data["telphone"]))
        if user:
            user_id = user["user_id"]
            new_notice = Notice.create({
                "notice_id": str(uuid.uuid1()),
                "notice_title": "通知",
                "notice_message": data["message"],
                "notice_createtime": datetime.datetime.now(),
                "notice_updatetime": datetime.datetime.now(),
                "notice_status": 141,
                "user_id": user_id
            })
            db.session.add(new_notice)

        else:
            pass
        # TODO 短信通知
        return Success("发送成功")