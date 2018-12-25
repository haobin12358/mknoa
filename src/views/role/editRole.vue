<template>
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/role' }">身份列表</el-breadcrumb-item>
        <el-breadcrumb-item>编辑身份</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="m-form-container">
        <el-form ref="roleForm" :model="form" label-width="100px" :rules="rules">
          <el-form-item label="身份名称：" prop="tag_name">
            <el-input v-model="form.tag_name" ></el-input>
          </el-form-item>
          <el-form-item label="身份等级：" prop="tag_level">
            <el-select v-model="form.tag_level"  placeholder="请选择身份等级">
              <el-option :label="item" v-for="item in level_option" :key="Math.random()" :value="item"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="身份权限" prop="tag_power_list">
            <!--<el-checkbox-group v-model="form.type">-->
              <!--<el-checkbox label="身份管理" name="type"></el-checkbox>-->
              <!--<el-checkbox label="审批流管理" name="type"></el-checkbox>-->
              <!--<el-checkbox label="商品管理" name="type"></el-checkbox>-->
              <!--<el-checkbox label="平台公告" name="type"></el-checkbox>-->
            <!--</el-checkbox-group>-->
            <el-tree
              :data="power_list"
              show-checkbox
              ref="tree"
              :props="props"
              node-key="power_id"
              @check-change="handleCheckChange"
              :default-checked-keys="form.tag_power_list"
            >
            </el-tree>
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
  import api from '../../api/api';
    export default {
      data() {
        return {
          level_option:[],
          power_list:[],
          props:{
            label: 'power_title',
            children:'children'
          },
          form: {
            tag_name: '',
            tag_level: '',
            tag_power_list:[],
            tag_id:''
          },
          ceshi:[],
          rules: {
            tag_name: [
              { required: true, message: '请输入身份名称' },
            ],
            tag_level: [
              { required: true, message: '请输入身份等级' }
            ],
            tag_power_list: [
              { type: 'array', required: true, message: '请选择身份权限' }
            ]
          }
        }
      },
      inject:['reload'],
      mounted(){
        this.getLevel();
        this.getPower();
        if(this.$route.query.tag_id){
          this.getDetail();
        }
      },
      methods: {
        /*保存*/
        submitSure() {
          this.getCheckedKeys();
          this.$refs['roleForm'].validate((valid) => {
            if (valid) {
              if(this.$route.query.tag_id){
                axios.post(api.update_tag + '?token=' +localStorage.getItem('token') +'&tag_id=' + this.form.tag_id,this.form).then(res => {
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
              }else{
                axios.post(api.new_tags + '?token=' +localStorage.getItem('token'),this.form).then(res => {
                  if(res.data.status == 200){
                    this.$notify({
                      title: '成功',
                      message: res.data.message,
                      type: 'success'
                    });
                    this.$router.push('/role/index');
                  }else{
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
        /*取消*/
        cancelForm(){
          this.reload();
        },
        /*树上多选框选择*/
        handleCheckChange(data, checked, indeterminate) {
          console.log(data, checked, indeterminate);
        },
        /*获取已选择树的key*/
        getCheckedKeys() {
          this.form.tag_power_list =  [].concat(this.$refs.tree.getCheckedKeys());
        },
        /*获取身份等级*/
        getLevel(){
          axios.get(api.get_user_tag_level_list,{
            params:{
              token:localStorage.getItem('token')
            }
          }).then(res => {
            if(res.data.status == 200){
              this.level_option = res.data.data.tag_level_list;
            }else{
              this.$message.error(res.data.message);
            }
          })
        },
        /*获取身份权限*/
        getPower(){
          axios.get(api.get_power_list_easy,{
            params:{
              token:localStorage.getItem('token')
            }
          }).then(res => {
            if(res.data.status == 200){
              this.power_list = res.data.data;
              console.log(this.power_list)
            }else{
              this.$message.error(res.data.message);
            }
          })
        },
        /*获取身份详情*/
        getDetail(){
          axios.get(api.get_tag_message,{
            params:{
              token:localStorage.getItem('token'),
              tag_id: this.$route.query.tag_id
            }
          }).then(res => {
            if(res.data.status == 200){
              this.form ={
                tag_id: res.data.data.tag_id,
                tag_name: res.data.data.tag_name,
                tag_level: res.data.data.tag_level
              }
              let arr = [];
              for(let i=0;i<res.data.data.power_list.length;i++){
                for(let  j=0;j<res.data.data.power_list[i].children.length;j++){
                  if(res.data.data.power_list[i].children[j].power_status == 5){
                    arr.push(res.data.data.power_list[i].children[j].power_id)
                  }
                }
              }
              this.form.tag_power_list = [].concat(arr);
            }
          })
        }
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
