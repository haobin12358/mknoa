from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SUsers import SUsers
from mknoa.service.SPowers import SPowers
from mknoa.common.success_response import Success
from mknoa.common.error_response import LoginError, NouseError, ColduseError, UnuseError, TokenError, ParamsError, \
    AuthorityError, RepeatError, TagLevelError, UnKnowError
from mknoa.common.due_power import user_can_use, tag_can_use, update_tag_message, power_to_tree, powereasy_to_powerhard
from mknoa.common.token_handler import usid_to_token, token_to_usid
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.extensions.register_ext import db
from mknoa.models.user import Tags, Users, UserTags
from mknoa.models.power import PowerTag, Powers, PowersMeta

import uuid, datetime, json

class CUsers(SUsers, SPowers):

    @get_session
    def login(self):
        """
        登录
        权限：user
        :return: 用户token/用户信息/用户身份/用户权限
        """
        data = parameter_required(('user_name', 'user_password'))
        user_name = data.get("user_name")
        user_password = self.get_password_by_name(user_name)
        if not user_password:
            return NouseError("无此用户")
        if user_password.user_password != data.get("user_password"):
            return LoginError("密码错误")
        else:
            user_id = get_model_return_dict(self.get_userid_by_name(user_name))["user_id"]
            token = usid_to_token(user_id)
            # token已经创建
            # 下文获取用户message
            user_message = get_model_return_dict(self.get_user_message(user_id))
            if user_message["user_status"] == 12:
                return UnuseError("用户不可用")
            elif user_message["user_status"] == 13:
                return ColduseError("账号已冻结，请联系管理员")
            user_message["user_createtime"] = user_message["user_createtime"].strftime("%Y-%m-%d %H:%M:%S")
            tag_list = []
            # 上帝有所有权限，没有任何身份标签
            if user_name == "admin":
                power_list = get_model_return_list(self.get_parent_power_admin())
                for power in power_list:
                    if power["power_path"] == " ":
                        power["power_path"] = power["power_path"].replace(" ", "")
                    if power["power_redirect"] == " ":
                        power["power_redirect"] = power["power_redirect"].replace(" ", "")
                    power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                    power["power_meta"] = power_meta
                    children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                    for children in children_list:
                        children_meta = get_model_return_dict(self.get_meta_by_powerid(children["power_id"]))
                        children["power_meta"] = children_meta
                    power["children"] = children_list

            else:
                # 下文获取用户的权限列表和tag列表
                tree = user_can_use(token, "user")
                if "status" not in tree:
                    power_list = tree["power_tree"]
                    tag_list = tree["tag_list"]
                else:
                    return tree
            return Success('登录成功',
                           data={
                               'token': token,
                               'power_list': power_list,
                               'user_message': user_message,
                               'user_tags': tag_list
                           })

    @get_session
    def new_tags(self):
        """
        新增用户标签
        权限user
        :return:
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]
        data = parameter_required(("tag_name", "tag_level", "tag_power_list"))
        tag_list = tree["tag_list"]
        for tag in tag_list:
            if tag["tag_level"] >= int(data.get("tag_level")):
                return TagLevelError("请创建比自己权限等级低的身份")
        tag_id = str(uuid.uuid1())
        tag = Tags.create({
            "tag_id": tag_id,
            "tag_name": data.get("tag_name"),
            "tag_level": data.get("tag_level"),
            "user_id": user_id,
            "tag_status": 21
        })
        db.session.add(tag)
        tag_power_list = data.get("tag_power_list")
        tag_power_list_hard = powereasy_to_powerhard(tag_power_list)
        if not tag_power_list_hard:
            return UnKnowError("未知权限，请后端核查")
        for power_id in tag_power_list_hard:
            new_powertag = PowerTag.create({
                "powertag_id": str(uuid.uuid1()),
                "power_id" : power_id,
                "tag_id": tag_id,
                "powertag_createtime": datetime.datetime.now(),
                "powertag_updatetime": datetime.datetime.now(),
                "powertag_status": 51
            })
            db.session.add(new_powertag)
        return Success('添加身份标签成功')

    @get_session
    def update_tag(self):
        """
        更新用户标签
        :return:
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]

        if "tag_id" not in args.keys():
            return ParamsError("参数缺失tag_id")
        sql_user_id = get_model_return_dict(self.get_userid_by_tagid(args["tag_id"]))["user_id"]
        # 判断是否是这个人创建的标签，and 上帝做一切事情都是对的
        if user_id != sql_user_id and user_id != "1":
            return AuthorityError("无权限， 请联系创建该身份的该用户或者超级管理员")

        data = parameter_required(("tag_name", "tag_level", "tag_power_list"))
        update_tags = self.s_update_tag(args["tag_id"],
                                        {
                                            "tag_name": data.get("tag_name"),
                                            "tag_level": data.get("tag_level")
                                        })

        # 清理无效权限
        tag_power_list = data.get("tag_power_list")
        tag_power_list_hard = powereasy_to_powerhard(tag_power_list)
        if not tag_power_list_hard:
            return UnKnowError("未知权限，请后端核查")

        # 先清理掉该身份下的所有权限
        powertag_list = get_model_return_list(self.get_tagpowerid_by_tagid(args["tag_id"]))
        for powertag in powertag_list:
            update_powertag = self.s_update_tagpower(powertag["powertag_id"],
                                                     {
                                                         "powertag_status": 52
                                                     })
        for power_id in tag_power_list_hard:
            new_powertag = PowerTag.create({
                "powertag_id": str(uuid.uuid1()),
                "power_id": power_id,
                "tag_id": args["tag_id"],
                "powertag_createtime": datetime.datetime.now(),
                "powertag_updatetime": datetime.datetime.now(),
                "powertag_status": 51
            })
            db.session.add(new_powertag)
        return Success('更新身份标签成功')

    @get_session
    def delete_tag(self):
        """
        删除用户标签，支持批量
        :return:
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]

        data = parameter_required(("tag_ids", ))
        for tag_id in data.get("tag_ids"):
            sql_user_id = get_model_return_dict(self.get_userid_by_tagid(tag_id))["user_id"]
            # 判断是否是这个人创建的标签，and 上帝做一切事情都是对的
            if user_id != sql_user_id and user_id != "1":
                return AuthorityError("无权限， 请联系创建该身份的该用户或者超级管理员")
            update_tag = self.s_update_tag(tag_id,
                                           {
                                               "tag_status": 22
                                           })
        return Success("成功删除身份标签")

    def _get_high_tag_level(self, user_id):
        """
        获取用户最高等级
        :param user_id: 用户id
        :return:
        """
        tags_list = get_model_return_list(self.get_usertagid_by_user(user_id))
        print(tags_list)
        tag_level_high = 7
        for tag in tags_list:
            tag_id = tag["tag_id"]
            print(tag_id)
            tag_level = get_model_return_dict(self.get_taglevel_by_tagid(tag_id))
            print(tag_level)
            tag_level = tag_level["tag_level"]
            if tag_level < tag_level_high:
                tag_level_high = tag_level
        return tag_level_high

    def _get_tag_high(self):
        """
        获取用户最低等级
        :return:
        """
        tags_list = get_model_return_list(self.get_all_taglevel())
        tag_level_low = 1
        for tag in tags_list:
            tag_level = tag["tag_level"]
            if tag_level > tag_level_low:
                tag_level_low = tag_level

        return tag_level_low

    def get_user_tag_level_list(self):
        """
        获取用户等级列表
        :return: 用户等级list
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]

        user_name = get_model_return_dict(self.get_username_by_userid(user_id))["user_name"]
        tag_level_list = []
        if user_name != "admin":
            tag_level_high = self._get_high_tag_level(user_id)
        else:
            tag_level_high = 1
        while tag_level_high < 8:
            tag_level_list.append(tag_level_high)
            tag_level_high = tag_level_high + 1
        return Success("获取身份等级列表成功", data={
            "tag_level_list": tag_level_list
        })

    def get_tag_list(self):
        """
        获取标签列表
        :return: 标签列表，涵盖id/等级/名称/权限
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        if "page_size" not in args.keys() or "page_num" not in args.keys():
            return ParamsError("参数缺失，请检查page_size和page_num有效性")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]

        tag_list = get_model_return_list(self.get_taglist_by_userid(int(args["page_num"]), int(args["page_size"]), user_id))
        tag_dict = []
        for tag in tag_list:
            tag_id = tag["tag_id"]
            tag_easy = tag_can_use(tag_id)
            tag_dict.append(tag_easy)

        page_count = len(get_model_return_list(self.get_taglist_count(user_id)))

        return {
            "status": 200,
            "message": "获取标签列表成功",
            "data": tag_dict,
            "total_count": page_count,
            "total_page": int(page_count / int(args["page_size"])) + 1
        }

    def get_tag_message(self):
        """
        获取标签详情
        :return: 标签列表，涵盖id/等级/名称/权限
        """
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        if "tag_id" not in args.keys():
            return ParamsError("参数缺失，请检查tag_id有效性")
        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]
        sql_user_id = get_model_return_dict(self.get_userid_by_tagid(args["tag_id"]))["user_id"]
        # 判断是否是这个人创建的标签，and 上帝做一切事情都是对的
        if user_id != sql_user_id and user_id != "1":
            return AuthorityError("无权限， 请联系创建该身份的该用户或者超级管理员")
        tag_id = args["tag_id"]

        # 先把该标签已有的权限获取出来，用于标记当前已有权限状态
        power_ids = get_model_return_list(self.get_powerid_by_tagid(tag_id))
        power_id_dict = []
        for row in power_ids:
            power_id_dict.append(row["power_id"])
        # 获取当前用户可以add的所有权限，然后在每个权限上标记是否已选
        power_dict = []
        if user_id == "1":
            # 上帝永远是对的
            power_list = get_model_return_list(self.get_parent_power_admin())
            for power in power_list:
                power_message = {}
                power_meta = get_model_return_dict(self.get_meta_by_powerid(power["power_id"]))
                power["power_meta"] = power_meta
                power_message["power_id"] = power["power_id"]
                if power["power_id"] in power_id_dict:
                    power_message["power_status"] = 5
                else:
                    power_message["power_status"] = 8
                power_message["power_title"] = power_meta["powermeta_title"]
                children_list = get_model_return_list(self.get_power_by_parentid(power["power_id"]))
                children_dict = []
                for children in children_list:
                    children_message = {}
                    children_meta = get_model_return_dict(self.get_meta_by_powerid(children["power_id"]))
                    children["power_meta"] = children_meta
                    children_message["power_id"] = children["power_id"]
                    if children["power_id"] in power_id_dict:
                        children_message["power_status"] = 5
                    else:
                        children_message["power_status"] = 8
                    children_message["power_title"] = children_meta["powermeta_title"]
                    children_dict.append(children_message)
                power_message["children"] = children_dict
                power_dict.append(power_message)
        else:
            tag_ids = get_model_return_list(self.get_usertagid_by_user(user_id))
            for tag in tag_ids:
                tag_id = tag["tag_id"]
                # 根据标签id获取了所有的权限id，这里的权限id中存在子权限id
                power_id_list = get_model_return_list(self.get_powerid_by_tagid(tag_id))
                power_id_dict = []
                for power in power_id_list:
                    power_id_dict.append(power["power_id"])

                # 去重
                power_id_dict = powereasy_to_powerhard(power_id_dict)
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
                        if power["power_id"] in power_id_dict:
                            power_message_list["power_status"] = 5
                        else:
                            power_message_list["power_status"] = 8
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
                                if children_list[i - 1]["power_id"] in power_id_dict:
                                    children_title_id["power_status"] = 5
                                else:
                                    children_title_id["power_status"] = 8
                                children_list_dict.append(children_title_id)
                            else:
                                children_list.remove(children_list[i - 1])
                            i = i - 1
                        power_message_list["children"] = children_list_dict
                        power_dict.append(power_message_list)
                    else:
                        pass
        tag_message = get_model_return_dict(self.get_tagname_by_tagid(tag_id))
        tag_message["power_list"] = power_dict

        return Success("获取标签列表成功", data=tag_message)

    @get_session
    def new_user(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")

        tree = user_can_use(args["token"], "user")
        if "status" in tree:
            return tree
        user_id = tree["user_id"]
        level_high = self._get_high_tag_level(user_id)

        # TODO 判断其他用户是否可以创建
        if user_id != "1" or int(level_high) != 1:
            return AuthorityError("无权限")
        data = parameter_required(("user_name", "user_password", "user_telphone", "user_tags", "user_message"))
        sql_user_id = get_model_return_dict(self.get_userid_by_name(data.get("user_name")))
        if sql_user_id:
            return RepeatError("用户名重复")
        user_id_new = str(uuid.uuid1())
        new_user = Users.create({
            "user_id": user_id_new,
            "user_name": data.get("user_name"),
            "user_password": data.get("user_password"),
            "user_telphone": data.get("user_telphone"),
            "user_status": 11,
            "user_message": data.get("user_message"),
            "user_createtime": datetime.datetime.now()
        })
        db.session.add(new_user)
        user_tags = data.get("user_tags")
        # TODO tag_id 验证
        for tag_id in user_tags:
            new_usertag = UserTags.create({
                "usertag_id": str(uuid.uuid1()),
                "user_id": user_id_new,
                "tag_id": tag_id,
                "usertag_createtime": datetime.datetime.now(),
                "usertag_updatetime": datetime.datetime.now(),
                "usertag_status": 31
            })
            db.session.add(new_usertag)

        return Success("创建用户成功")

    @get_session
    def get_my_message(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        # TODO 判断其他用户是否可以查看用户列表
        if "user_id" not in args.keys():
            return ParamsError("参数缺失,user_id")
        user_message = get_model_return_dict(self.get_user_message(args["user_id"]))
        user_message["user_password"] = "**********"
        user_tags = get_model_return_list(self.get_usertagid_by_user(args["user_id"]))
        tag_list = []
        for tag in user_tags:
            tag_list.append(tag["tag_id"])
        user_message["tag_list"] = tag_list
        return Success("获取用户信息成功", data=user_message)

    @get_session
    def get_all_user(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        # TODO 判断其他用户是否可以查看用户列表
        if user_id != "1":
            return AuthorityError("无权限")
        if "page_size" not in args.keys() or "page_num" not in args.keys():
            return ParamsError("参数缺失，请检查page_size和page_num有效性")

        user_list = get_model_return_list(self.get_userlist_page(int(args["page_num"]), int(args["page_size"])))
        for user in user_list:
            user_level = self._get_high_tag_level(user["user_id"])
            user["user_level"] = user_level
        page_count = len(get_model_return_list(self.get_userlist()))

        return {
            "status": 200,
            "message": "获取标签列表成功",
            "data": user_list,
            "total_count": page_count,
            "total_page": int(page_count / int(args["page_size"])) + 1
        }

    @get_session
    def get_tags_all(self):
        all_tags = get_model_return_list(self.get_all_tag_by_none())
        return Success("获取身份下拉列表成功", data=all_tags)

    @get_session
    def update_password(self):
        args = request.args.to_dict()
        if "token" not in args.keys():
            return TokenError("未登录")
        user_id = token_to_usid(args["token"])
        data = json.loads(request.data)
        if "user_password" not in data:
            return ParamsError("请输入新密码")
        if "user_password_old" not in data:
            return ParamsError("请输入旧密码")
        user_password = get_model_return_dict(self.get_user_message(user_id))
        if not user_password or not user_password["user_password"]:
            return NouseError("无此用户")
        if user_password["user_password"] != data["user_password"]:
            return LoginError("密码错误")
        updata_user = self.s_update_user(user_id,
                                         {
                                             "user_password": data["user_password"]
                                         })
        return Success("修改密码成功")

    @get_session
    def update_user_info(self):
        args = request.args.to_dict()
        if "user_id" not in args:
            return ParamsError("参数缺失，请检查user_id的合法性")

        data = parameter_required(("user_name", "user_password", "user_telphone", "user_tags", "user_message"))
        if data.get("user_password").replace("*", "") == "":
            update_user = self.s_update_user(args["user_id"],
                                             {
                                                 "user_name": data.get("user_name"),
                                                 "user_telphone": data.get("user_telphone"),
                                                 "user_message": data.get("user_message")
                                             })
        else:
            update_user = self.s_update_user(args["user_id"],
                                             {
                                                 "user_name": data.get("user_name"),
                                                 "user_telphone": data.get("user_telphone"),
                                                 "user_message": data.get("user_message"),
                                                 "user_password": data.get("user_password")
                                             })
        user_tag = get_model_return_list(self.get_usertagid_by_userid(args["user_id"]))
        for tag_ids in user_tag:
            print(tag_ids)
            update_usertag = self.s_update_usertag(tag_ids["usertag_id"],
                                                   {
                                                       "usertag_status": 32,
                                                       "usertag_updatetime": datetime.datetime.now()
                                                   })
        for tag_dict in data.get("user_tags"):
            new_usertag = UserTags.create({
                "usertag_id": str(uuid.uuid1()),
                "user_id": args["user_id"],
                "tag_id": tag_dict,
                "usertag_createtime": datetime.datetime.now(),
                "usertag_updatetime": datetime.datetime.now(),
                "usertag_status": 31
            })
        return Success("更新用户成功")