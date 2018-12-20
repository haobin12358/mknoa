from flask import request
from mknoa.common.params_validates import parameter_required
from mknoa.common.base_service import get_session
from mknoa.service.SUsers import SUsers
from mknoa.common.success_response import Success
from mknoa.models.user import Users

class CUsers(SUsers):

    @get_session
    def login(self):
        data = parameter_required(('user_name', 'user_password'))
        user_name = data.get("user_name")
        user_password = self.get_password_by_name(user_name)
        if user_password.get("user_password") == data.get("user_password"):
            return Success('登录成功', data={'token': token})
