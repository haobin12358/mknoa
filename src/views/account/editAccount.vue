<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/account/account' }">账号列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑账号</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="accountForm" :model="form" label-width="100px" :rules="rules">
        <el-form-item label="账号：" prop="user_name">
          <el-input v-model="form.user_name" ></el-input>
        </el-form-item>
        <el-form-item label="密码：" prop="user_password">
          <el-input v-model="form.user_password" type="password" ></el-input>
        </el-form-item>
        <el-form-item label="联系方式：" prop="user_telphone">
          <el-input v-model="form.user_telphone" ></el-input>
        </el-form-item>
        <el-form-item label="关联身份：" prop="user_tags">
          <el-select v-model="form.user_tags" multiple  placeholder="请选择身份">
            <el-option :label="item.tag_name" v-for="item in level_list" :key="item.tag_name" :value="item.tag_name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="具体信息：" prop="user_message">
          <el-input v-model="form.user_message" type="textarea"></el-input>
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
  import axois from 'axios';
  import api from '../../api/api';
  export default {
    data() {
      return {
        level_list:[],
        form: {
          user_name: '',
          user_password: '',
          user_telphone: '',
          user_message: '',
          user_tags: []
        },
        rules: {
          user_name: [
            { required: true, message: '请输入活动名称', trigger: 'blur' },
          ],
          user_password: [
            { required: true, message: '请输入密码', trigger: 'change' }
          ],
          user_tags: [
            { type: 'array', required: true, message: '请至少选择一个身份关联', trigger: 'change' }
          ],
          user_telphone: [
            { required: true, message: '请输入联系方式', trigger: 'change' }
          ],
          user_message: [
            { required: true, message: '请填写具体信息', trigger: 'blur' }
          ]
        }
      }
    },
    inject:['reload'],
    mounted(){
      this.getLevel();
    },
    methods: {
      submitSure() {
        this.$refs['accountForm'].validate((valid) => {
          if (valid) {
            axois.post(api.new_user + '?token=' +localStorage.getItem('token'),this.form).then(res => {
              if(res.data.status == 200){
                this.$notify({
                  title: '成功',
                  message: res.data.message,
                  type: 'success'
                });
              }else{
                this.$message.error(res.data.message);
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      cancelForm(){
        this.reload();
      },
      /*获取身份等级*/
      getLevel(){
        axois.get(api.get_tags_all,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
          if(res.data.status == 200){
            this.level_list = res.data.data;
          }else{
            this.$message.error(res.data.message);
          }

        })
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
