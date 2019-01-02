<template>
  <div class="container">
    <el-autocomplete prefix-icon="el-icon-menu" placeholder="请输入菜单名" v-model="searchTxt" size="medium"
                     value-key="title"  :fetch-suggestions="querySearch" @select="selectMenu" clearable>
    </el-autocomplete>
  </div>
</template>

<script>
  import {mapGetters} from "vuex";


  export default {
    name: "MenuSearch",

    components: {},

    data() {
      return {
        searchTxt: '',
      }
    },

    computed: {
      ...mapGetters(['side']),
      menuList(){
        let rst = [];

        for (let i = 0; i < this.side.length; i++) {
          if(this.side[i].children){
            for (let j = 0; j < this.side[i].children.length; j++) {
              if(!this.side[i].children[j].hidden){
                rst.push({
                  path: this.side[i].power_path + '/' + this.side[i].children[j].power_path,
                  title: this.side[i].children[j].power_meta.powermeta_title
                })
              }
            }
          }else{
          }
        }

        return rst;
      }
    },

    methods: {
      querySearch(queryString, cb) {
        let searchRes =  this.menuList.filter(item => item.title.toLowerCase().indexOf(queryString.toLowerCase()) !== -1)

        cb(searchRes);
      },
      selectMenu(menu){
        this.$router.push(menu.path)
      },
    },

    created() {

    },
  }
</script>

<style lang="less" scoped>
  @import "../../styles/myIndex";

  .container {

  }
</style>
