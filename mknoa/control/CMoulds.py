from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SMoulds import SMoulds
from mknoa.common.success_response import Success
from mknoa.common.error_response import TokenError, ParamsError, AuthorityError
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.moulds import Moulds, MouldElement, Elements

import uuid, datetime, json

class CMoulds(SMoulds):

    @get_session
    def new_elements(self):
        data = parameter_required(("element_name",))
        new_elements = Elements.create({
            "element_id": str(uuid.uuid1()),
            "element_name": data.get("element_name"),
            "element_createtime": datetime.datetime.now(),
            "element_status": 71
        })
        db.session.add(new_elements)
        return Success("创建元素成功")

    @get_session
    def new_mould(self):
        data = parameter_required(("mould_name", "mould_time", "mould_list"))
        mould_id = str(uuid.uuid1())
        new_mould = Moulds.create({
            "mould_id": mould_id,
            "mould_name": data.get("mould_name"),
            "mould_time": data.get("mould_time"),
            "mould_createtime": datetime.datetime.now(),
            "mould_updatetime": datetime.datetime.now(),
            "mould_status": 61
        })
        db.session.add(new_mould)
        mould_list = data.get("mould_list")
        for mould_element in mould_list:
            if "mouldelement_name" not in mould_element or "mouldelement_index" not in mould_element:
                return ParamsError("参数缺失，请检查mouldelement_name和mouldelement_index合法性")
            if "mouldelement_name" == "表单":
                if "mouldelement_rank" not in mould_element:
                    return ParamsError("参数缺失，请检查表单行列参数合法性")
                else:
                    mouldelement_rank = ""
                    for row in mould_element["mouldelement_rank"]:
                        if mouldelement_rank != "":
                            mouldelement_rank = mouldelement_rank + "#"
                        mouldelement_rank = mouldelement_rank + row
            else:
                mouldelement_rank = None

            if "mouldelement_name" == "文本框":
                if "mouldelement_trans" not in mould_element:
                    return ParamsError("参数缺失，请检查mouldelement_trans合法性")
                else:
                    mouldelement_trans = mould_element["mouldelement_trans"]
            else:
                mouldelement_trans = None
            element_ids = get_model_return_dict(self.get_elementid_by_elementname(mould_element["mouldelement_name"]))
            if not element_ids:
                return ParamsError("参数值有误，请检查mouldelement_name值合法性")
            element_id = element_ids["element_id"]
            new_mould_element = MouldElement.create({
                "mouldelement_id": str(uuid.uuid1()),
                "mould_id": mould_id,
                "element_id": element_id,
                "mouldelement_name": mouldelement_trans,
                "mouldelement_index": mould_element["mouldelement_index"],
                "mouldelement_rank": mouldelement_rank,
                "mouldelement_status": 81,
                "mouldelement_createtime": datetime.datetime.now(),
                "mouldelement_updatetime": datetime.datetime.now()
            })
            db.session.add(new_mould_element)
        return Success("创建模板成功")

    @get_session
    def update_mould(self):
        args = request.args.to_dict()
        if "mould_id" not in args:
            return ParamsError("参数缺失，请检查mould_id合法性")
        data = parameter_required(("mould_name", "mould_time", "mould_list"))
        update_mould = self.s_update_mould(args["mould_id"],
                                           {
                                               "mould_name": data.get("mould_name"),
                                               "mould_time": data.get("mould_time"),
                                               "mould_updatetime": datetime.datetime.now()
                                           })
        mould_element_now = get_model_return_list(self.get_mould_element_by_mouldid(args["mould_id"]))
        for mould_element in mould_element_now:
            delete_mould_element = self.s_update_mouldelement(mould_element["mouldelement_id"],
                                                              {
                                                                  "mouldelement_status": 82
                                                              })
        mould_list = data.get("mould_list")
        for mould_element in mould_list:
            if "mouldelement_name" not in mould_element or "mouldelement_index" not in mould_element:
                return ParamsError("参数缺失，请检查mouldelement_name和mouldelement_index合法性")
            if "mouldelement_name" == "表单":
                if "mouldelement_rank" not in mould_element:
                    return ParamsError("参数缺失，请检查表单行列参数合法性")
                else:
                    mouldelement_rank = ""
                    for row in mould_element["mouldelement_rank"]:
                        if mouldelement_rank != "":
                            mouldelement_rank = mouldelement_rank + "#"
                        mouldelement_rank = mouldelement_rank + row
            else:
                mouldelement_rank = None

            if "mouldelement_name" == "文本框":
                if "mouldelement_trans" not in mould_element:
                    return ParamsError("参数缺失，请检查mouldelement_trans合法性")
                else:
                    mouldelement_trans = mould_element["mouldelement_trans"]
            else:
                mouldelement_trans = None
            element_ids = get_model_return_dict(self.get_elementid_by_elementname(mould_element["mouldelement_name"]))
            if not element_ids:
                return ParamsError("参数值有误，请检查mouldelement_name值合法性")
            element_id = element_ids["element_id"]
            new_mould_element = MouldElement.create({
                "mouldelement_id": str(uuid.uuid1()),
                "mould_id": args["mould_id"],
                "element_id": element_id,
                "mouldelement_name": mouldelement_trans,
                "mouldelement_index": mould_element["mouldelement_index"],
                "mouldelement_rank": mouldelement_rank,
                "mouldelement_status": 81,
                "mouldelement_createtime": datetime.datetime.now(),
                "mouldelement_updatetime": datetime.datetime.now()
            })
            db.session.add(new_mould_element)
        return Success("更新模板成功")

    @get_session
    def delete_mould(self):
        data = json.loads(request.data)
        for mould_id in data:
            update_mould = self.s_update_mould(mould_id,
                                               {
                                                   "mould_status": 62,
                                                   "mould_updatetime": datetime.datetime.now()
                                               })
        return Success("删除模板成功")

    @get_session
    def get_mould_list(self):
        args = request.args.to_dict()
        if "page_num" not in args or "page_size" not in args:
            return ParamsError("参数缺失，请检查page_num和page_size的合法性")
        mould_list = get_model_return_list(self.get_mould_list_by_page(int(args["page_num"]), int(args["page_size"])))
        mould_count = get_model_return_list(self.get_mould_count())
        return {
            "status": 200,
            "message": "获取模板列表成功",
            "data": mould_list,
            "total_count": len(mould_count),
            "total_page": int(len(mould_count) / int(args["page_size"])) + 1
        }

    @get_session
    def get_mould_message(self):
        args = request.args.to_dict()
        if "mould_id" not in args:
            return ParamsError("参数缺失，请检查mould_id的合法性")
        mould_message = get_model_return_dict(self.get_mould_message_by_mouldid(args["mould_id"]))
        mould_elements = get_model_return_list(self.get_mould_element_by_mouldid(args["mould_id"]))
        for element in mould_elements:
            if element["mouldelement_rank"]:
                element["mouldelement_rank"] = element["mouldelement_rank"].split("#")
            element["mouldelement_name_trans"] = get_model_return_dict(self.get_elementname_by_elementid(element["element_id"]))["element_name"]
        mould_message["mould_list"] = mould_elements
        return Success("获取模板信息成功", data=mould_message)