<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>模板列表</span>
        <span class="m-grey">共{{total_count}}条数据</span>
      </div>
      <div class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/module/editModule')">
            <svg-icon icon-class="icon-add" />
            新建模板
          </span>
        <span class="m-title-btn" @click="deleteMould">
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
        @selection-change="handleSelectionChange"
      empty-text="暂无模板">
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
            <span class="m-table-btn" @click="deleteMould(scope.row,'row')">
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
        total_count:0,
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
            this.total_count = res.data.total_count;
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
      pageChange(num){
        this.getMould(num);
        this.page_info.page_num = num;
      },
      /*改变路由*/
      changeRoute(path,item){
        let mould_id = '';
        if(item){
          mould_id = item.mould_id;
        }
        this.$router.push({path:path,query:{mould_id}})
      },
      /*删除*/
      deleteMould(item,name){
        let params = [];
        if(name){
          params.push(item.mould_id)
        }else{
          for(let i=0;i<this.multipleSelection.length;i++){
            params.push(this.multipleSelection[i].mould_id)
          }
        }
        let that = this;
        this.$confirm('确定要删除这些审批流吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(api.delete_mould +'?token='+localStorage.getItem('token'),{
            mould_list:params
          }).then(res => {
            if(res.data.status == 200){
              that.$notify({
                title: '成功',
                message: res.data.message,
                type: 'success'
              });
              that.getMould(that.page_info.page_num);
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
