<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/announcement' }">公告列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑公告</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="公告标题：">
          <el-input v-model="form.name" ></el-input>
        </el-form-item>
        <el-form-item label="公告内容：">
          <el-input v-model="form.name" type="textarea"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="m-form-btn">
            <span class="active">保存</span>
            <span>取消</span>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      }
    },
    methods: {
      onSubmit() {
        console.log('submit!');
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
