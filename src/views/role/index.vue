<template>
    <div class="m-role">
      <div class="m-title-box">
        <div>
          <span>身份列表</span>
          <span class="m-grey">共25条数据</span>
        </div>
        <div class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/role/editRole')">
            <svg-icon icon-class="icon-add" />
            新建身份
          </span>
          <span class="m-title-btn" @click="deleteRole">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
        </div>
      </div>
      <div>
        <el-table
          ref="multipleTable"
          :data="role_list"
          tooltip-effect="dark"
          style="width: 100%;border-radius: 8px;"
          @selection-change="handleSelectionChange">
          <el-table-column
            type="selection"
            width="55">
          </el-table-column>
          <el-table-column
            prop="tag_name"
            label="身份名称"
            >
          </el-table-column>
          <el-table-column
            prop="tag_level"
            label="身份等级"
            align="center"
            >
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
            >
            <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/role/editRole',scope.row)">
                  <svg-icon icon-class="icon-edit" />
                <span>编辑</span>
              </span>
              <span class="m-table-btn" @click="deleteRole(scope.row,'row')">
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
              page_size:100
            },
            total_page:0,
            role_list:[],
            multipleSelection: [],

          }
        },
      components:{
          page
      },
      mounted(){
        this.getLevel(1);
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
      /**获取所有身份*/
        getLevel(num){
          axois.get(api.get_tag_list,{
            params:{
              token:localStorage.getItem('token'),
              page_num: num,
              page_size: this.page_info.page_size || 10
            }
          }).then(res => {
              if(res.data.status == 200){
                this.role_list = res.data.data;
                this.total_page = res.data.total_page;
              }else{
                this.$message.error(res.data.message);
              }
          })
        },
        pageChange(num){
          this.getLevel(num);
          this.page_info.page_num = num;
        },
        /*改变路由*/
        changeRoute(path,item){
          let tag_id = '';
          if(item){
              tag_id = item.tag_id;
          }
          this.$router.push({path:path,query:{tag_id}})
        },
        /*删除*/
        deleteRole(item,name){
          let params = [];
          if(name){
            params.push(item.tag_id)
          }else{
            for(let i=0;i<this.multipleSelection.length;i++){
              params.push(this.multipleSelection[i].tag_id)
            }
          }
          let that = this;
          this.$confirm('确定要删除这些身份吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            axois.post(api.delete_tag +'?token='+localStorage.getItem('token'),{
              tag_ids:params
            }).then(res => {
              if(res.data.status == 200){
                that.$notify({
                  title: '成功',
                  message: res.data.message,
                  type: 'success'
                });
                that.getLevel(that.page_info.page_num);
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
