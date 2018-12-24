import axios from 'src/utils/myAxios';
import api from 'src/api/api'

export const login = (username, password) => axios(api.login, {
  noLoading: true,
  method: 'post',
  data: {
    user_name: username,
    user_password: password
  },
});
