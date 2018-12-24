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

  get_admin_list: title + 'user/get_admin_list',                          //获取管理员列表
  add_admin_by_superadmin: title + 'user/add_admin_by_superadmin',        //添加啊管理员
  get_admin_all_type: title + 'user/get_admin_all_type',                  //获取管理员身份
  update_admin: title + 'user/update_admin',                              //更新管理员
  update_admin_password: title + 'user/update_admin_password',            //修改密码
  product_list: title + 'product/list',                                   //获取商品列表
  delete_product: title + 'product/delete_list',                          //删除商品
  supplizer_list: title + 'supplizer/list',                               //获取供应商列表
  category_list: title + 'category/list',                                 //获取类目
  brand_list: title + 'brand/list',                                       //获取品牌
  scene_list: title + 'scene/list',                                       //获取场景
  items_list: title + 'items/list',                                       //获取标签
  create_product: title + 'product/create',                               //添加商品

  get_order_situation: title + 'order/get_order_situation',               //获取订单概况
  get_all_order: title + 'order/list',                                    //获取所有订单
  get_order_by_LOid: title + 'order/get',                                 //获取订单详情
  order_count: title + 'order/count',                                     //获取订单数量
  get_omfilter: title + 'order/get_omfilter',                             //获取订单filter
  update_order_status: title + 'order/update_order_status',               //更新订单状态

  update_activity: title + 'activity/update',                             //  修改活动基础信息
  add_commodity: title + 'commodity/add',                                 //  添加试用商品
  get_all_qa: title + 'qa/get_all',                                       //获取所有问题
  add_questanswer: title + 'qa/add_questanswer',                          //添加问题
  add_questoutline: title + 'qa/add_questoutline',                        //添加问题类型
  product_get: title + 'product/get',                                     //获取商品详情
  delete_questoutline: title + 'qa/delete_questoutline',                  //删除问题分类
  delete_question: title + 'qa/delete_question',                          //删除问题
  upload_file: title + 'file/upload'                                       //上传图片

}

export default api
