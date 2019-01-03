<template>
  <div  v-if="approval_message">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/allApprove' }">审批流管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{approval_message.approvalsub_message.approval_name}}</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="m-row">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <el-card class="box-card">
          <h3 class="m-title-name">审批流名称</h3>
          <el-row >
            <el-col :xs="24" :sm="6" :md="4" :lg="4" :xl="4">
              <span class="m-label">来源：</span>
              <span>{{approval_message.approvalsub_message.user_truename}}</span>
            </el-col>
            <el-col :xs="24" :sm="6" :md="6" :lg="6" :xl="6">
              <span class="m-label">申请时间：</span>
              <span>{{approval_message.approvalsub_message.approvalsub_createtime}}</span>
            </el-col>
            <el-col :xs="24" :sm="6" :md="8" :lg="8" :xl="8">
              <span class="m-label">截止时间：</span>
              <span>{{approval_message.approvalsub_message.approvalsub_endtime}}</span>
            </el-col>
          </el-row>
         <p class="m-row">
           <span class="m-label">联系方式：</span>
           <span>{{approval_message.approvalsub_message.user_telphone}}</span>
         </p>
          <div class="m-row">
            <span class="m-label">详情：</span>
            <div class="m-detail-box">
              <div class="m-row  m-flex-start" v-for="(items,index) in approval_message.approvalsub_list">
                <span class="m-label" v-if="items.element_name != '文本框'">{{items.element_name}}：</span>
                <span class="m-label" v-else>{{items.mouldelement_name}}：</span>
                <span v-if="items.element_name == '文本框'">{{items.element_value}}</span>
                <a :href="item.url" class="m-link" v-else-if="items.element_name == '文件'" :download="item.name" v-for="item in items.element_value">{{item.name}}</a>
                <div class="m-up-img-box" v-else-if="items.element_name == '图片'">
                  <div class="inputbg m-img-xl el-upload-list--picture-card" v-for="(item,i) in items.element_value">
                    <img :src="item"   style="width: 120px;height:120px;"/>
                    <span class="el-upload-list__item-actions">
                          <span class="el-upload-list__item-preview" @click="handlePreviewPic(i,index)">
                            <i class="el-icon-zoom-in"></i>
                          </span>

                        </span>
                  </div>
                </div>
                <table width="80%" class="m-approval-table" cellspacing="1" cellpadding="0" v-else-if="items.element_name == '表格'">
                  <tr v-for="i in items.element_value">
                    <td v-for="j in i">
                      {{j}}
                    </td>
                  </tr>
                </table>

                <el-dialog :visible.sync="dialogVisible">
                  <img width="100%" :src="dialogImageUrl" alt="">
                </el-dialog>
              </div>

            </div>
          </div>
          <div class="m-row">
            <span class="m-label">上级意见：</span>
            <ul class="m-reason-ul">
              <li class="m-agree" v-for="(items,index) in approval_message.approvalsov_list">
                <svg-icon icon-class="icon-agree" v-if="items.approvalsov_suggestion == '审批通过'" class="m-icon"/>
                <svg-icon icon-class="icon-refuse" v-else-if="items.approvalsov_suggestion == '已驳回'" class="m-icon"/>
                <svg-icon icon-class="icon-wait" v-else-if="items.approvalsov_suggestion == '待审批'" class="m-icon"/>
                <p class="m-mr">
                  <span v-if="items.approvalsov_suggestion == '待审批' && approval_message.approvalsub_message.is_approval == 162">待{{items.tag_name}}审批</span>
                  <span v-if="items.approvalsov_suggestion == '待审批' && approval_message.approvalsub_message.is_approval == 161">待我审批</span>
                  <span v-else>{{items.user_truename}}</span>
                  <span class="m-grey">{{items.approvalsov_createtime}}</span>
                </p>
                <p class="m-reason" v-if="items.approvalsov_suggestion != '待审批'">
                  {{items.approvalsov_message}}
                </p>
                <template v-if="items.approvalsov_suggestion == '待审批' && approval_message.approvalsub_message.is_approval == 161">
                  <p class="m-margin" >
                    <el-radio-group v-model="form.approvalsov_suggestion">
                      <el-radio label="通过">通过</el-radio>
                      <el-radio label="拒绝">拒绝</el-radio>
                    </el-radio-group>
                  </p>
                  <p>
                    <el-input v-model="form.approvalsov_message" type="textarea" placeholder="请输入审批缘由"></el-input>
                  </p>
                </template>

              </li>
            </ul>
          </div>
        </el-card>
        <div class="m-form-btn m-outside" v-if="approval_message.approvalsub_message.is_approval == 161">
          <span class="active" @click="approvalSure">提交</span>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../../api/api'
    export default {
        data(){
          return{
            approval_message:null,
            dialogImageUrl:'',
            dialogVisible:false,
            form:{
              approvalsov_suggestion:'通过',
              approvalsov_message:''
            }
          }
        },
      mounted(){
          if(this.$route.query.approvalsub_id){
            this.getDetails()
          }else{
            this.$router.go(-1)
          }
      },
      methods:{
        getDetails(){
          axios.get(api.approve_approval_message,{
            params:{
              token:localStorage.getItem('token'),
              approvalsub_id: this.$route.query.approvalsub_id
            }
          }).then(res => {
            if(res.data.status == 200){
              this.approval_message = res.data.data;
            }else{
              this.$message.error(res.data.message);
            }
          })
        },
        //预览
        handlePreviewPic(i,index) {
          this.dialogVisible = true;
          this.dialogImageUrl = this.approval_message.approvalsub_lis[index].element_value[i];
        },
        approvalSure(){
          axios.post(api.approve_approval
            +'?token='+localStorage.getItem('token')
            + '&approvalsub_id='+this.$route.query.approvalsub_id,
            this.form).then(res => {
              if(res.data.status == 200){
                this.getDetails();
                this.$notify({
                  title: '成功',
                  message: res.data.message,
                  type: 'success'
                });
              }else{
                this.$message.error(res.data.message);
              }
          })
        }
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  .m-row{
    margin-top: 20px;
    .m-label{
      color: #BBBBBB;
      display: inline-block;
      width: 100px;
      text-align: right;
    }
    .m-title-name{
      margin-bottom: 20px;
    }
    .m-detail-box{
      display: inline-block;
      padding: 0 10px 20px;
      background-color: #FDFDFD;
      border:1px dashed rgba(216,216,216,1);
      border-radius:8px;
      width: 60%;
      vertical-align: text-top;
    }
    .m-link{
      color: #409EFF;
      text-decoration:underline;
      margin-right: 10px;
    }
    .m-upload-img{
      display: inline-block;
      width: 100px;
      height: 100px;
    }
    .m-reason-ul{
      display: inline-block;
      vertical-align: text-top;
      width: 60%;
      li{
        border-left: 3px solid transparent;
        padding-left: 20px;
        padding-bottom: 0;
        position: relative;

        &.m-agree{
          border-left: 3px solid #34AEFF;
          padding-bottom: 20px;
        }
        &:last-child{
          border-left: 3px solid transparent;
        }
        .m-reason{
          padding: 20px;
          width: 100%;
          background-color: #F7F8FF;
          border:1px dashed rgba(224,224,250,1);
          border-radius:8px;
          margin-top: 20px;
        }
        .m-icon{
          position: absolute;
          top: -1px;
          left: -7.5px;
          background-color: #fff;
        }
        .m-margin{
          padding: 10px 0;
        }
      }
    }
    .el-upload-list--picture-card .el-upload-list__item-actions:hover {
      opacity: 1;
    }
    .m-approval-table{
      border-right: 1px solid #eee;
      border-bottom: 1px solid #eee;
      td{
        border-left: 1px solid #eee;
        border-top: 1px solid #eee;
        text-align: center;
        padding: 10px 0;
      }
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
  }

</style>
