<template>
    <div>
      <div class="m-title-box">
        <div>
          <span>审批流管理</span>
        </div>
        <div  class="m-title-btn-box">
          <span class="m-title-btn active" @click="changeRoute('/addApprove')">
            <svg-icon icon-class="icon-add" />
            发起审批
          </span>
          <span class="m-title-btn">
            <svg-icon icon-class="icon-delete" />
            批量删除
          </span>
        </div>
      </div>
      <el-tabs type="border-card">
        <el-tab-pane>
          <span slot="label">我发起的审批 <span class="m-tab-num">25</span></span>

          <div class="m-filter-btn-box">
            <span class="m-filter-btn active"> 全部</span>
            <span class="m-filter-btn "> 已审批</span>
            <span class="m-filter-btn "> 待审批</span>
          </div>
          <el-table
            ref="multipleTable"
            :data="tableData3"
            tooltip-effect="dark"
            style="width: 100%"
            @selection-change="handleSelectionChange">
            <el-table-column
              type="selection"
              width="55">
            </el-table-column>
            <el-table-column
              label="审批流名称"
              >
              <template slot-scope="scope">{{ scope.row.date }}</template>
            </el-table-column>
            <el-table-column
              label="提交时间"
            >
              <template slot-scope="scope">{{ scope.row.date }}</template>
            </el-table-column>
            <el-table-column
              label="截止时间"
            >
              <template slot-scope="scope">{{ scope.row.date }}</template>
            </el-table-column>
            <el-table-column
              prop="name"
              label="来源"
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
            <page :total="total_page"></page>
          </div>
        </el-tab-pane>
        <el-tab-pane label="定时任务补偿">
          <span slot="label">我发起的审批 <span class="m-tab-num">25</span></span>
        </el-tab-pane>
      </el-tabs>

    </div>
</template>

<script>
  import page from '../../components/common/page';
    export default {
        data(){
          return{
            tableData3: [{
              date: '2016-05-03',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-02',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-04',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-01',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-08',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-06',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }, {
              date: '2016-05-07',
              name: '王小虎',
              address: '上海市普陀区金沙江路 1518 弄'
            }],
            multipleSelection: [],
            total_page:1
          }
        },
      components:{
        page
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
        changeRoute(v){
          this.$router.push(v)
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
