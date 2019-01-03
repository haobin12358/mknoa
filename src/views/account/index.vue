<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>账号列表</span>
        <span class="m-grey">共{{total_count}}条数据</span>
      </div>
      <div class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/account/editAccount')">
            <svg-icon icon-class="icon-add" />
            新建账号
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
        :data="user_list"
        tooltip-effect="dark"
        style="width: 100%;border-radius: 8px;"
        @selection-change="handleSelectionChange"
        empty-text="暂无账号">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          label="账号"
        >
          <template slot-scope="scope">{{ scope.row.user_name }}</template>
        </el-table-column>
        <el-table-column
          prop="user_telphone"
          label="联系方式"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="user_level"
          label="身份等级"
          align="center"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          align="center"
        >
          <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/account/editAccount',scope.row)">
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
        <page :total="total_page" @pageChange="pageChange"></page>
      </div>

    </div>
  </div>
</template>

<script>
  import page from '../../components/common/page';
  import axois from 'axios';
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
        total_count:0,
        user_list:[],
        multipleSelection: [],
      }
    },
    components:{
      page
    },
    mounted(){
      this.getUser(1);
    },
    methods: {
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
      /**获取所有用户*/
      getUser(num){
        axois.get(api.get_all_user,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num,
            page_size: this.page_info.page_size || 10
          }
        }).then(res => {
            if(res.data.status == 200){
              this.total_page = res.data.total_page;
              this.user_list = res.data.data;
              this.total_count = res.data.total_count;
            }else{
              this.$message.error(res.data.message);
            }
        })
      },
      /*分页*/
      pageChange(num){
        this.getUser(num);
        this.page_info.page_num = num;
      },
      /*改变路由*/
      changeRoute(path,item){
        let user_id = '';
        if(item){
          user_id = item.user_id;
        }
        this.$router.push({path:path,query:{user_id}})
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
