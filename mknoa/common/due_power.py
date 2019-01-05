from mknoa.common.token_handler import token_to_usid
from mknoa.common.error_response import UnKnowError, NouseError, AuthorityError
from mknoa.common.get_model_return_list import get_model_return_dict, get_model_return_list
from mknoa.service.SUsers import SUsers
from mknoa.service.SPowers import SPowers
from flask import current_app

def user_can_use(token, power_name):
    power_list = ["index", "user", "mould", "approval", "notice"]
    if power_name not in power_list:
        return UnKnowError("未知权限，后端逻辑异常，请拖走祭天")
    user_id = token_to_usid(token)
    current_app.logger.info("user_id:" + str(user_id))
    user = SUsers()
    user_message = user.get_user_message(user_id)
    if not user_message:
        return NouseError("无此用户")
    tag_id_list = get_model_return_list(user.get_usertagid_by_user(user_id))
    if not tag_id_list and user_id != "1":
        return AuthorityError("无任何权限")
    tag_id_dict = []
    for row in tag_id_list:
        tag_id_dict.append(row["tag_id"])
    current_app.logger.info("tag_id_dict:" + str(tag_id_dict))
    power_id_dict = []
    power = SPowers()
    for tag in tag_id_dict:
        powers = get_model_return_list(power.get_powerid_by_tagid(tag))
        for row in powers:
            if row["power_id"] not in power_id_dict:
                power_id_dict.append(row["power_id"])
    current_app.logger.info("power_id_dict:" + str(power_id_dict))
    power_tree = power_to_tree(power_id_dict)
    tag_list = update_tag_message(tag_id_dict)
    return {
        "tag_dict": tag_id_dict,
        "tag_list": tag_list,
        "power_dict": power_id_dict,
        "power_tree": power_tree,
        "user_id": user_id
    }

def powereasy_to_powerhard(power_list_easy):
    power = SPowers()
    power_id_dict = []
    for power_id in power_list_easy:
        if power_id not in power_id_dict:
            power_id_dict.append(power_id)
        power_parent = get_model_return_dict(power.get_parent_by_powerid(power_id))
        current_app.logger.info("power_parent:" + str(power_parent))
        if "power_parent_id" not in power_parent:
            return None
        if power_parent["power_parent_id"] not in power_id_dict and power_parent["power_parent_id"] != "0":
            power_id_dict.append(power_parent["power_parent_id"])

    return power_id_dict

def tag_can_use(tag_id):
    user = SUsers()
    power = SPowers()
    power_id_dict = []
    power = get_model_return_list(power.get_powerid_by_tagid(tag_id))
    for row in power:
        if row["power_id"] not in power_id_dict:
            power_id_dict.append(row["power_id"])
    tag_message = get_model_return_dict(user.get_tagname_by_tagid(tag_id))
    power_tree = power_to_tree(power_id_dict)
    tag_message["power_list"] = power_tree
    return tag_message

def update_tag_message(tag_dict):
    user = SUsers()
    tag_list = []
    for tag in tag_dict:
        tag_message = get_model_return_dict(user.get_tagname_by_tagid(tag))
        tag_list.append(tag_message)
    return tag_list

def power_to_tree(power_dict):
    power = SPowers()
    parent_dict = []
    power_list = []
    for power_id in power_dict:
        parent = get_model_return_dict(power.get_parent_by_powerid(power_id))
        if not parent or parent["power_parent_id"] != "0":
            pass
        else:
            parent_dict.append(power_id)
    for power_id in parent_dict:
        power_message = get_model_return_dict(power.get_power_by_powerid(power_id))
        if power_message["power_path"] == " ":
            power_message["power_path"] = power_message["power_path"].replace(" ", "")
        if power_message["power_redirect"] == " ":
            power_message["power_redirect"] = power_message["power_redirect"].replace(" ", "")
        power_meta = get_model_return_dict(power.get_meta_by_powerid(power_id))
        power_message["power_meta"] = power_meta
        power_message["children"] = []
        power_children = get_model_return_list(power.get_power_by_parentid(power_id))
        for power_children_message in power_children:
            if power_children_message["power_id"] in power_dict:
                if power_children_message["power_path"] == " ":
                    power_children_message["power_path"] = power_children_message["power_path"].replace(" ", "")
                if power_children_message["power_redirect"] == " ":
                    power_children_message["power_redirect"] = power_children_message["power_redirect"].replace(" ", "")
                power_children_meta = get_model_return_dict(power.get_meta_by_powerid(power_children_message["power_id"]))
                power_children_message["power_meta"] = power_children_meta
                power_message["children"].append(power_children_message)
            else:
                pass
        power_list.append(power_message)
    return power_list