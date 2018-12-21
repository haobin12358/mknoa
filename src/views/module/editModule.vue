<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/module' }">模板列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑模板</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="模板名称：">
          <el-input v-model="form.name" ></el-input>
        </el-form-item>
        <el-form-item label="审批时间：">
          <el-input v-model="form.name" size="mini"></el-input>
          <span>天</span>
        </el-form-item>
        <el-form-item label="模板元素：">
          <el-checkbox-group
            v-model="checkedCities1"
            text-color="#FF7373"
            fill="#FF7373"
            >
            <p><el-checkbox label="图片">图片</el-checkbox></p>
            <p><el-checkbox label="文本框">文本框</el-checkbox></p>
            <p><el-checkbox label="表单">表单</el-checkbox></p>
            <p><el-checkbox label="文件">文件</el-checkbox></p>
          </el-checkbox-group>
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
        },
        checkedCities1: ['上海', '北京'],
        cities: ['上海', '北京', '广州', '深圳']
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
