<template>
  <div>
    <div class="m-title-box">
      <div>
        <span>商品管理</span>
      </div>

    </div>
    <el-tabs type="border-card" @tab-click="tabPlaneClick">

      <el-tab-pane label="库存列表">
        <span slot="label">库存列表</span>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
          <el-form-item label="sku编码">
            <el-input v-model="formInline.sku_id" placeholder="sku编码"></el-input>
          </el-form-item>
          <el-form-item label="品牌">
            <el-input v-model="formInline.brand" placeholder="品牌"></el-input>
          </el-form-item>
          <el-form-item label="商品名称">
            <el-input v-model="formInline.i_name" placeholder="商品名称"></el-input>
          </el-form-item>
          <el-form-item label="供应商名称">
            <el-input v-model="formInline.supplier_name" placeholder="供应商名称"></el-input>
          </el-form-item>
          <el-form-item>
            <div class="m-form-btn">
              <span class="active" @click="getProduct(1)">搜索</span>
            </div>
          </el-form-item>
        </el-form>
        <el-table
          ref="multipleTable"
          v-loading="loading"
          :data="product_list"
          tooltip-effect="dark"
          style="width: 100%"
          :fit="true"
          empty-text="暂无商品">
          <!--<el-table-column-->
          <!--type="selection"-->
          <!--width="55">-->
          <!--</el-table-column>-->
          <el-table-column
            prop="i_name"
            label="商品名称"
          >
          </el-table-column>
          <el-table-column
            prop="brand"
            label="商品品牌"
          >
          </el-table-column>
          <el-table-column
            prop="sku_id"
            label="sku编码"
          >
          </el-table-column>
          <el-table-column
            prop="properties_value"
            label="颜色尺寸"
          >
          </el-table-column>
          <el-table-column
            prop="qty"
            label="库存"
          >
          </el-table-column>
          <el-table-column
            prop="supplier_name"
            label="供应商名称"
          >
          </el-table-column>
        </el-table>
        <div class="m-bottom">
          <page :total="total_page_product" @pageChange="pageChangeProduct"></page>
        </div>
      </el-tab-pane>
      <el-tab-pane label="今日销量">
        <span slot="label">今日销量 </span>
        <el-table
          ref="multipleTable"
          v-loading="loading"
          :data="today_sale"
          tooltip-effect="dark"
          style="width: 100%"
          :fit="true"
          empty-text="暂无销量">
          <!--<el-table-column-->
          <!--type="selection"-->
          <!--width="55">-->
          <!--</el-table-column>-->
          <el-table-column
            prop="sku_id"
            label="sku编码"
          >
          </el-table-column>
          <el-table-column
            prop="sale_num"
            label="销售数目"
          >
          </el-table-column>

        </el-table>
        <div class="m-bottom">
          <page :total="total_page_today" @pageChange="pageChangeToday"></page>
        </div>
      </el-tab-pane>
      <el-tab-pane label="历史销售额">
        <span slot="label">历史销售额 </span>
        <el-table
          ref="multipleTable"
          v-loading="loading"
          :data="history_sale"
          tooltip-effect="dark"
          style="width: 100%"
          :fit="true"
          empty-text="暂无审批">
          <!--<el-table-column-->
          <!--type="selection"-->
          <!--width="55">-->
          <!--</el-table-column>-->
          <el-table-column
            prop="sku_id"
            label="sku编码"
          >
          </el-table-column>
          <el-table-column
            prop="sale_num"
            label="销售数目"
          >
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
        //库存
        product_list:[],
        page_info_product:{
          page_num:1,
          page_size:10
        },
        total_page_product:1,
        total_count_product:0,
        loading:false,
        return_approval:[],
        total_page:1,
        total_count:0,
        page_info_my:{
          page_num:1,
          page_size:10
        },
        formInline: {
          sku_id: '',
          brand: '',
          i_name:'',
          supplier_name:''
        },
        //今日销量
        today_sale:[],
        total_page_today:1,
        total_count_today:0,
        page_info_today:{
          page_num:1,
          page_size:10
        },
        //历史销量
        history_sale:[],
        total_page_history:1,
        total_count_history:0,
        page_info_history:{
          page_num:1,
          page_size:10
        },
      }
    },
    components:{
      page
    },
    mounted(){
      this.getList();
      this.getProduct(1);
      // this.getToday(1);
      // this.getApproval(1,'全部');
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

      changeRoute(v,item){
        this.$router.push({path:v,query:{approvalsub_id:item.approvalsub_id}})
      },
      //  获取商品列表
      getProduct(num){
        this.loading = true;
        axios.get(api.get_product_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num || this.page_info_product.page_num,
            page_size:this.page_info_product.page_size,
            sku_id: this.formInline.sku_id,
            brand: this.formInline.brand,
            i_name: this.formInline.i_name,
            supplier_name: this.formInline.supplier_name,
          }
        }).then(res => {
          if(res.data.status == 200){
            this.product_list = res.data.data;
            this.total_page_product = res.data.total_page;
            this.loading = false;
            this.total_count_product = res.data.total_count;

          }else{
            this.loading = false;
            this.$message.error(res.data.message);
          }
        })
      },
      //  获取今日销量
      getToday(num){
        this.loading = true;
        axios.get(api.get_qyt_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num || this.page_info_today.page_num,
            page_size:this.page_info_today.page_size
          }
        }).then(res => {
          if(res.data.status == 200){
            this.today_sale = res.data.data;
            this.total_page_today = res.data.total_page;
            this.loading = false;
            this.total_count_today = res.data.total_count;

          }else{
            this.loading = false;
            this.$message.error(res.data.message);
          }
        })
      },
      pageChangeProduct(num){

          this.getProduct(num);
        this.page_info_product.page_num = num;
      },
      pageChangeToday(num){
        this.getToday(num);
        this.page_info_today.page_num = num;
      },
      //  获取历史销量批
      getHistory(num,state){
        this.loading = true;
        axios.get(api.get_qyt_list,{
          params:{
            token:localStorage.getItem('token'),
            page_num: num || this.page_info_history.page_num,
            page_size:this.page_info_history.page_size,
          }
        }).then(res => {
          if(res.data.status == 200){
            this.history_sale = res.data.data;
            this.total_page_history = res.data.total_page;
            this.loading = false;
            if(state == '全部'){
              this.total_count_history = res.data.total_count;
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
        this.page_info_product.page_num = num;
      },
      //我发起的和我审批的切换点击
      tabPlaneClick(tab){
        if(tab.label == '库存列表'){
          this.getProduct(1);
        }else if(tab.label == '今日销量'){
          this.getToday(1);
        }else{
          this.getHistory(1);
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
