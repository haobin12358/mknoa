<template>
  <div class="container m-index">
    <div v-if="is_admin">
      <el-row :gutter="24" class="m-index-top">
        <el-col :span="6" :xs="12">
          <el-card class="box-card">
            <p>
              <svg-icon icon-class="icon-card" />
              <span>身份管理</span>
            </p>
            <div class="m-num-box">
              <span class="m-num">{{index_data.len_tag_list}}</span>
              <span>个</span>
            </div>
            <div class="m-index-top-btn m-orange" @click="changeRoute('/role/editRole')">
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
              <span class="m-num">{{index_data.len_user_list}}</span>
              <span>个</span>
            </div>
            <div class="m-index-top-btn m-purple" @click="changeRoute('/account/editAccount')">
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
              <span class="m-grey" @click="changeRoute('/announcement')">查看更多</span>
            </p>
            <div class="m-announcement-box">
              <p class="m-flex-between m-one-announcement" v-for="(item,index) in index_data.notice_message_public" @click="changeRoute('/announcement/editAnnouncement','notice',item)">
                <span>{{item.notice_message}}</span>
                <span>{{item.notice_updatetime}}</span>
              </p>
            </div>
            <div class="m-index-top-btn m-pink" @click="changeRoute('/announcement/editAnnouncement')">
              <span>+ 新建公告</span>
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
              <span class="m-card-btn m-yellow" @click="changeRoute('/approve/editApprove')">+ 新建审批流</span>
            </div>
            <div class="m-scroll">
              <ul class="m-approve-ul">
                <li v-for="(item,index) in index_data.approval_list" @click="changeRoute('/approve/editApprove','approval',item)">
             <span>
               <span>{{item.approval_name}}</span>
                <span class="m-grey">（{{item.approval_level}}）</span>
             </span>
                  <span class="m-grey">{{item.approval_updatetime}}更新</span>
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

              <span class="m-card-btn m-blue" @click="changeRoute('/module/editModule')">+ 新建模板</span>
            </div>
            <div class="m-scroll">
              <ul class="m-template-ul">
                <li v-for="(item,index) in index_data.mould_list" @click="changeRoute('/module/editModule','module',item)">
                  <span>{{item.mould_name}}</span>
                </li>

              </ul>
            </div>

          </el-card>
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <el-row :gutter="24" class="m-index-top">
        <el-col :span="9" :xs="24">
          <el-card class="box-card">
            <p>
              <svg-icon icon-class="icon-approve" />
              <span>我发起的审批</span>
            </p>
            <div class="m-num-box m-normal">
              <div class="m-num-box-one">
                <p>
                  <span class="m-num">{{normal_data.len_wait_my_suggest}}</span>
                  <span>个</span>
                </p>
                <p class="m-alert">待审批</p>
              </div>
              <div  class="m-num-box-one">
                <p>
                  <span class="m-num">{{normal_data.len_sov_my_suggest}}</span>
                  <span>个</span>
                </p>
                <p class="m-alert">已审批</p>
              </div>
            </div>
            <div class="m-index-top-btn m-orange" @click="changeRoute('/allApprove')">
              <span>+ 发起审批</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="9" :xs="24">
          <el-card class="box-card">
            <p>
              <svg-icon icon-class="icon-approve" />
              <span>提交给我的审批</span>
            </p>
            <div class="m-num-box m-normal">
              <div class="m-num-box-one">
                <p>
                  <span class="m-num">{{normal_data.len_wait_my_resove_suggest}}</span>
                  <span>个</span>
                </p>
                <p class="m-alert">待审批</p>
              </div>
              <div  class="m-num-box-one">
                <p>
                  <span class="m-num">{{normal_data.len_sov_my_resove_suggest}}</span>
                  <span>个</span>
                </p>
                <p class="m-alert">已审批</p>
              </div>
            </div>
            <div class="m-index-top-btn m-orange" @click="changeRoute('/allApprove')">
              <span>+ 去审批</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6" :xs="24">
          <el-card class="box-card">
            <p class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-card" />
             <span>身份管理</span>
            </span>

            </p>
            <div class="m-num-box">
              <span class="m-num">{{normal_data.len_tag_list}}</span>
              <span>个</span>
            </div>
            <div class="m-index-top-btn m-orange" @click="changeRoute('/role/editRole')">
              <span>+ 新建身份</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="m-index-bottom">
        <el-col :span="18" :xs="24">
          <el-card class="box-card">
            <div slot="header" class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-announcement" />
              <span>平台公告</span>
            </span>
              <span class="m-grey" @click="changeRoute('/announcement')">查看更多</span>
            </div>
            <div class="m-scroll">
              <ul class="m-approve-ul">
                <li v-for="(item,index) in normal_data.notice_list" @click="changeRoute('/approve/editApprove','approval',item)">
                <div >{{item.notice_message}}
               </div>
                  <span class="m-grey m-time">{{item.notice_updatetime}}</span>
                </li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6" :xs="24">
          <el-card class="box-card">
            <div slot="header" class="m-flex-between">
            <span>
              <svg-icon icon-class="icon-message" />
              <span>短信提醒</span>
            </span>

            </div>
            <div class="m-scroll m-message">
              <p>
                <img src="../../common/images/icon-message.png"  alt="">
              </p>
              <p>
                <span class="m-message-btn">+ 新建短信提醒</span>
              </p>
            </div>

          </el-card>
        </el-col>
      </el-row>
    </div>

  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../../api/api'
  export default {
    name: 'ProfileIndex',

    components: {},

    data() {
      return {
        index_data:null,
        normal_data:null,
        is_admin:false
      }
    },

    computed: {},

    methods: {
      getData(){
        axios.get(api.get_index_message,{
          params:{
            token:localStorage.getItem('token')
          }
        }).then(res => {
            if(res.data.status == 200){
              console.log(res.data.message.indexOf('超级管理员'))
              if(res.data.message.indexOf('超级管理员') != -1){
                this.index_data = res.data.data;
                this.is_admin = true;
              }else{
                this.normal_data = res.data.data;
                this.is_admin = false;
              }

            }
        })
      },
      /*改变路由*/
      changeRoute(path,name,item){
        switch (name){
          case 'notice':
            this.$router.push({path:path,query:{notice_id:item.notice_id}});
            break;
          case 'approval':
            this.$router.push({path:path,query:{approval_id:item.approval_id}});
            break;
          case 'module':
            this.$router.push({path:path,query:{mould_id:item.mould_id}});
            break;
          default:
            this.$router.push({path:path});
        }

      },
    },

    created() {
      this.getData();
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
      &.m-normal{
        display: flex;
        flex-flow: row;
        justify-content: center;
        align-items: center;
        margin: 24px 0;
        .m-alert{
          font-size: 12px;
          color: #B9B9B9;
        }
        .m-num-box-one{
          width: 48%;
          text-align: center;
          &:first-child{
            border-right: 1px solid #eee;
          }
        }
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
        padding: 20px;
        background:rgba(247,248,255,1);
        border-radius:8px;
        display: flex;
        flex-flow: row;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 20px;
        .m-time{
          width: 20%;
          text-align: right;
        }
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
        /*line-height: 130px;*/
        display: flex;
        flex-flow: row;
        align-items: center;
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
  .m-message{
    text-align: center;
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: center;
    img{
      display: block;
      width: 67px;
      height:67px;
      margin-bottom: 20px;
    }
    .m-message-btn{
      padding: 10px 32px;
      color: #fff;
      background:rgba(255,115,115,1);
      border-radius:23px;
      margin-top: 20px;
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
