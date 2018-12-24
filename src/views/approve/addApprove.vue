<template>
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/allApprove' }">审批流管理</el-breadcrumb-item>
        <el-breadcrumb-item>发起审批</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="m-row">
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
          <el-card class="box-card">
            <el-form ref="form" :model="form" label-width="120px">
              <el-form-item label="审批类型：">
                <el-select v-model="form.region" placeholder="请选择审批流">
                  <el-option label="区域一" value="shanghai"></el-option>
                  <el-option label="区域二" value="beijing"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="活动名称：">
                 <span>3天</span>
              </el-form-item>
              <el-form-item label="申请人：">
                <el-input v-model="form.name"></el-input>
              </el-form-item>
              <el-form-item label="理由描述：">
                <el-input type="textarea" v-model="form.desc"></el-input>
              </el-form-item>
              <el-form-item label="上传图片：">
                <el-upload
                  class="upload-demo"
                  action="https://jsonplaceholder.typicode.com/posts/"
                  :on-preview="handlePreview"
                  :on-remove="handleRemove"
                  :before-remove="beforeRemove"
                  multiple
                  :limit="3"
                  :on-exceed="handleExceed"
                >
                  <el-button size="small" type="primary">
                    <svg-icon icon-class="icon-img" />
                    上传图片
                  </el-button>
                </el-upload>
              </el-form-item>
              <el-form-item label="上传附件：">
                <el-upload
                  class="upload-demo"
                  action="https://jsonplaceholder.typicode.com/posts/"
                  :on-preview="handlePreview"
                  :on-remove="handleRemove"
                  :before-remove="beforeRemove"
                  multiple
                  :limit="3"
                  :on-exceed="handleExceed"
                >
                  <el-button size="small" type="primary">
                    <svg-icon icon-class="icon-file" />
                    上传附件
                  </el-button>
                </el-upload>
              </el-form-item>
              <el-form-item>
                <div class="m-form-btn">
                  <span class="active">提交</span>
                </div>
              </el-form-item>
            </el-form>

          </el-card>
        </el-col>
      </el-row>


    </div>
</template>

<script>
  export default {
    data() {
      return {
        data:[['a','b','c'],['a','b','c'],['a','b','c']],
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },

      }
    },
    methods: {
      onSubmit() {
        console.log('submit!');
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      getCheckedKeys(key){
        console.log(this.$refs.tree.getCheckedKeys())
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
.m-row{
  margin-top: 20px;
}
</style>
