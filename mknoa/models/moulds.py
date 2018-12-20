# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL, DATETIME

from mknoa.common.base_model import Base, Column

class Moulds(Base):
    """
    模板
    """
    mould_id = Column(String(64), primary_key=True)                         # 主键id
    mould_name = Column(Text, nullable=False)                               # 模板名称
    mould_time = Column(Integer, default=0)                                 # 审批时间设定，0为无限制
    mould_createtime = Column(DATETIME, default=datetime.datetime.now())    # 模板创建时间
    mould_updatetime = Column(DATETIME, default=datetime.datetime.now())    # 模板更新时间
    mould_status = Column(Integer, default=61)                              # 模板状态{61可用62不可用}

class Elements(Base):
    """
    元素
    """
    element_id = Column(String(64), primary_key=True)                       # 主键id
    element_name = Column(String(64), nullable=False)                       # 元素名称
    element_code = Column(Integer)                                          # 元素编码
    element_createtime = Column(DATETIME, default=datetime.datetime.now())  # 元素创建时间
    element_status = Column(Integer, default=71)                            # 元素状态{71可用72不可用}

class MouldElement(Base):
    """
    模板内置元素
    """
    mouldelement_id = Column(String(64), primary_key=True)                      # 主键id
    mould_id = Column(String(64), nullable=False)                               # 模板id，关联
    element_id = Column(String(64), nullable=False)                             # 元素id，关联
    mouldelement_name = Column(Text, nullable=False)                            # 用于诠释元素内容代表的含义
    mouldelement_icon_id = Column(String(200), nullable=False)                  # 元素id，前端使用
    mouldelement_index = Column(Integer)                                        # 元素顺序
    mouldelement_rank = Column(String(200))                                     # 行列，*号间隔，列表特有
    mouldelement_status = Column(Integer, default=81)                           # 状态{81可用82不可用}
    mouldelement_createtime = Column(DATETIME, default=datetime.datetime.now()) # 创建时间
    mouldelement_updatetime = Column(DATETIME, default=datetime.datetime.now()) # 更新时间