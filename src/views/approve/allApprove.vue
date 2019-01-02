<template>
    <div>
      <div class="m-title-box">
        <div>
          <span>审批流管理</span>
        </div>
        <div  class="m-title-btn-box">

          <el-dropdown :hide-on-click="false" trigger="click" @command="handleCommand">
             <span class="m-title-btn active">
              <svg-icon icon-class="icon-add" />
              发起审批
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-for="item in approval_list" :command="item" :key="item.approval_id">{{item.approval_name}}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span class="m-title-btn">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
        </div>
      </div>
      <el-tabs type="border-card" @tab-click="tabPlaneClick">

        <el-tab-pane label="我发起的审批">
          <span slot="label">我发起的审批 <span class="m-tab-num" v-if="total_count_my > 0">{{total_count_my}}</span></span>

          <div class="m-filter-btn-box">
            <span class="m-filter-btn " :class="item.active?'active':''" v-for="(item,index) in tab_list_my" @click="tabClick(item,index,'tab_list_my','my')">{{item.name}}</span>
          </div>
          <el-table
            ref="multipleTable"
            v-loading="loading"
            :data="my_approval"
            tooltip-effect="dark"
            style="width: 100%"
            :fit="true"
            @selection-change="handleSelectionChange">
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
            <el-table-column
              prop="approval_name"
              label="审批流名称"
              >
            </el-table-column>
            <el-table-column
              prop="approvalsub_createtime"
              label="提交时间"
            >
            </el-table-column>
            <el-table-column
              prop="approvalsub_endtime"
              label="截止时间"
            >
            </el-table-column>
            <el-table-column
              prop="user_truename"
              label="发起人"
              width="100"
            >
            </el-table-column>
            <el-table-column
              prop="approvalsub_status"
              label="状态"
              width="100"
              >
            </el-table-column>
            <el-table-column
              prop="address"
              label="操作"
              align="center"

            >
              <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/approveDetail')">
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
            <page :total="total_page_my" @pageChange="pageChangeMy"></page>
          </div>
        </el-tab-pane>
        <el-tab-pane label="我收到的审批">
          <span slot="label">我收到的审批 <span class="m-tab-num" v-if="total_count > 0">{{total_count}}</span></span>
          <div class="m-filter-btn-box">
            <span class="m-filter-btn " :class="item.active?'active':''" v-for="(item,index) in tab_list" @click="tabClick(item,index,'tab_list')">{{item.name}}</span>
          </div>
          <el-table
            ref="multipleTable"
            v-loading="loading"
            :data="return_approval"
            tooltip-effect="dark"
            style="width: 100%"
            :fit="true"
            @selection-change="handleSelectionChange">
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
            <el-table-column
              prop="approval_name"
              label="审批流名称"
            >
            </el-table-column>
            <el-table-column
              prop="approvalsub_createtime"
              label="提交时间"
            >
            </el-table-column>
            <el-table-column
              prop="approvalsub_endtime"
              label="截止时间"
            >
            </el-table-column>
            <el-table-column
              prop="user_truename"
              label="发起人"
              width="100"
            >
            </el-table-column>
            <el-table-column
              prop="approvalsub_status"
              label="状态"
              width="100"
            >
            </el-table-column>
            <el-table-column
              prop="address"
              label="操作"
              align="center"

            >
              <template slot-scope="scope">
              <span class="m-table-btn" @click="changeRoute('/approveDetail')">
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
        </el-tab-pane>
      </el-tabs>

    </div>
</template>

