# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL

from mknoa.common.base_model import Base, Column

class Powers(Base):
    """
    权限名称
    """
    __tablename__ = "Powers"
    power_id = Column(String(64), primary_key=True)                 # 主键id
    power_name = Column(Text)                                       # 板块名称
    power_status = Column(Integer, default=41)                      # 权限状态{41可用42禁用43权限冻结}
    power_icon_id = Column(String(200))                             # 控件id
    power_use_js = Column(String(200))                              # 控件js
    power_createtime = Column(DateTime)                             # 创建时间
    power_updatetime = Column(DateTime)                             # 更新时间

class PowerTag(Base):
    """
    权限身份关联表
    """
    __tablename__ = "PowerTag"
    powertag_id = Column(String(64), primary_key=True)                          # 主键id
    power_id = Column(String(64), nullable=False)                               # 权限id，关联
    tag_id = Column(String(64), nullable=False)                                 # 身份id，关联
    powertag_createtime = Column(DateTime, default=datetime.datetime.now())     # 创建时间
    powertag_updatetime = Column(DateTime, default=datetime.datetime.now())     # 更新时间
    powertag_status = Column(Integer, default=51)                               # 状态{51可用52不可用}