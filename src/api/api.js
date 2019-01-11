// const title = 'http://10.0.0.197:7443/sharp/manager/';
// const title = 'http://120.79.182.43:7443/sharp/manager/';
// const title = 'http://47.104.228.112:8111/api/v1/'
const title = 'https://mknoa.lkfcni.cn/api/v1/'

const api = {
  login: title + 'user/login',                                      //用户登录
  get_index_message:title + 'notice/get_index_message',//首页
  get_all_user: title +'user/get_all_user',//获取用户列表
  get_my_message: title + 'user/get_my_message',//获取用户详情
  new_user: title + 'user/new_user',//生成用户
  update_user_info: title +'user/update_user_info',//更新用户
  delete_user: title + 'user/delete_user',//删除用户
  get_user_tag_level_list: title +'user/get_user_tag_level_list',//获取身份等级
  get_tag_list:title +'user/get_tag_list',///获取身份标签
  get_tags_all: title +'user/get_tags_all',//获取下拉身份标签
  get_power_list_easy: title +'power/get_power_list_easy',//获取权限列表
  // delete_tag: title + 'user/delete_tag',//删除用户
  get_all_user_easy: title +'user/get_all_user_easy',//获取用户列表
  new_tags: title +'user/new_tags',//创建身份
  delete_tag: title + 'user/delete_tag',//删除身份
  get_tag_message: title +'user/get_tag_message',//获取标签详情
  update_tag: title + 'user/update_tag',//更新标签
  update_password: title +'user/update_password',//更新密码
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
  get_mould_list_choose: title +'mould/get_mould_list_choose',//获取选择模板列表

  approval_list: title +'approval/approval_list',//获取审批列表
  approval_message: title + 'approval/approval_message',//获取审批详情
  new_approval: title +'approval/new_approval',//新增审批
  update_approval: title +'approval/update_approval',//更新审批
  delete_approval: title + 'approval/delete_approval',//删除审批
  get_my_approval_list: title + 'approval/get_my_approval_list',//获取可创建的审批流列表
  get_relaunch_approval: title +'approval/get_relaunch_approval',//获取需要发起的审批流表单样式
  upload_files: title +'common/upload_files',//上传文件
  launch_approval: title +'approval/launch_approval',//发起创建流
  my_approve_approval_list: title + 'approval/my_approve_approval_list',//我发起的审批流
  approve_approval_list: title + 'approval/approve_approval_list',//我收到的审批流
  approve_approval_message: title +'approval/approve_approval_message',//审批流详情
  approve_approval: title +'approval/approve_approval',//审批
  get_product_list: title + 'common/get_product_list',//获取库存列表
  get_qyt_list: title +'common/get_qyt_list',//获取今日销量
  send_message: title +'notice/send_message',//发送短信
  get_history_sale: title +'common/get_history_sale',//获取历史销售
}

export default api