<script>
  import page from '../../components/common/page';
  import axios from 'axios';
  import api from '../../api/api';
      export default {
        data(){
          return{
            approval_list:[],
            my_approval:[],
            loading:false,
            tab_list_my:[
              {
                name:'全部',
                value:'全部',
                active:true
              },
              {
                name:'已审批',
                value:'已审批',
                active:false
              },
              {
                name:'待审批',
                value:'未审批',
                active:false
              }
            ],
            return_approval:[],
            tab_list:[
              {
                name:'全部',
                value:'全部',
                active:true
              },
              {
                name:'已审批',
                value:'已审批',
                active:false
              },
              {
                name:'待审批',
                value:'未审批',
                active:false
              }
            ],
            total_page:1,
            total_count:0,
            page_info:{
              page_num:1,
              page_size:10
            },
            multipleSelection: [],
            total_page_my:1,
            total_count_my:0,
            page_info_my:{
              page_num:1,
              page_size:10
            }
          }
        },
      components:{
        page
      },
        mounted(){
          this.getList();
          this.getMyApproval(1,'全部');
        },
      methods: {
        /*获取可创建的审批流列表*/
        getList(){
          axios.get(api.get_my_approval_list,{
            params:{
              token:localStorage.getItem('token')
            }
          }).then(res => {
            if(res.data.status == 200){
              this.approval_list = res.data.data;
            }else{
              this.$message.error(res.data.message);
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
        changeRoute(v){
          this.$router.push(v)
        },
        //发起审批
        handleCommand(item){
          this.$router.push({path:'/addApprove',query:{approval_id:item.approval_id}});
        },
        //全部，待审批点击
        tabClick(item,index,list,name){
          let arr = [].concat(this[list]);
          for(let i = 0;i<arr.length;i++){
            arr[i].active = false;
          }
          arr[index].active = true;
          this[list] = [].concat(arr);
          if(name ==  'my'){
            this.getMyApproval(this.page_info_my.page_num,item.value);
          }else{
            this.getApproval(this.page_info.page_num,item.value);
          }
        },
      //  获取我发起的审批
        getMyApproval(num,state){
          this.loading = true;
          axios.get(api.my_approve_approval_list,{
            params:{
              token:localStorage.getItem('token'),
              page_num: num || this.page_info_my.page_num,
              page_size:this.page_info_my.page_size,
              approvalsov_suggestion:state
            }
          }).then(res => {
            if(res.data.status == 200){
              this.my_approval = res.data.data;
              this.total_page_my = res.data.total_page;
              this.loading = false;
              if(state == '全部'){
                this.total_count_my = res.data.total_count;
              }

            }else{
              this.loading = false;
              this.$message.error(res.data.message);
            }
          })
        },
        pageChangeMy(num){
          for(let i =0;i<this.tab_list_my.length;i++){
            if(this.tab_list_my[i].active){
              this.getMyApproval(num,this.tab_list_my[i].value);
            }
          }
          this.page_info_my.page_num = num;
        },
        //  获取我收到的审批
        getApproval(num,state){
          this.loading = true;
          axios.get(api.approve_approval_list,{
            params:{
              token:localStorage.getItem('token'),
              page_num: num || this.page_info.page_num,
              page_size:this.page_info.page_size,
              approvalsov_suggestion:state
            }
          }).then(res => {
            if(res.data.status == 200){
              this.return_approval = res.data.data;
              this.total_page = res.data.total_page;
              this.loading = false;
              if(state == '全部'){
                this.total_count = res.data.total_count;
              }

            }else{
              this.loading = false;
              this.$message.error(res.data.message);
            }
          })
        },
        pageChange(num){
          for(let i =0;i<this.tab_list.length;i++){
            if(this.tab_list[i].active){
              this.getApproval(num,this.tab_list[i].value);
            }
          }
          this.page_info.page_num = num;
        },
        //我发起的和我审批的切换点击
        tabPlaneClick(tab){
          if(tab.label == '我发起的审批'){
            this.getMyApproval(1,'全部');
          }else{
            this.getApproval(1,'全部');
          }
        }
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  .m-tab-num{
    display: inline-block;
    width: 21px;
    height: 21px;
    line-height: 21px;
    border-radius: 50%;
    background-color: #CDCDCD;
    color: #fff;
    margin-left: 10px;
    text-align: center;
  }
  .el-tabs--border-card>.el-tabs__header .el-tabs__item.is-active{
    .m-tab-num{
      background-color: #FF7373;
    }
  }
  .m-filter-btn-box{
    .m-filter-btn{
      display: inline-block;
      padding: 4px 22px;
      color: #FF7373;
      border: 1px solid #FF7373;
      border-radius: 19px;
      margin-right: 10px;
      cursor: pointer;
      &.active{
        background-color: #FF7373;
        color: #fff;
      }
    }
  }
</style>
