<template>
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/allApprove' }">审批流管理</el-breadcrumb-item>
        <el-breadcrumb-item>发起审批</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="m-row" v-if="approval_message">
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
          <el-card class="box-card">
            <el-form ref="form" :model="form" label-width="120px">
              <el-form-item label="审批类型">
                <span>{{approval_message.approval_name}}</span>
              </el-form-item>
              <el-form-item label="审批时间">
                 <span>{{approval_message.mould_message.mould_time}}天</span>
              </el-form-item>
              <template v-for="(item,index) in approval_message.mould_message.mould_list">

                <el-form-item label="上传图片" v-if="item.mouldelement_name_trans == '图片'">
                  <!--<el-upload-->
                    <!--class="upload-demo"-->
                    <!--action="https://jsonplaceholder.typicode.com/posts/"-->
                    <!--:on-preview="handlePreviewPic"-->
                    <!--:on-remove="handleRemovePic"-->
                    <!--:before-remove="beforeRemovePic"-->
                    <!--:http-request="uploadImg"-->
                    <!--list-type="picture"-->
                    <!--multiple-->
                    <!--:file-list="approval_message.mould_message.mould_list[index].element_value"-->
                  <!--&gt;-->
                    <!--<el-button size="small" class="m-upload-btn">-->
                      <!--<svg-icon icon-class="icon-img" />-->
                      <!--上传图片-->
                    <!--</el-button>-->
                  <!--</el-upload>-->
                  <div class="inputbg"><el-button size="small" class="m-upload-btn">
                    <svg-icon icon-class="icon-img" />
                    上传图片
                  </el-button>
                    <input type="file" id="main" accept="image/*" @change="uploadImg">
                  </div>
                  <div class="m-up-img-box" v-if="approval_message.mould_message.mould_list[index].element_value.length >0">
                    <div class="inputbg m-img-xl el-upload-list--picture-card" v-for="(key,k) in approval_message.mould_message.mould_list[index].element_value">
                      <img :src="key"   style="width: 120px;height:120px;"/>
                      <span class="el-upload-list__item-actions">
                        <span class="el-upload-list__item-preview" @click="handlePreviewPic(k,index)">
                          <i class="el-icon-zoom-in"></i>
                        </span>
                        <span class="el-upload-list__item-delete" @click="handleRemovePic(k,index)">
                          <i class="el-icon-delete"></i>
                        </span>
                      </span>
                    </div>
                  </div>
                  <el-dialog :visible.sync="dialogVisible">
                    <img width="100%" :src="dialogImageUrl" alt="">
                  </el-dialog>
                </el-form-item>
                <el-form-item :label="item.mouldelement_name" v-if="item.mouldelement_name_trans == '文本框'">
                  <el-input v-model="approval_message.mould_message.mould_list[index].element_value"></el-input>
                </el-form-item>
                <el-form-item label="表格" v-if="item.mouldelement_name_trans == '表格'">
                  <table width="100%" class="m-approval-table" cellspacing="1" cellpadding="0">
                    <tr v-for="(i,_index) in item.element_value">
                      <td v-for="(j,_j) in i">
                        <el-input v-model="approval_message.mould_message.mould_list[index].element_value[_index][_j]"></el-input>
                      </td>
                    </tr>
                  </table>
                </el-form-item>
                <el-form-item label="上传附件" v-if="item.mouldelement_name_trans == '文件'">
                  <el-upload
                    class="upload-demo"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :before-remove="beforeRemove"
                    multiple
                    :file-list="approval_message.mould_message.mould_list[index].element_value"
                    :http-request="uploadFile"
                  >
                    <el-button size="small" class="m-upload-btn">
                      <svg-icon icon-class="icon-file" />
                      上传附件
                    </el-button>
                  </el-upload>
                </el-form-item>

              </template>
              <el-form-item>
                <div class="m-form-btn">
                  <span class="active" @click="submitSure">提交</span>
                </div>
              </el-form-item>
            </el-form>

          </el-card>
        </el-col>
      </el-row>


    </div>
</template>

