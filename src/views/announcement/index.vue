<template>
  <div class="m-role">
    <div class="m-title-box">
      <div>
        <span>公告列表</span>
        <span class="m-grey">共25条数据</span>
      </div>
      <div class="m-title-btn-box">
          <span class="m-title-btn active">
            <svg-icon icon-class="icon-add" />
            新建公告
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
        :data="tableData3"
        tooltip-effect="dark"
        style="width: 100%;border-radius: 8px;"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          label="标题"
        >
          <template slot-scope="scope">{{ scope.row.date }}</template>
        </el-table-column>
        <el-table-column
          label="内容"
        >
          <template slot-scope="scope">是</template>
        </el-table-column>
        <el-table-column
          prop="address"
          label="操作"
          align="center"
        >
          <template slot-scope="scope">
              <span class="m-table-btn">
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
        total_page:3
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
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
