from mknoa.common.base_service import SBase
from mknoa.models.power import Powers, PowerTag, PowersMeta
from sqlalchemy import or_, and_, extract

class SPowers(SBase):

    def get_parent_power_admin(self):
        return self.session.query(Powers.power_id,
                                  Powers.power_component, Powers.power_path, Powers.power_redirect, Powers.power_status, Powers.power_hidden)\
            .filter_by(power_parent_id='0').all()

    def get_meta_by_powerid(self, power_id):
        return self.session.query(PowersMeta.powermeta_roles, PowersMeta.powermeta_icon, PowersMeta.powermeta_title)\
            .filter_by(power_id=power_id).first()

    def get_power_by_parentid(self, power_parent_id):
        return self.session.query(Powers.power_id,
                                  Powers.power_component, Powers.power_path, Powers.power_redirect, Powers.power_status, Powers.power_hidden)\
            .filter_by(power_parent_id=power_parent_id).filter_by(power_status=41).all()

    def get_power_by_powerid(self, power_id):
        return self.session.query(Powers.power_id, Powers.power_parent_id,
                                  Powers.power_component, Powers.power_path, Powers.power_redirect, Powers.power_status) \
            .filter_by(power_id=power_id).first()

    def get_powerid_by_tagid(self, tag_id):
        return self.session.query(PowerTag.power_id).filter_by(tag_id=tag_id).filter_by(powertag_status=51).all()

    def update_spower(self, power_id, power):
        self.session.query(Powers).filter_by(power_id=power_id).update(power)
        self.session.commit()
        return True

    def update_spowermeta(self, power_id, powermeta):
        self.session.query(PowersMeta).filter_by(power_id=power_id).update(powermeta)
        self.session.commit()
        return True