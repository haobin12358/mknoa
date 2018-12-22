from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SPowers import SPowers
from mknoa.service.SUsers import SUsers
from mknoa.common.success_response import Success
from mknoa.common.error_response import TokenError, ParamsError, AuthorityError
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.power import PowerTag, Powers, PowersMeta

import uuid, datetime, json

class CPowers(SPowers, SUsers):

    @get_session
    def new_power(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        # 限制只有上帝才能new complation power
        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        if user_name != "admin":
            return AuthorityError("无权限")
        data = parameter_required(("power_parent_id", "power_path", "power_meta", "power_name"))
        power_id = str(uuid.uuid1())
        new_power = Powers.create({
            "power_id": power_id,
            "power_path": data.get("power_path"),
            "power_redirect": data.get("power_redirect"),
            "power_status": 41,
            "power_parent_id": data.get("power_parent_id"),
            "power_component": data.get("power_component"),
            "power_createtime": datetime.datetime.now(),
            "power_updatetime": datetime.datetime.now(),
            "power_name": data.get("power_name")
        })
        db.session.add(new_power)
        power_meta = data.get("power_meta")
        if "powermeta_icon" not in power_meta.keys():
            power_meta["powermeta_icon"] = None
        if "powermeta_roles" not in power_meta.keys():
            powermeta_roles = None
        else:
            powermeta_roles = ""
            for row in power_meta["powermeta_roles"]:
                if powermeta_roles != "":
                    powermeta_roles = powermeta_roles + "#"
                powermeta_roles = powermeta_roles + row
        new_powermeta = PowersMeta.create({
            "powermeta_id": str(uuid.uuid1()),
            "powermeta_title": data.get("power_meta")["powermeta_title"],
            "powermeta_roles": powermeta_roles,
            "powermeta_icon": power_meta["powermeta_icon"],
            "power_id": power_id
        })
        db.session.add(new_powermeta)

        return Success("新增权限成功")

    @get_session
    def get_power_list(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        if user_name == "admin":
            power_list = get_model_return_list(self.get_parent_power_admin())
            for power in power_list:
                power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                power["power_meta"] = power_meta
                children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                for children in children_list:
                    children_meta = get_model_return_dict(self.get_meta_by_powerid(children["power_id"]))
                    children["power_meta"] = children_meta
                power["children"] = children_list
            return Success("获取上帝权限成功", data=power_list)

        else:
            tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
            power_list = []
            for tag in tag_ids:
                tag_id = tag["tag_id"]
                # 根据标签id获取了所有的权限id，这里的权限id中存在子权限id
                power_id_list = get_model_return_list(self.get_powerid_by_tagid(tag_id))
                power_id_dict = []
                for power in power_id_list:
                    power_id_dict.append(power["power_id"])
                for power in power_id_list:
                    power_id = power["power_id"]
                    power_message = get_model_return_dict(self.get_power_by_powerid(power_id))
                    # 判断，如果是根节点，那么处理，如果不是根节点，那么放弃
                    if power_message["power_parent_id"] == "0":
                        power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                        power_message["power_meta"] = power_meta
                        # 根据刚才的权限id获取子权限列表，子权限列表中可能有部分子权限是无权限的
                        children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                        i = len(children_list)
                        # 循环处理字权限列表数据，如果子权限列表中存在无权限的内容，则remove处理
                        while i > 0:
                            if children_list[i - 1]["power_id"] in power_id_dict:
                                children_meta = get_model_return_dict(self.get_meta_by_powerid(children_list[i - 1]["power_id"]))
                                children_list[i - 1]["power_meta"] = children_meta
                            else:
                                children_list.remove(children_list[i - 1])
                            i = i - 1
                        power_message["children"] = children_list
                        power_list.append(power_message)
                    else:
                        pass
            return Success("获取用户权限成功", data=power_list)

    @get_session
    def get_power_list_easy(self):
        """
        创建/更新身份时使用
        :return:
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        if user_name == "admin":
            # 上帝永远是对的
            power_list = get_model_return_list(self.get_parent_power_admin())
            power_dict = []
            for power in power_list:
                power_message = {}
                power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                power["power_meta"] = power_meta
                power_message["power_id"] = power["power_id"]
                power_message["power_title"] = power_meta["powermeta_title"]
                children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                children_dict = []
                for children in children_list:
                    children_message = {}
                    children_meta = get_model_return_dict(self.get_meta_by_powerid(children["power_id"]))
                    children["power_meta"] = children_meta
                    children_message["power_id"] = children["power_id"]
                    children_message["power_title"] = children_meta["powermeta_title"]
                    children_dict.append(children_message)
                power_message["children"] = children_dict
                power_dict.append(power_message)
            return Success("获取上帝权限成功", data=power_dict)

        else:
            tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
            power_list = []
            for tag in tag_ids:
                tag_id = tag["tag_id"]
                # 根据标签id获取了所有的权限id，这里的权限id中存在子权限id
                power_id_list = get_model_return_list(self.get_powerid_by_tagid(tag_id))
                power_id_dict = []
                for power in power_id_list:
                    power_id_dict.append(power["power_id"])
                power_dict = []
                for power in power_id_list:
                    power_id = power["power_id"]
                    power_message_list = {}
                    power_message = get_model_return_dict(self.get_power_by_powerid(power_id))
                    # 判断，如果是根节点，那么处理，如果不是根节点，那么放弃
                    if power_message["power_parent_id"] == "0":
                        power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                        # 把根节点的power_title和power_id给出
                        power_message_list["power_title"] = power_meta["powermeta_title"]
                        power_message_list["power_id"] = power["power_id"]
                        # 根据刚才的权限id获取子权限列表，子权限列表中可能有部分子权限是无权限的
                        children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                        i = len(children_list)
                        # 循环处理字权限列表数据，如果子权限列表中存在无权限的内容，则remove处理
                        children_list_dict = []
                        while i > 0:
                            children_title_id = {}
                            if children_list[i - 1]["power_id"] in power_id_dict:
                                children_meta = get_model_return_dict(
                                    self.get_meta_by_powerid(children_list[i - 1]["power_id"]))
                                children_list[i - 1]["power_meta"] = children_meta
                                # 放置children的power_id和power_title
                                children_title_id["power_id"] = children_list[i - 1]["power_id"]
                                children_title_id["power_title"] = children_meta["powermeta_title"]
                                children_list_dict.append(children_title_id)
                            else:
                                children_list.remove(children_list[i - 1])
                            i = i - 1
                        power_message_list["children"] = children_list_dict
                        power_dict.append(power_message_list)
                    else:
                        pass
            return Success("获取用户权限成功", data=power_dict)

    @get_session
    def update_power(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        if "power_id" not in args.keys():
            return ParamsError("缺失参数power_id")
        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        if user_name != "admin":
            return AuthorityError("无权限")

        data = parameter_required(("power_parent_id", "power_path", "power_meta"))
        new_power = self.update_spower(args["power_id"], {
            "power_path": data.get("power_path"),
            "power_redirect": data.get("power_redirect"),
            "power_parent_id": data.get("power_parent_id"),
            "power_component": data.get("power_component"),
            "power_updatetime": datetime.datetime.now()
        })
        power_meta = data.get("power_meta")
        if "powermeta_icon" not in power_meta.keys():
            power_meta["powermeta_icon"] = None
        if "powermeta_roles" not in power_meta.keys():
            powermeta_roles = None
        else:
            powermeta_roles = ""
            for row in power_meta["powermeta_roles"]:
                if powermeta_roles != "":
                    powermeta_roles = powermeta_roles + "#"
                powermeta_roles = powermeta_roles + row
        new_powermeta = self.update_spowermeta(args["power_id"], {
            "powermeta_title": data.get("power_meta")["powermeta_title"],
            "powermeta_roles": powermeta_roles,
            "powermeta_icon": power_meta["powermeta_icon"],
            "power_id": args["power_id"]
        })

        return Success("更新权限成功")

    @get_session
    def update_power_status(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        if user_name != "admin":
            return AuthorityError("无权限")
        data = json.loads(request.data)
        for row in data:
            if "power_status" not in row.keys() or "power_id" not in row.keys():
                return ParamsError("参数缺失")
            else:
                update_power = self.update_spower(row["power_id"],
                                                  {
                                                      "power_status": row["power_status"]
                                                  })
        return Success("更新权限成功")