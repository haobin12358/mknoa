# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL, DATETIME

from mknoa.common.base_model import Base, Column

class Approvals(Base):
    """
    审批流实体
    """
    __tablename__ = "Approvals"
    approval_id = Column(String(64), primary_key=True)                          # 主键id
    approval_name = Column(Text, nullable=False)                                # 审批流名称
    mould_id = Column(String(64), nullable=False)                               # 模板id，关联
    approval_status = Column(Integer, default=91)                               # 状态{91可用92不可用}
    approval_createtime = Column(DATETIME, default=datetime.datetime.now())     # 创建时间
    approval_updatetime = Column(DATETIME, default=datetime.datetime.now())     # 更新时间

class ApprovalLevel(Base):
    """
    审批流身份层级
    """
    __tablename__ = "ApprovalLevel"
    approvallevel_id = Column(String(64), primary_key=True)                     # 主键id
    approvallevel_status = Column(Integer, default=101)                         # 状态{101可用102不可用}
    approvallevel_index = Column(Integer, default=1)                            # 审批等级
    approval_id = Column(String(64), nullable=False)                            # 审批流实体id，关联
    tag_id = Column(String(64), nullable=False)                                 # 身份id，关联

class ApprovalPower(Base):
    """
    发起审批流权限
    """
    __tablename__ = "ApprovalPower"
    approvalpower_id = Column(String(64), primary_key=True)                     # 主键id
    approvalpower_status = Column(Integer, default=111)                         # 状态{111可用112不可用}
    approvalpower_createtime = Column(DATETIME, default=datetime.datetime.now())# 创建时间
    approvalpower_updatetime = Column(DATETIME, default=datetime.datetime.now())# 更新时间
    tag_id = Column(String(64), nullable=False)                                 # 身份id，关联
    approval_id = Column(String(64), nullable=False)                            # 审批流实体id，关联

class ApprovalSub(Base):
    """
    发起的审批流
    """
    __tablename__ = "ApprovalSub"
    approvalsub_id = Column(String(64), primary_key=True)                       # 主键id
    approval_name = Column(Text, nullable=False)                                # 审批流名称
    approvalsub_createtime = Column(DATETIME, default=datetime.datetime.now())  # 发起审批时间
    approvalsub_status = Column(Integer, default=121)                           # 审批状态{121审批中122审批通过123已驳回}
    user_truename = Column(Text, nullable=False)                                # 发起者名称
    user_id = Column(String(64), nullable=False)                                # 用户id
    user_telphone = Column(String(64), nullable=False)                          # 用户联系方式
    approvalsub_endtime = Column(DATETIME)                                      # 审批截止时间
    approvalsub_message = Column(Text)                                          # 审批备注
    approval_id = Column(String(64), nullable=False)                            # 审批流实体id
    approvalsub_num = Column(Integer, nullable=False)                           # 审批流总等级数目

class ApprovalMould(Base):
    """
    审批流页签样式与内容
    """
    __tablename__ = "ApprovalMould"
    approvalmould_id = Column(String(64), primary_key=True)                     # 主键id
    element_name = Column(String(64), nullable=False)                           # 元素名称
    mouldelement_name = Column(Text, nullable=False)                            # 元素释义
    mouldelement_index = Column(Integer)                                        # 顺序
    element_value = Column(Text)                                                # 填写内容
    mouldelement_rank = Column(String(200))                                     # 表格行列，*间隔
    approvalsub_id = Column(String(64), nullable=False)                         # 发起的审批流id，关联

class ApprovalSov(Base):
    """
    审批流审批情况
    """
    __tablename__ = "ApprovalSov"
    approvalsov_id = Column(String(64), primary_key=True)                       # 主键id
    approvalsov_suggestion = Column(Integer, nullable=False)                    # 审批结果{131通过132驳回,133待审批}
    approvalsov_message = Column(Text)                                          # 审批意见详情
    approvalsov_createtime = Column(DATETIME, default=datetime.datetime.now())  # 审批时间
    user_truename = Column(String(128), nullable=False)                         # 审批人名称
    approvalsub_id = Column(String(64), nullable=False)                         # 发起的审批流id
    approvalsub_index = Column(Integer)                                         # 审批顺序编号