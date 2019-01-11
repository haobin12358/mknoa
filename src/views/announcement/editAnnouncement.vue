<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/announcement' }">公告列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑公告</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="noticeForm" :model="form" label-width="100px" :rules="rules" :disabled="!isRead">
        <el-form-item label="公告标题：" prop="notice_title">
          <el-input v-model="form.notice_title" ></el-input>
        </el-form-item>
        <el-form-item label="公告内容：" prop="notice_message">
          <el-input v-model="form.notice_message" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="推送身份：" >
          <el-select v-model="form.tag_list" multiple placeholder="请选择">
            <el-option
              v-for="item in tags"
              :key="item.tag_id"
              :label="item.tag_name"
              :value="item.tag_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="推送用户：" >
          <el-select v-model="form.user_list" multiple placeholder="请选择">
            <el-option
              v-for="item in users"
              :key="item.user_id"
              :label="item.user_name"
              :value="item.user_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="isRead">
          <div class="m-form-btn">
            <span class="active" @click="submitSure">保存</span>
            <span @click="cancelForm">取消</span>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../../api/api'
  export default {
    data() {
      return {
        form: {
          notice_title: '',
          notice_message:'',
          tag_list:[],
          user_list:[]
        },
        rules: {
          notice_title: [
            { required: true, message: '请输入公告标题', trigger: 'blur' },
          ],
          notice_message: [
            { required: true, message: '请输入公告内容码', trigger: 'change' }
          ]
        },
        tags:[],
        users:[]
      }
    },
    inject:['reload'],
    computed:{
      isRead(){
        return this.$route.query.is_read
      }
    },
    mounted(){
      if(this.$route.query.notice_id){
        this.getDetail();
      }
      this.getTags();
      this.getUsers();
    },
    methods: {
      //保存
      submitSure() {
        this.$refs['noticeForm'].validate((valid) => {
          if (valid) {
            if(this.$route.query.notice_id){
              axios.post(api.update_notice + '?token=' +localStorage.getItem('token') +'&notice_id=' + this.form.notice_id,this.form).then(res => {
                if(res.data.status == 200){
                  this.$notify({
                    title: '成功',
                    message: res.data.message,
                    type: 'success'
                  });
                  this.$router.push({path:'/announcement'})
                }else{
                  this.$message.error(res.data.message);
                }
              })
            }else {
              axios.post(api.new_notice + '?token=' + localStorage.getItem('token'), this.form).then(res => {
                if (res.data.status == 200) {
                  this.$notify({
                    title: '成功',
                    message: res.data.message,
                    type: 'success'
                  });
                  this.$router.push('/announcement');
                } else {
                  this.$message.error(res.data.message);
                }
              })
            }
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      //取消，重新加载页面
      cancelForm(){
        this.reload();
      },
    //  获取公告详情
      getDetail(){
        axios.get(api.get_notice_message,{
          params:{
            token:localStorage.getItem('token'),
            notice_id: this.$route.query.notice_id
          }
        }).then(res => {
          if(res.data.status == 200){
            this.form ={
              notice_id: this.$route.query.notice_id,
              notice_title:res.data.data.notice_title,
              notice_message: res.data.data.notice_message,
              tag_list:res.data.data.tag_list ?[].concat(res.data.data.tag_list):[] ,
              user_list:res.data.data.user_list ? [].concat(res.data.data.user_list):[]
            }
          }
        })
      },
    //  获取身份列表
      getTags(){
        axios.get(api.get_tags_all,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
          if(res.data.status == 200){
            this.tags = res.data.data;
          }else{
            this.$message.error(res.data.message)
          }
        })
      },
    //  获取用户列表
      getUsers(){
        axios.get(api.get_all_user_easy,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
          if(res.data.status == 200){
            this.users = res.data.data;
          }else{
            this.$message.error(res.data.message)
          }
        })
      }

    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
