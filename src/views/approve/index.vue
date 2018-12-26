<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>审批流列表</span>
        <span class="m-grey">共25条数据</span>
      </div>
      <div  class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/approve/editApprove')">
            <svg-icon icon-class="icon-add" />
            新建审批流
          </span>
        <span class="m-title-btn" @click="deleteApprove">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
      </div>
    </div>
    <div>
      <el-table
        ref="multipleTable"
        :data="approve_list"
        tooltip-effect="dark"
        style="width: 100%;border-radius: 8px;"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          label="审批流名称"
          prop="approval_name"
        >
        </el-table-column>
        <el-table-column
          label="是否设置多级审批"
        >
          <template slot-scope="scope">是</template>
        </el-table-column>
        <el-table-column
          prop="address"
          label="操作"
          align="center"
        >
          <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/approve/editApprove',scope.row)">
                  <svg-icon icon-class="icon-edit" />
                <span>编辑</span>
              </span>
            <span class="m-table-btn" @click="deleteApprove(scope.row,'row')">
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
        approve_list:[],
        multipleSelection: []
      }
    },
    components:{
      page
    },
    mounted(){
      this.getApprove(1);
    },
    methods: {
      //获取审批列表
      getApprove(num){
        axios.get(api.approval_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num,
            page_size: this.page_info.page_size || 10
          }
        }).then(res => {
          if(res.data.status == 200){
            this.approve_list = res.data.data;
            this.total_page = res.data.total_page;
          }
        })
      },
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
        let approval_id = '';
        if(item){
          approval_id = item.approval_id;
        }
        this.$router.push({path:path,query:{approval_id}})
      },
      pageChange(num){
        this.getMould(num);
        this.page_info.page_num = num;
      },
      /*删除*/
      deleteApprove(item,name){
        let params = [];
        if(name){
          params.push(item.approval_id)
        }else{
          for(let i=0;i<this.multipleSelection.length;i++){
            params.push(this.multipleSelection[i].approval_id)
          }
        }
        let that = this;
        this.$confirm('确定要删除这些审批流吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(api.delete_approval +'?token='+localStorage.getItem('token'),{
            approval_list:params
          }).then(res => {
            if(res.data.status == 200){
              that.$notify({
                title: '成功',
                message: res.data.message,
                type: 'success'
              });
              that.getApprove(that.page_info.page_num);
            }else{
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
