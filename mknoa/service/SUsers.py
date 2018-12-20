from mknoa.common.base_service import SBase
from mknoa.models.user import Users
from sqlalchemy import or_, and_, extract

class SUsers(SBase):

    def get_password_by_name(self, user_name):
        return self.session.query(Users.user_password).filter_by(user_name=user_name).first()