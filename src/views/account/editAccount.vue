<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/account' }">账号列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑账号</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="账号：">
          <el-input v-model="form.name" ></el-input>
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="form.name" type="password" ></el-input>
        </el-form-item>
        <el-form-item label="联系方式：">
          <el-input v-model="form.name" ></el-input>
        </el-form-item>
        <el-form-item label="关联身份：">
          <el-select v-model="form.region"  placeholder="请选择身份等级">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
          </el-select>
          <span class="m-cut-add-box">
             <svg-icon icon-class="icon-form-cut" />
             <svg-icon icon-class="icon-form-add" />
          </span>
        </el-form-item>
        <el-form-item label="具体信息：">
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
