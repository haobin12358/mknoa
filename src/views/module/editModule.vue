<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/module/index' }">模板列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑模板</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="m-form-container">
      <el-form ref="moudleForm" :model="form" label-width="100px" :rules="rules">
        <el-form-item label="模板名称：" prop="mould_name">
          <el-input v-model="form.mould_name" ></el-input>
        </el-form-item>
        <el-form-item label="审批时间：" prop="mould_time">
          <el-input v-model="form.mould_time" type="number" size="mini"></el-input>
          <span>天</span>
        </el-form-item>
        <el-form-item label="模板元素：" prop="mouldelement_name">
          <el-checkbox-group
            v-model="form.mouldelement_name"
            text-color="#FF7373"
            fill="#FF7373"
            >
            <p><el-checkbox label="图片" >图片</el-checkbox></p>
            <p><el-checkbox label="文本框" @change="textChange">文本框</el-checkbox></p>

            <div class="m-text-box" v-if="show_text">
              <el-row :gutter="10" class="m-row" v-for="(item,index) in text_value" :key="Math.random()">
                <el-col :xs="3" :sm="3" :md="3" :lg="3" :xl="3" class="m-label"><span >文本框标题</span></el-col>
                <el-col :span="12"><el-input v-model="text_value[index]" placeholder="请输入内容"></el-input></el-col>
                <el-col :span="4">
                  <span class="m-cut-add-box">
                    <span @click="cutText(index)">  <svg-icon icon-class="icon-form-cut" /></span>

                       <span v-if="index == text_value.length-1" @click="addText"><svg-icon icon-class="icon-form-add" /></span>
                  </span>
                </el-col>
              </el-row>
            </div>
            <p><el-checkbox label="表单" @change="tableChange">表单</el-checkbox></p>
            <div class="m-table-box" v-if="show_table">
              <el-row :gutter="10" class="m-row" v-for="(item,index) in table_value" :key="Math.random()">
                <el-col :xs="2" :sm="2" :md="2" :lg="2" :xl="2" class="m-label"><span >行列数:</span></el-col>
                <el-col :span="2"><el-input type="number" v-model="table_value[index][0]" ></el-input></el-col>
                <el-col :span="1" class="m-label"><span >行</span></el-col>
                <el-col :span="2"><el-input type="number" v-model="table_value[index][1]" ></el-input></el-col>
                <el-col :span="1" class="m-label"><span >列</span></el-col>
                <el-col :span="4">
                  <span class="m-cut-add-box">
                    <span @click="cutTable(index)">  <svg-icon icon-class="icon-form-cut" /></span>
                       <span v-if="index == table_value.length-1" @click="addTable"><svg-icon icon-class="icon-form-add" /></span>
                  </span>
                </el-col>
              </el-row>
            </div>
            <p><el-checkbox label="文件">文件</el-checkbox></p>
          </el-checkbox-group>
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
        input:'',
        mould_id:'',
        form: {
          mould_name: '',
          mould_time: '',
          mouldelement_name: []
        },
        rules: {
          mould_name: [
            { required: true, message: '请输入模板名称' },
          ],
          mould_time: [
            { required: true, message: '请输入审批时间' }
          ],
          mouldelement_name: [
            { required: true, message: '请选择模板内容' }
          ]
        },
        show_text:false,
        text_value:[''],
        show_table:false,
        table_value:[[1,1]]
      }
    },
    inject:['reload'],
    mounted(){
      if(this.$route.query.mould_id){
        this.getDetail();
      }
    },
    methods: {
      /*获取用户详情*/
      getDetail(){
        axios.get(api.get_mould_message,{
          params:{
            token:localStorage.getItem('token'),
            mould_id: this.$route.query.mould_id
          }
        }).then(res => {
          if(res.data.status == 200){
            this.mould_id = this.$route.query.mould_id;
            this.form ={
              mould_name:res.data.data.mould_name,
              mould_time: res.data.data.mould_time
            }
            let arr1 = [] , arr2 = [],arr =[];
            for(let i=0;i<res.data.data.mould_list.length;i++){
              if(res.data.data.mould_list[i].mouldelement_name_trans == '文本框'){
                arr1.push(res.data.data.mould_list[i].mouldelement_name);
                this.show_text = true;
              }else  if(res.data.data.mould_list[i].mouldelement_name_trans == '表单'){
                arr2.push(res.data.data.mould_list[i].mouldelement_rank);
                this.show_table = true;
              }
              arr.push(res.data.data.mould_list[i].mouldelement_name_trans);
            }
            if(arr1.length == 0){
              arr1.push('')
            }
            if(arr2.length == 0){
              arr2.push('')
            }
            this.text_value = [].concat(arr1);
            this.table_value = [].concat(arr2);
            this.form.mouldelement_name = [].concat(arr);
          }
        })
      },
      /*确定*/
      submitSure() {
        this.$refs['moudleForm'].validate((valid) => {
          if (valid) {
            let arr = this.form.mouldelement_name;
            let list = [];
            let _index = 1;
            for(let i=0;i<arr.length;i++){
              if(arr[i] == '图片' || arr[i] == '文件'){
                list.push({mouldelement_name:arr[i],mouldelement_index:_index});
                _index++;
              }else if(arr[i] == '文本框') {
                for (let j = 0; j < this.text_value.length; j++) {
                  if (this.text_value[j] == '') {
                    this.$message({
                      message: '请先设置文本框名称',
                      type: 'warning'
                    });
                    return false;
                  } else {
                    list.push({
                      mouldelement_name: arr[i],
                      mouldelement_index: _index,
                      mouldelement_trans: this.text_value[j]
                    });
                    _index++;
                  }
                }
              }else if(arr[i] == '表单'){
                for(let j=0;j<this.table_value.length;j++){
                  list.push({
                    mouldelement_name: arr[i],
                    mouldelement_index: _index,
                    mouldelement_rank: this.table_value[j]
                  });
                  _index++;
                }
              }
            }

            axios.post(api.new_mould +'?token='+localStorage.getItem('token'),{
              mould_name: this.form.mould_name,
              mould_time: this.form.mould_time,
              mould_list: list
            }).then(res => {
              if(res.data.status == 200){
                this.$notify({
                  title: '成功',
                  message: res.data.message,
                  type: 'success'
                });
                this.$router.push({path:'/module/index'})
              }else{
                this.$message.error(res.data.message);
              }
            })
          }
        })
      },
      /*取消*/
      cancelForm(){
        this.reload();
      },
      //点击文本框
      textChange(bool){
        this.show_text = bool;
      },
      tableChange(bool){
        this.show_table = bool;
      },
      //添加一行文本框
      addText(){
        this.text_value.push('');
      },
      //删除一行文本框
      cutText(index){
        let that = this;
        this.$confirm('确定要删除这级身份吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.text_value.splice(index,1)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      //添加一行表格
      addTable(){
        this.table_value.push([1,1]);
      },
      //删除一行表格
      cutTable(index){
        let that = this;
        this.$confirm('确定要删除这级身份吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.table_value.splice(index,1)
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
