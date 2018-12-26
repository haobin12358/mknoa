from mknoa.common.base_service import SBase
from mknoa.models.moulds import Elements, Moulds, MouldElement
from sqlalchemy import or_, and_, extract

class SMoulds(SBase):

    def get_elementid_by_elementname(self, element_name):
        return self.session.query(Elements.element_id).filter_by(element_name=element_name).first()

    def get_mould_list_by_page(self, page_num, page_size):
        return self.session.query(Moulds.mould_id, Moulds.mould_name, Moulds.mould_time).filter_by(mould_status=61)\
            .offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_mould_count(self):
        return self.session.query(Moulds.mould_id, Moulds.mould_name, Moulds.mould_time).filter_by(mould_status=61).all()

    def get_mould_message_by_mouldid(self, mould_id):
        return self.session.query(Moulds.mould_time, Moulds.mould_name).filter_by(mould_id=mould_id).first()

    def get_mould_element_by_mouldid(self, mould_id):
        return self.session.query(MouldElement.mouldelement_id, MouldElement.element_id, MouldElement.mouldelement_name,
                                  MouldElement.mouldelement_index, MouldElement.mouldelement_rank)\
            .filter_by(mould_id=mould_id).filter_by(mouldelement_status=81).all()

    def get_elementname_by_elementid(self, element_id):
        return self.session.query(Elements.element_name).filter_by(element_id=element_id).first()

    def s_update_mould(self, mould_id, mould):
        self.session.query(Moulds).filter_by(mould_id=mould_id).update(mould)
        self.session.commit()
        return True

    def s_update_mouldelement(self, mouldelement_id, mouldelement):
        self.session.query(MouldElement).filter_by(mouldelement_id=mouldelement_id).update(mouldelement)
        self.session.commit()
        return True