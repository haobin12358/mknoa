import axios from 'src/utils/myAxios';
import api from 'src/api/api'

export const login = (adname, adpassword) => axios(api.login, {
  noLoading: true,
  method: 'post',
  data: {
    adname,
    adpassword,
  },
});
