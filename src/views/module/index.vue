<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>模板列表</span>
        <span class="m-grey">共25条数据</span>
      </div>
      <div class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/module/editModule')">
            <svg-icon icon-class="icon-add" />
            新建板块
          </span>
        <span class="m-title-btn">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
      </div>
    </div>
    <div>
      <el-table
        ref="multipleTable"
        :data="mould_list"
        tooltip-effect="dark"
        style="width: 100%;border-radius: 8px;"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          prop="mould_name"
          label="模块名称"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          align="center"
        >
          <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/module/editModule',scope.row)">
                  <svg-icon icon-class="icon-edit" />
                <span>编辑</span>
              </span>
            <span class="m-table-btn">
                  <svg-icon icon-class="icon-delete" />
                <span>删除</span>
              </span>
          </template>
        </el-table-column>
      </el-table>
      <div class="m-bottom">
        <page :total="total_page"></page>
      </div>

    </div>
  </div>
</template>

<script>
  import page from '../../components/common/page';
  import axios from 'axios';
  import api from '../../api/api';
  export default {
    data(){
      return{
        /*分页信息*/
        page_info:{
          page_num:1,
          page_size:10
        },
        total_page:0,
        mould_list:[],
        multipleSelection: []
      }
    },
    components:{
      page
    },
    mounted(){
      this.getMould(1);
    },
    methods: {
      //获取模板列表
      getMould(num){
        axios.get(api.get_mould_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num,
            page_size: this.page_info.page_size || 10
          }
        }).then(res => {
          if(res.data.status == 200){
            this.mould_list = res.data.data;
            this.total_page = res.data.total_page;
          }
        })
      },

      //表格选择
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      /*改变路由*/
      changeRoute(path,item){
        let mould_id = '';
        if(item){
          mould_id = item.mould_id;
        }
        this.$router.push({path:path,query:{mould_id}})
      },
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
