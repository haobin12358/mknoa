<template>
  <div class="container m-index">
    <el-row :gutter="24" class="m-index-top">
      <el-col :span="6" :xs="12">
        <el-card class="box-card">
          <p>
            <svg-icon icon-class="icon-card" />
            <span>身份管理</span>
          </p>
          <div class="m-num-box">
            <span class="m-num">25</span>
            <span>个</span>
          </div>
          <div class="m-index-top-btn m-orange">
            <span>+ 新建身份</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6" :xs="12">
        <el-card class="box-card">
          <p>
            <svg-icon icon-class="icon-people" />
            <span>账号管理</span>
          </p>
          <div class="m-num-box">
            <span class="m-num">25</span>
            <span>个</span>
          </div>
          <div class="m-index-top-btn m-purple">
            <span>+ 新建账号</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12" :xs="24">
        <el-card class="box-card">
          <p class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-announcement" />
             <span>公告管理</span>
            </span>
            <span class="m-grey">查看更多</span>
          </p>
          <div class="m-announcement-box">
            <p class="m-flex-between m-one-announcement">
              <span>关于批发系统12月31日停止运营的业务公告</span>
              <span>2018-12-01</span>
            </p>
            <p class="m-flex-between m-one-announcement">
              <span>关于批发系统12月31日停止运营的业务公告</span>
              <span>2018-12-01</span>
            </p>
          </div>
          <div class="m-index-top-btn m-pink">
            <span>+ 新建广告</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="m-index-bottom">
      <el-col :span="12" :xs="24">
        <el-card class="box-card">
          <div slot="header" class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-approve" />
              <span>审批流管理</span>
            </span>
            <span class="m-card-btn m-yellow">+ 新建审批流</span>
          </div>
          <div class="m-scroll">
            <ul class="m-approve-ul">
              <li>
             <span>
               <span>审批流名称1</span>
                <span class="m-grey">（已设置多级审批）</span>
             </span>
                <span class="m-grey">2018-12-01更新</span>
              </li>
              <li>
             <span>
               <span>审批流名称1</span>
                <span class="m-grey">（已设置多级审批）</span>
             </span>
                <span class="m-grey">2018-12-01更新</span>
              </li>
              <li>
             <span>
               <span>审批流名称1</span>
                <span class="m-grey">（已设置多级审批）</span>
             </span>
                <span class="m-grey">2018-12-01更新</span>
              </li>
              <li>
             <span>
               <span>审批流名称1</span>
                <span class="m-grey">（已设置多级审批）</span>
             </span>
                <span class="m-grey">2018-12-01更新</span>
              </li>
              <li>
             <span>
               <span>审批流名称1</span>
                <span class="m-grey">（已设置多级审批）</span>
             </span>
                <span class="m-grey">2018-12-01更新</span>
              </li>
            </ul>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12" :xs="24">
        <el-card class="box-card">
          <div slot="header" class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-moban" />
              <span>模板管理</span>
            </span>

            <span class="m-card-btn m-blue">+ 新建模板</span>
          </div>
          <div class="m-scroll">
            <ul class="m-template-ul">
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
              <li>
                <span>模板名称1</span>
              </li>
            </ul>
          </div>

        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: 'ProfileIndex',

    components: {},

    data() {
      return {}
    },

    computed: {},

    methods: {},

    created() {

    }
  }
</script>

<style lang="less" scoped>
  @import "../../styles/myIndex";
.m-index{
  .m-index-top{
    .box-card{
      height: 213px;
    }
    .m-num-box{
      text-align: center;
      margin: 30px 0;
      .m-num{
        font-size: 55px;
      }
    }
    .m-index-top-btn{
      padding: 15px 0 0;
      text-align: center;
      border-top: 1px solid #F5F6FF;
      font-size: 13px;
      cursor: pointer;
      &.m-orange{
        color: #FC9E21;
      }
      &.m-purple{
        color: #7D5D99;
      }
      &.m-pink{
        color: #E55982;
      }
    }
    .m-announcement-box{
      .m-one-announcement{
        height:38px;
        line-height: 38px;
        background:rgba(247,248,255,1);
        border-radius:8px;
        padding: 0 20px;
        margin-bottom: 18px;
        color: #B9B9B9;
        font-size: 12px;
        &:first-child{
          margin-top: 20px;
          margin-bottom: 10px;
        }
      }
    }
  }
  .m-index-bottom{
    margin-top: 20px;
    .box-card{
      height: 405px;
    }
    .m-card-btn{
      display: block;
      padding: 8px 20px;
      border-radius: 23px;
      font-size: 13px;
      &.m-yellow{
        color: #F0BA9D;
        border: 1px solid #F0BA9D;
      }
      &.m-blue{
        color: #01ABFD;
        border: 1px solid #01ABFD;
      }
    }
    .m-scroll{
      height: 300px;
      overflow-y: auto;
    }
    .m-approve-ul{
      li{
        height:56px;
        line-height: 56px;
        background:rgba(247,248,255,1);
        padding: 0 10px;
        border-radius:8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
      }
    }
    .m-template-ul{
      display: flex;
      flex-flow: row;
      align-items: center;
      justify-content: flex-start;
      flex-wrap: wrap;
      li{
        width: 130px;
        height: 130px;
        background:rgba(247,248,255,1);
        line-height: 130px;
        border-radius:8px;
        text-align: center;
        margin-right: 16px;
        margin-bottom: 20px;
        &:nth-child(4n){
          margin-right: 0;
        }
      }
    }
  }
}
  /*定义滚动条高宽及背景 高宽分别对应横竖滚动条的尺寸*/
  .m-scroll::-webkit-scrollbar
  {
    width: 4px;
    height: 4px;
    background-color: #F5F5F5;
  }

  /*定义滚动条轨道 内阴影+圆角*/
  .m-scroll::-webkit-scrollbar-track
  {
    -webkit-box-shadow: inset 0 0 2px #fff;
    border-radius: 20px;
    background-color: #Fff;
  }

  /*定义滑块 内阴影+圆角*/
  .m-scroll::-webkit-scrollbar-thumb
  {
    border-radius: 20px;
    -webkit-box-shadow: inset 0 0 6px #BBBBBB;
    background-color: #fff;
  }
</style>
