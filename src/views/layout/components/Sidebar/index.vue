<template>

  <el-scrollbar wrap-class="scrollbar-wrapper">
    <div class="m-role-box">
      <img src="../../../../common/images/icon-role.png" class="m-role-img" alt="">
      <h3 class="m-role-name">{{userInfo.user_name}}</h3>
      <!--<p>超级管理员</p>-->
    </div>
    <el-menu
      :show-timeout="200"
      :default-active="$route.path"
      :collapse="isCollapse"
      mode="vertical"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <sidebar-item v-for="route in side" :key="Math.random()" :item="route" :base-path="route.power_path"/>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'

export default {
  components: { SidebarItem },
  computed: {
    ...mapGetters([
      // 'permission_routers',
      'userInfo',
      'sidebar',
      'side'
    ]),
    routes() {
      return this.$router.options.routes
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  },
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
  .m-role-box{
    text-align: center;
    padding: 40px 0;
    background-color: rgb(48, 65, 86);
    font-size: 12px;
    color: #fff;
    .m-role-img{
      display: inline-block;
      width: 90px;
      height: 90px;
    }
    .m-role-name{
      font-size: 14px;
      font-weight: normal;
    }
  }
</style>
