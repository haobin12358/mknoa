<template>
  <div class="components-container">
    <el-dialog v-el-drag-dialog :visible.sync="dialogTableVisible" title="修改密码" @dragDialog="handleDrag">
      <el-form :model="pwdForm" :rules="rules" ref="pwdForm" label-width="120px">
        <el-form-item label="请输入旧密码" prop="password_old">
          <el-input type="password" class="m-input-pwd"
                    placeholder="" v-model="pwdForm.password_old"></el-input>
        </el-form-item>
        <el-form-item label="请输入新密码" prop="password_new">
          <el-input type="password" class="m-input-pwd"
                    placeholder="" v-model="pwdForm.password_new"></el-input>
        </el-form-item>
        <el-form-item label="请确认新密码" prop="password_repeat">
          <el-input type="password" class="m-input-pwd"
                    placeholder="" v-model="pwdForm.password_repeat"></el-input>
        </el-form-item>
        <el-form-item >
          <div class="m-form-btn">
            <span class="active" @click="submitSure">
              确认
            </span>
            <span @click="dialogTableVisible =false">
              取消
            </span>
          </div>
        </el-form-item>
      </el-form>

    </el-dialog>
  </div>
</template>

<script>
import elDragDialog from 'src/directive/el-dragDialog' // base on element-ui
import axios from 'axios';
import api from '../../api/api'
export default {
  name: 'DragDialogDemo',
  directives: { elDragDialog },
  data() {
    return {
      dialogTableVisible: false,
      pwdForm: {
        password_old: '',
        password_new: '',
        password_repeat: ''
      },
      rules: {
        password_old: [
          {required: true, message: '请输入旧密码', trigger: 'blur'}
        ],
        password_new: [
          {required: true, message: '请输入新密码', trigger: 'blur'}
        ],
        password_repeat: [
          {required: true, message: '请确认新密码', trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    // v-el-drag-dialog onDrag callback function
    handleDrag() {
      this.$refs.select.blur()
    },
    showDialog(){
        this.dialogTableVisible = true;
    },
    submitSure(){
      if(this.pwdForm.password_new != this.pwdForm.password_repeat){
        this.$message.error('两次新密码不一致');
        return false;
      }
      this.$refs['pwdForm'].validate((valid) => {
        if (valid) {
          axios.post(api.update_password + '?token='+localStorage.getItem('token'),{
            user_password:this.pwdForm.password_new,
            user_password_old: this.pwdForm.password_old
          }).then(res => {
            if(res.data.status == 200){
              this.$notify({
                title: '成功',
                message: res.data.message,
                type: 'success'
              });
              this.dialogTableVisible = false;
            }else{
              this.$message.error(res.data.message);
            }
          })
        }
      })
    }
  }
}
</script>
