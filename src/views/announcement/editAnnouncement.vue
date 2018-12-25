<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/announcement/announcement' }">公告列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑公告</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="noticeForm" :model="form" label-width="100px" :rules="rules">
        <el-form-item label="公告标题：" prop="notice_title">
          <el-input v-model="form.notice_title" ></el-input>
        </el-form-item>
        <el-form-item label="公告内容：" prop="notice_message">
          <el-input v-model="form.notice_message" type="textarea"></el-input>
        </el-form-item>
        <el-form-item>
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
          notice_message:''
        },
        rules: {
          notice_title: [
            { required: true, message: '请输入公告标题', trigger: 'blur' },
          ],
          notice_message: [
            { required: true, message: '请输入公告内容码', trigger: 'change' }
          ]
        }
      }
    },
    inject:['reload'],
    mounted(){
      if(this.$route.query.notice_id){
        this.getDetail();
      }
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
                  this.$router.push({path:'/announcement/announcement'})
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
                  this.$router.push('/announcement/announcement');
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
              notice_message: res.data.data.notice_message
            }
          }
        })
      }

    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
