// const title = 'http://10.0.0.197:7443/sharp/manager/';
// const title = 'http://120.79.182.43:7443/sharp/manager/';
const title = 'http://47.104.228.112:8111/api/v1/'

const api = {
  login: title + 'user/login',                                      //用户登录
  get_all_user: title +'user/get_all_user',//获取用户列表
  get_my_message: title + 'user/get_my_message',//获取用户详情
  new_user: title + 'user/new_user',//生成用户
  get_user_tag_level_list: title +'user/get_user_tag_level_list',//获取身份等级
  get_tag_list:title +'user/get_tag_list',///获取身份标签
  get_tags_all: title +'user/get_tags_all',//获取下拉身份标签
  get_power_list_easy: title +'power/get_power_list_easy',//获取权限列表
  // delete_tag: title + 'user/delete_tag',//删除用户
  new_tags: title +'user/new_tags',//创建身份
  delete_tag: title + 'user/delete_tag',//删除身份
  get_tag_message: title +'user/get_tag_message',//获取标签详情
  update_tag: title + 'user/update_tag',//更新标签
  get_notice_list: title + 'notice/get_notice_list',//获取公告列表
  get_notice_message: title +'notice/get_notice_message',//获取公告详情
  update_notice: title + 'notice/update_notice',//编辑公告
  delete_notice: title + 'notice/delete_notice',//删除公告
  new_notice: title + 'notice/new_notice',//发布公告
  get_mould_list: title + 'mould/get_mould_list',//获取模板列表
  get_mould_message: title + 'mould/get_mould_message',//获取模板详情
  new_mould: title + 'mould/new_mould',//创建模板
  delete_mould: title +'mould/delete_mould',//删除模板
  update_mould: title + 'mould/update_mould',//更新模板


}

export default api
