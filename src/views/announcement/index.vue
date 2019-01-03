<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>公告列表</span>
        <span class="m-grey">共{{total_count}}条数据</span>
      </div>
      <div class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/announcement/editAnnouncement')">
            <svg-icon icon-class="icon-add" />
            新建公告
          </span>
        <span class="m-title-btn" @click="deleteAnnouncement">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
      </div>
    </div>
    <div>
      <el-table
        ref="multipleTable"
        :data="announcement_list"
        tooltip-effect="dark"
        style="width: 100%;border-radius: 8px;"
        @selection-change="handleSelectionChange"
        empty-text="暂无公告">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          prop="notice_title"
          label="标题"
        >
        </el-table-column>
        <el-table-column
          prop="notice_message"
          label="内容"
        >
        </el-table-column>
        <el-table-column
          prop="notice_updatetime"
          label="发布时间"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          align="center"
        >
          <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/announcement/editAnnouncement',scope.row)">
                  <svg-icon icon-class="icon-edit" />
                <span>编辑</span>
              </span>
            <span class="m-table-btn" @click="deleteAnnouncement(scope.row,'row')">
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
        announcement_list:[],
        multipleSelection: [],
      }
    },
    components:{
      page
    },
    mounted(){
      this.getAnnouncement(1)
    },
    methods: {
      //获取公告列表
      getAnnouncement(num){
        axios.get(api.get_notice_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num:num,
            page_size:this.page_info.page_size || 10
          }
        }).then(res =>{
           if(res.data.status == 200){
             this.announcement_list = res.data.data;
             this.total_page = res.data.total_page;
             this.total_count = res.data.total_count;
           }
        })
      },
      /*分页*/
      pageChange(num){
        this.getAnnouncement(num);
        this.page_info.page_num = num;
      },
      /*改变路由*/
      changeRoute(path,item){
        let notice_id = '';
        if(item){
          notice_id = item.notice_id;
        }
        this.$router.push({path:path,query:{notice_id}})
      },
      //表格多选操作
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
      /*删除*/
      deleteAnnouncement(item,name){
        let params = [];
        if(name){
          params.push(item.notice_id)
        }else{
          for(let i=0;i<this.multipleSelection.length;i++){
            params.push(this.multipleSelection[i].notice_id)
          }
        }
        let that = this;
        this.$confirm('确定要删除这些身份吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(api.delete_notice +'?token='+localStorage.getItem('token'),{
            notice_list:params
          }).then(res => {
            if(res.data.status == 200){
              that.$notify({
                title: '成功',
                message: res.data.message,
                type: 'success'
              });
              that.getAnnouncement(that.page_info.page_num);
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
