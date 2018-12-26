<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/approve' }">审批流列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑审批流</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="approveForm" :model="form" label-width="120px" :rules="rules">
        <el-form-item label="审批流名称：" prop="approval_name">
          <el-input v-model="form.approval_name" ></el-input>
        </el-form-item>
        <el-form-item label="选择模板：" prop="mould_id">
          <el-select v-model="form.mould_id" placeholder="请选择模板">
            <el-option :label="item.mould_name" v-for="item in mould_list" :key="item.mould_id" :value="item.mould_id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="多级审批：" required>
          <div v-for="(items,index) in form.approval_level_list">
            <el-select v-model="form.approval_level_list[index].tag_id"  placeholder="请选择默认审批身份">
              <el-option :label="item.tag_name" v-for="item in tag_list" :key="item.tag_name" :value="item.tag_id"></el-option>
            </el-select>
            <span class="m-cut-add-box">
               <span @click="cutTag(index)" v-if="!(form.approval_level_list.length == 1 && index == 0)"><svg-icon icon-class="icon-form-cut" /></span>
              <span @click="addTag" v-if="index == form.approval_level_list.length-1"> <svg-icon icon-class="icon-form-add"  /></span>
            </span>
          </div>
        </el-form-item>
        <el-form-item label="使用身份：" prop="approval_power_list">
          <el-select v-model="form.approval_power_list" multiple  placeholder="请选择身份">
            <el-option :label="item.tag_name" v-for="item in tag_list" :key="item.tag_name" :value="item.tag_id"></el-option>
          </el-select>
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
        form: {
          approval_name: '',
          mould_id: '',
          approval_level_list: [
            {
              tag_id:'',
              approvallevel_index:1
            }
          ],
          approval_power_list:[]
        },
        rules: {
          approval_name: [
            { required: true, message: '请输入审批流名称', trigger: 'blur' },
          ],
          mould_id: [
            { required: true, message: '请选择模板', trigger: 'change' }
          ],
          approval_power_list: [
            { required: true, message: '请选择使用身份', trigger: 'change' }
          ]
        },
        tag_list:[],
        mould_list:[]
      }
    },
    inject:['reload'],
    mounted(){
      this.getTag();
      this.getMould();
      if(this.$route.query.approval_id){
        this.getDetail();
      }
    },
    methods: {
      //  获取公告详情
      getDetail(){
        axios.get(api.approval_message,{
          params:{
            token:localStorage.getItem('token'),
            approval_id: this.$route.query.approval_id
          }
        }).then(res => {
          if(res.data.status == 200){
            this.approval_id = this.$route.query.approval_id;
            this.form ={
              approval_name:res.data.data.approval_name,
              mould_id: res.data.data.mould_id,
              approval_level_list:[].concat(res.data.data.approval_level_list),
              approval_power_list:[].concat(res.data.data.approval_power_list)
            }
          }
        })
      },
      /*保存*/
      submitSure() {
        this.$refs['approveForm'].validate((valid) => {
          if (valid) {
            for(let i=0;i<this.form.approval_level_list.length;i++){
              if(this.form.approval_level_list[i].tag_id == ''){
                this.$message.error('请先选择每个关联身份');
                return false;
              }
            }
            console.log(this.form.approval_power_list)

            if(this.$route.query.approval_id){
              axios.post(api.update_approval + '?token=' +localStorage.getItem('token') +'&approval_id=' + this.approval_id,this.form).then(res => {
                if(res.data.status == 200){
                  this.$notify({
                    title: '成功',
                    message: res.data.message,
                    type: 'success'
                  });
                  this.$router.push('/approve');
                }else{
                  this.$message.error(res.data.message);
                }
              })
            }else {
              axios.post(api.new_approval + '?token=' + localStorage.getItem('token'), this.form).then(res => {
                if (res.data.status == 200) {
                  this.$notify({
                    title: '成功',
                    message: res.data.message,
                    type: 'success'
                  });
                  this.$router.push('/approve');
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
      /*取消*/
      cancelForm(){
        this.reload();
      },
      /*获取模板*/
      getMould(){
        axios.get(api.get_mould_list_choose,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
          if(res.data.status == 200){
            this.mould_list = res.data.data;
          }else{
            this.$message.error(res.data.message);
          }

        })
      },
      /*获取身份等级*/
      getTag(){
        axios.get(api.get_tags_all,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
          if(res.data.status == 200){
            this.tag_list = res.data.data;
          }else{
            this.$message.error(res.data.message);
          }

        })
      },
      /*添加关联身份*/
      addTag(){
        this.form.approval_level_list.push({tag_id:'', approvallevel_index:this.form.approval_level_list.length +1});
      },
      cutTag(index){
        let that = this;
        this.$confirm('确定要删除这级身份吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.form.approval_level_list.splice(index,1)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
