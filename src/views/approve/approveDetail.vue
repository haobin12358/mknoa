<template>
  <div >
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/allApprove' }">审批流管理</el-breadcrumb-item>
      <el-breadcrumb-item>审批流名称</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="m-row">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <el-card class="box-card">
          <h3 class="m-title-name">审批流名称</h3>
          <el-row >
            <el-col :xs="24" :sm="6" :md="4" :lg="4" :xl="4">
              <span class="m-label">来源：</span>
              <span>鹿野野</span>
            </el-col>
            <el-col :xs="24" :sm="6" :md="6" :lg="6" :xl="6">
              <span class="m-label">申请时间：</span>
              <span>2018-12-09 12:30</span>
            </el-col>
            <el-col :xs="24" :sm="6" :md="8" :lg="8" :xl="8">
              <span class="m-label">截止时间：</span>
              <span>2018-12-09 12:30</span>
            </el-col>
          </el-row>
         <p class="m-row">
           <span class="m-label">联系方式：</span>
           <span>15912345678</span>
         </p>
          <div class="m-row">
            <span class="m-label">详情：</span>
            <div class="m-detail-box">
              <p class="m-row">
                <span class="m-label">申请人：</span>
                <span>15912345678</span>
              </p>
              <p class="m-row">
                <span class="m-label">请假时间：</span>
                <span>15912345678</span>
              </p>
              <p class="m-row">
                <span class="m-label">相关附件：</span>
                <a href="#" class="m-link"> dddd</a>
                <a href="#" class="m-link"> dddd</a>
              </p>
            </div>
          </div>
          <div class="m-row">
            <span class="m-label">上级意见：</span>
            <ul class="m-reason-ul">
              <li class="m-agree">
                <svg-icon icon-class="icon-agree" class="m-icon"/>
                <p class="m-mr">
                  <span>A领导</span>
                  <span class="m-grey">2018-12-09 12:30</span>
                </p>
                <p class="m-reason">
                  同意
                </p>
              </li>
              <li class="m-agree">
                <svg-icon icon-class="icon-agree" class="m-icon"/>
                <p class="m-mr">
                  <span>A领导</span>
                  <span class="m-grey">2018-12-09 12:30</span>
                </p>
                <p class="m-reason">
                  同意
                </p>
              </li>
              <li >
                <svg-icon icon-class="icon-wait" class="m-icon"/>
                <!--<svg-icon icon-class="icon-refuse" class="m-icon"/>-->
                <p>
                  待我审批
                </p>
                <p class="m-margin">
                  <el-radio-group v-model="radio2">
                    <el-radio :label="3">同意</el-radio>
                    <el-radio :label="6">拒绝</el-radio>
                  </el-radio-group>
                </p>
                <p>
                  <el-input v-model="input" type="textarea" placeholder="请输入审批缘由"></el-input>
                </p>
              </li>
            </ul>
          </div>
        </el-card>
        <div class="m-form-btn m-outside">
          <span class="active">提交</span>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
    export default {
        data(){
          return{
            radio2:3,
            input:''
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
  }
</style>
