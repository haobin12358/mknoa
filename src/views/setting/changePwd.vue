<template>
  <div class="components-container">
    <el-dialog v-el-drag-dialog :visible.sync="dialogTableVisible" title="修改密码" @dragDialog="handleDrag">
      <el-form :model="pwdForm" :rules="rules" ref="pwdForm" label-width="120px">
        <el-form-item label="请输入旧密码" prop="password_old">
          <el-input type="password" class="m-input-pwd"
                    placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="请输入新密码" prop="password_new">
          <el-input type="password" class="m-input-pwd"
                    placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="请确认新密码" prop="password_repeat">
          <el-input type="password" class="m-input-pwd"
                    placeholder=""></el-input>
        </el-form-item>
      </el-form>

    </el-dialog>
  </div>
</template>

<script>
import elDragDialog from 'src/directive/el-dragDialog' // base on element-ui

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
  }
}
</script>
