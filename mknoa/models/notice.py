# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL

from mknoa.common.base_model import Base, Column

class Notice(Base):
    """
    公告
    """
    __tablename__ = "Notice"
    notice_id = Column(String(64), primary_key=True)                # 主键id
    notice_title = Column(Text, nullable=False)                     # 公告标题
    notice_message = Column(Text)                                   # 公告内容
    notice_createtime = Column(DateTime, datetime.datetime.now())   # 创建时间
    notice_updatetime = Column(DateTime, datetime.datetime.now())   # 更新时间
    notice_status = Column(Integer, default=141)                    # 公告状态{141可读142已删}