# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL, DATETIME

from mknoa.common.base_model import Base, Column


class Users(Base):
    """
    用户表
    """
    __tablename__ = "Users"
    user_id = Column(String(64), primary_key=True)                              # 主键id
    user_name = Column(String(128), nullable=False)                             # 用户名
    user_password = Column(String(128), nullable=False)                         # 用户密码
    user_createtime = Column(DATETIME, default=datetime.datetime.now())         # 创建时间
    user_truename = Column(String(128))                                         # 用户真实姓名
    user_telphone = Column(String(20))                                          # 联系方式
    user_email = Column(String(64))                                             # 用户邮箱
    user_wechat = Column(String(64))                                            # 用户微信
    user_qq = Column(String(64))                                                # 用户qq
    user_message = Column(Text)                                                 # 个性签名
    user_status = Column(Integer, nullable=False, default=11)                   # 用户状态{11可用12不可用13冻结}
    user_location = Column(Text)                                                # 用户地址
    user_contract = Column(Text)                                                # 用户合同
    user_icon = Column(Text)                                                    # 用户头像

class Tags(Base):
    """
    身份标签表
    """
    __tablename__ = "Tags"
    tag_id = Column(String(64), primary_key=True)                               # 主键id
    tag_name = Column(String(256), nullable=False)                              # 身份名称
    tag_status = Column(Integer, nullable=False, default=21)                    # 身份状态{21可用22废弃}
    tag_level = Column(Integer, default=1)                                      # 身份等级
    user_id = Column(String(64), nullable=False)                                # 创建人id

class UserTags(Base):
    """
    用户身份关联表
    """
    __tablename__ = "UserTags"
    usertag_id = Column(String(64), primary_key=True)                           # 主键id
    user_id = Column(String(64), nullable=False)                                # 用户id，关联
    tag_id = Column(String(64), nullable=False)                                 # 身份id，关联
    usertag_createtime = Column(DATETIME, default=datetime.datetime.now())      # 创建时间
    usertag_updatetime = Column(DATETIME, default=datetime.datetime.now())      # 更新时间
    usertag_status = Column(Integer, nullable=False, default=31)                # 关联状态{31关联中32关联解除}