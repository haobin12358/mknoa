from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SNotice import SNotice
from mknoa.common.success_response import Success
from mknoa.common.error_response import TokenError, ParamsError, AuthorityError
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.notice import Notice

import uuid, datetime, json

class CNotice(SNotice):

    @get_session
    def new_notice(self):
        data = parameter_required(("notice_title", "notice_message"))
        new_notice = Notice.create({
            "notice_id": str(uuid.uuid1()),
            "notice_title": data.get("notice_title"),
            "notice_message": data.get("notice_message"),
            "notice_createtime": datetime.datetime.now(),
            "notice_updatetime": datetime.datetime.now(),
            "notice_status": 141
        })
        db.session.add(new_notice)
        return Success("发布公告成功")

    @get_session
    def update_notice(self):
        data = parameter_required(("notice_title", "notice_message"))
        args = request.args.to_dict()
        if "notice_id" not in args:
            return ParamsError("参数缺失，请检查notice_id合法性")
        update_notice = self.s_update_notice(args["notice_id"],
                                             {
                                                 "notice_title": data.get("notice_title"),
                                                 "notice_message": data.get("notice_message"),
                                                 "notice_updatetime": datetime.datetime.now()
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
        if "page_size" not in args.keys() or "page_num" not in args.keys():
            return ParamsError("参数缺失，请检查page_size和page_num的合法性")
        notice_list = get_model_return_list(self.get_notice_list_by_page(int(args["page_size"]), int(args["page_num"])))
        notice_count = get_model_return_list(self.get_notice_list_count())
        for notice in notice_list:
            notice["notice_updatetime"] = notice["notice_updatetime"].strftime("%Y-%m-%d")
        return {
            "status": 200,
            "message": "获取公告列表成功",
            "data": notice_list,
            "total_count": len(notice_count),
            "total_page": int(len(notice_count) / int(args["page_size"])) + 1
        }

    @get_session
    def get_my_notice(self):
        pass

    @get_session
    def get_notice_message(self):
        args = request.args.to_dict()
        if "notice_id" not in args.keys():
            return ParamsError("参数缺失，请检查notice_id的合法性")
        notice_message = get_model_return_dict(self.get_notice_message_by_noticeid(args["notice_id"]))
        return Success("获取公告详情成功", data=notice_message)