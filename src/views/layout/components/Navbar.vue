<template>
  <el-menu class="navbar" mode="horizontal">
    <hamburger :toggle-click="toggleSideBar" :is-active="sidebar.opened" class="hamburger-container"/>
    <breadcrumb/>

    <div class="right-menu-wrap">
<!--v-if="device!=='mobile'"-->
      <template >
        <menu-search v-if="device!=='mobile'"></menu-search>
        <error-log class="errLog-container right-menu-item"/>
        <!--<span class="m-card-btn " @click="logout">-->
            <!--<svg-icon icon-class="icon-exit" />-->
          <!--退出</span>-->
        <!--<el-tooltip content="全屏" effect="dark" placement="bottom">-->
          <!--<screenfull class="screenfull right-menu-item"/>-->
        <!--</el-tooltip>-->
        <el-dropdown class="avatar-container" trigger="click" @command="handleCommand">
          <div class="avatar-wrapper">
            <!--<img v-lazy="userInfo.adheader" class="user-avatar">-->

            <!--<svg-icon icon-class="icon-per" />-->
            <img src="../../../common/images/icon-personal.png" class="m-icon-personal" />
          </div>
          <el-dropdown-menu slot="dropdown" class="user-dropdown">
            <el-dropdown-item command="pwd">
              修改密码
            </el-dropdown-item>
            <el-dropdown-item command="logout" divided>
              退出系统
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </template>


    </div>


    <change-pwd ref="changePwd"></change-pwd>
  </el-menu>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import Breadcrumb from 'src/components/Breadcrumb'
  import Hamburger from 'src/components/Hamburger'
  import ErrorLog from 'src/components/ErrorLog'
  import Screenfull from 'src/components/Screenfull'
  import SizeSelect from 'src/components/SizeSelect'
  import ChangePwd from 'src/views/setting/changePwd'
  import MenuSearch from 'src/components/MenuSearch'

  export default {
    components: {
      Breadcrumb,
      Hamburger,
      ErrorLog,
      Screenfull,
      SizeSelect,
      ChangePwd,
      MenuSearch
    },
    computed: {
      ...mapGetters([
        'sidebar',
        'avatar',
        'device',
        'userInfo'
      ])
    },
    methods: {
      toggleSideBar() {
        this.$store.dispatch('ToggleSideBar')
      },
      handleCommand(command) {
        switch (command) {
          case 'pwd':
            this.$refs.changePwd.showDialog();
            break
          case 'logout':
            this.logout()
            break
          default:
            break
        }
      },
      logout() {
        this.$confirm('确认要退出当前登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$store.dispatch('LogOut').then(() => {
            // location.reload() // 为了重新实例化vue-router对象 避免bug
            this.$router.push('/');
          })

        }).catch(() => {

        });

      }
    }
  }
</script>

<style lang="less" scoped>
  @import "../../../styles/myIndex";

  .navbar {
    height: 50px;
    line-height: 50px;
    border-radius: 0px !important;
    .hamburger-container {
      line-height: 58px;
      height: 50px;
      float: left;
      padding: 0 10px;
    }

    .right-menu-wrap {
      float: right;
      height: 100%;
      .fj(flex-end);
      align-items: center;

      &:focus {
        outline: none;
      }
      .right-menu-item {
        display: inline-block;
        margin: 0 8px;
      }
      .screenfull {
        height: 20px;
      }
      .international {
        vertical-align: top;
      }
      .theme-switch {
        vertical-align: 15px;
      }
      .avatar-container {
        height: 50px;
        margin-right: 30px;
        margin-left: 10px;
        cursor: pointer;

        .avatar-wrapper {
          margin-top: 5px;
          /*position: relative;*/
          //.fj();
          /*align-items: center;*/
          height: 40px;

          .user-avatar {
            width: 40px;
            border-radius: 10px;
          }
          .el-icon-caret-bottom {
            cursor: pointer;
            position: absolute;
            right: -20px;
            top: 25px;
            font-size: 12px;
          }
        }

      }
      .m-card-btn{
        display: block;
        padding: 8px 20px;
        border-radius: 23px;
        font-size: 13px;
        color: #666666;
        border: 1px solid #888888;
        line-height: normal;
      }
      .m-icon-personal{
        display: inline-block;
        width: 30px;
        height: 30px;
        vertical-align: text-bottom;
      }
    }

  }
</style>