<script>
  import axios from 'axios';
  import api from '../../api/api';
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
        approval_message:null,
        dialogVisible:false,
        dialogImageUrl:''
      }
    },
    mounted(){
      this.approval_name = this.$route.query.approval_name;
      this.getApproveMessage();
    },
    methods: {
      submitSure() {
        let arr = [].concat(this.approval_message.mould_message.mould_list);
        let _arr = [],_index = -1;
        for(let i=0;i<arr.length;i++){
          if(arr[i].mouldelement_name_trans == '文件'){
            _arr = [].concat(arr[i].element_value);
            _index = i;
          }
        }
        if(_index > -1){
          for(let j=0;j<_arr.length;j++){
            arr[_index].element_value[j] = {
              name:_arr[j].name,
              url:_arr[j].url
            }
          }
        }
        axios.post(api.launch_approval +'?token='+localStorage.getItem('token')+'&approval_id='+this.$route.query.approval_id,{
          approval_name:this.approval_message.approval_name,
          approvalmould_list: arr
        }).then(res => {
          if(res.data.status == 200){
            this.$notify({
              title: '成功',
              message: res.data.message,
              type: 'success'
            });
            this.$router.push('/allApprove');
          }
        })
      },
      /*获取样式*/
      getApproveMessage(){
        axios.get(api.get_relaunch_approval,{
          params:{
            token:localStorage.getItem('token'),
            approval_id: this.$route.query.approval_id
          }
        }).then(res => {
          if(res.data.status == 200){
            this.approval_message = res.data.data;
          }
        })
      },
      //删除图片
      handleRemovePic(i,index){
        let arr = [].concat(this.approval_message.mould_message.mould_list);
        arr[index].element_value.splice(i,1);
        this.approval_message.mould_message.mould_list = [].concat(arr);
      },
      handleRemove(file, fileList) {
        let arr = [].concat(this.approval_message.mould_message.mould_list);
        for(let i =0;i<arr.length;i++){
          if(arr[i].mouldelement_name_trans == '文件'){
            arr[i].element_value = [].concat(fileList);
          }
        }
        this.approval_message.mould_message.mould_list = [].concat(arr);
      },
      //预览
      handlePreviewPic(i,index) {
        this.dialogVisible = true;
        this.dialogImageUrl = this.approval_message.mould_message.mould_list[index].element_value[i];
      },
      handlePreview(file) {
        console.log(file);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      uploadImg(file){
        let form = new FormData();
        form.append("file", file.target.files[0]);
        form.append("FileType", 'pic');
        axios.post(api.upload_files ,form).then(res => {
          if(res.data.status == 200){
            let arr = [].concat(this.approval_message.mould_message.mould_list);
            for(let i =0;i<arr.length;i++){
              if(arr[i].mouldelement_name_trans == '图片'){
                arr[i].element_value.push(res.data.data.url);
              }
            }
            this.approval_message.mould_message.mould_list = [].concat(arr);
            var file = document.getElementById('main');
            file.value ='';
          }else{
            this.$message({
              type: 'error',
              message: '服务器请求失败，请稍后再试 '
            });
          }
        },error =>{
          this.$message({
            type: 'error',
            message: '服务器请求失败，请稍后再试 '
          });
        })
      },
      uploadFile(file){
        let form = new FormData();
        form.append("file", file.file);
        form.append("FileType", 'file');
        axios.post(api.upload_files ,form).then(res => {
          if(res.data.status == 200){
            let arr = [].concat(this.approval_message.mould_message.mould_list);
            for(let i =0;i<arr.length;i++){
              if(arr[i].mouldelement_name_trans == '文件'){
                arr[i].element_value.push({name:res.data.data.filename,url:res.data.data.url});
              }
            }
            this.approval_message.mould_message.mould_list = [].concat(arr);
          }else{
            this.$message({
              type: 'error',
              message: '服务器请求失败，请稍后再试 '
            });
          }
        },error =>{
          this.$message({
            type: 'error',
            message: '服务器请求失败，请稍后再试 '
          });
        })
      }

    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
.m-row{
  margin-top: 20px;
}
  .m-approval-table{
    border-right: 1px solid #eee;
    border-bottom: 1px solid #eee;
    td{
      border-left: 1px solid #eee;
      border-top: 1px solid #eee;
      text-align: center;
    }
  }
.el-upload-list--picture-card .el-upload-list__item-actions:hover {
  opacity: 1;
}
.m-up-img-box{
  display: flex;
  flex-flow: row;
  align-items: flex-start;
  justify-content: flex-start;
  flex-wrap: wrap;
  height: auto;
  margin-top: 20px;
  min-height: 120px;
  .el-upload-list__item-actions {
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    cursor: default;
    text-align: center;
    color: #fff;
    opacity: 0;
    font-size: 20px;
    background-color: rgba(0,0,0,.5);
    -webkit-transition: opacity .3s;
    transition: opacity .3s;
    border-radius: 6px;
    display: flex;
    flex-flow: row;
    align-items: center;
    justify-content: center;
    span {
      cursor: pointer;
    }
  }
}
.inputbg{
  margin-left: 10px;
  color: #97ADCB;
  background-color: #fbfdff;
  border-radius: 6px;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  position: relative;
  width: 100px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  &.m-img-xl{
    width: 120px;
    height: 120px;
    line-height: 120px;
  }
}
.inputbg input{
  position: absolute;
  top: 0;
  left: 0;
  opacity:0;
  filter:alpha(opacity=0);
  width: 100px;
  height: 36px;
  line-height: 36px;
  cursor: pointer;
}
</style>
