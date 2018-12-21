<template>
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/role' }">身份列表</el-breadcrumb-item>
        <el-breadcrumb-item>编辑身份</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="m-form-container">
        <el-form ref="form" :model="form" label-width="100px">
          <el-form-item label="身份名称：">
            <el-input v-model="form.name" ></el-input>
          </el-form-item>
          <el-form-item label="身份等级：">
            <el-select v-model="form.region"  placeholder="请选择身份等级">
              <el-option label="区域一" value="shanghai"></el-option>
              <el-option label="区域二" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="身份权限">
            <el-checkbox-group v-model="form.type">
              <el-checkbox label="身份管理" name="type"></el-checkbox>
              <el-checkbox label="审批流管理" name="type"></el-checkbox>
              <el-checkbox label="商品管理" name="type"></el-checkbox>
              <el-checkbox label="平台公告" name="type"></el-checkbox>
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
