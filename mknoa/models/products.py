# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, DECIMAL, DATETIME

from mknoa.common.base_model import Base, Column

class Products(Base):
    """
    商品表
    """
    __tablename__ = "Products"
    sku_id = Column(String(200), primary_key=True)                          # sku_主键
    i_id = Column(String(200), nullable=False)                              # 款式编码
    i_name = Column(Text, nullable=False)                                   # 款式名称
    properties_value = Column(Text)                                         # 颜色及规格
    supplier_id = Column(String(64), nullable=False)                        # 供应商id
    supplier_name = Column(Text, nullable=False)                            # 供应商名称
    brand = Column(Text)                                                    # 品牌

class ProductsQyt(Base):
    """
    商品库存表
    """
    __tablename__ = "ProductsQyt"
    sku_id = Column(String(200), primary_key=True)                          # sku_主键
    qty = Column(Integer, default=0)                                        # 可用库存
    order_lock = Column(Integer, default=0)                                 # 锁仓库存