# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL, DATETIME

from mknoa.common.base_model import Base, Column

class Powers(Base):
    """
    权限名称
    """
    __tablename__ = "Powers"
    power_id = Column(String(64), primary_key=True)                 # 主键id
    power_status = Column(Integer, default=41)                      # 权限状态{41可用42禁用43权限冻结}
    power_path = Column(String(200))                                # 控件路径
    power_component = Column(String(200))                           # 控件样式
    power_redirect = Column(Text)                                   # 存储路径
    power_parent_id = Column(String(64))                            # 父权限
    power_createtime = Column(DATETIME)                             # 创建时间
    power_updatetime = Column(DATETIME)                             # 更新时间
    power_name = Column(String(200))                                # 名称
    power_hidden = Column(Boolean)                                  # 是否隐藏

class PowersMeta(Base):
    """
    权限的meta
    """
    __tablename__ = "PowersMeta"
    powermeta_id = Column(String(64), primary_key=True)             # 主键id
    powermeta_title = Column(String(128), nullable=False)           # 标题名称
    power_id = Column(String(64), nullable=False)                   # 权限id，关联
    powermeta_icon = Column(String(64))                             # 图标
    powermeta_roles = Column(String(128))                           # 格式为["a","b"]，存储为"a#b"

class PowerTag(Base):
    """
    权限身份关联表
    """
    __tablename__ = "PowerTag"
    powertag_id = Column(String(64), primary_key=True)                          # 主键id
    power_id = Column(String(64), nullable=False)                               # 权限id，关联
    tag_id = Column(String(64), nullable=False)                                 # 身份id，关联
    powertag_createtime = Column(DATETIME, default=datetime.datetime.now())     # 创建时间
    powertag_updatetime = Column(DATETIME, default=datetime.datetime.now())     # 更新时间
    powertag_status = Column(Integer, default=51)                               # 状态{51可用52不可用}