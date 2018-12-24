<template>
  <div id="app">
    <router-view v-if="isRouterAlive"/>
  </div>
</template>

<script>
export default {
  name: 'App',
  provide(){
    return {
      reload: this.reload
    }
  },
  data(){
    return {
      isRouterAlive: true
    }
  },
  computed:{
    cachedViews() {
      return this.$store.state.tagsView.cachedViews
    },
    key() {
      return this.$route.fullPath
    },
  },
  methods:{
    reload(){
      this.isRouterAlive = false;
      this.$nextTick(function () {
        this.isRouterAlive = true;
      })
    }
  },
  created(){
    this.$store.commit('InitInfo');
  }
}
</script>
