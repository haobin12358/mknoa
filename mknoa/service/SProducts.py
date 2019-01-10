from mknoa.common.base_service import SBase
from mknoa.models.products import Products

class SProducts(SBase):

    def get_product(self, sku_id):
        return self.session.query(Products.sku_id).filter_by(sku_id=sku_id).first()

    def get_product_by_page(self, page_size, page_num, tag_sn=None, sku_id=None, brand=None, i_name=None, supplier_name=None):
        product = self.session.query(Products.sku_id, Products.brand, Products.i_id, Products.i_name,
                                     Products.properties_value, Products.supplier_id, Products.supplier_name)
        if tag_sn:
            product = product.filter(Products.supplier_id == tag_sn)
        if sku_id:
            product = product.filter(Products.sku_id.like("%{0}%".format(sku_id)))
        if brand:
            product = product.filter(Products.brand.like("%{0}%".format(brand)))
        if i_name:
            product = product.filter(Products.i_name.like("%{0}%".format(i_name)))
        if supplier_name:
            product = product.filter(Products.supplier_name.like("%{0}%".format(supplier_name)))
        return product.offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_product_by_page_count(self, tag_sn=None, sku_id=None, brand=None, i_name=None, supplier_name=None):
        product = self.session.query(Products.sku_id, Products.brand, Products.i_id, Products.i_name,
                                     Products.properties_value, Products.supplier_id, Products.supplier_name)
        if tag_sn:
            product = product.filter(Products.supplier_id == tag_sn)
        if sku_id:
            product = product.filter(Products.sku_id.like("%{0}%".format(sku_id)))
        if brand:
            product = product.filter(Products.brand.like("%{0}%".format(brand)))
        if i_name:
            product = product.filter(Products.i_name.like("%{0}%".format(i_name)))
        if supplier_name:
            product = product.filter(Products.supplier_name.like("%{0}%".format(supplier_name)))
        return product.all()

    def get_product_qyt_by_sku(self, sku_id):
        return