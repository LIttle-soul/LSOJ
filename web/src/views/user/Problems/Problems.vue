
<template>
  <el-card style="margin-top: 60px;">
    <template #header>
      <div>
        <span>问题列表</span>
      </div>
    </template>
    <div>
    <el-table
    :data="Data | dataslice"
    size="mini"
    style="width: 100%;"
    :row-class-name="tableRowClassName"
    :default-sort="{prop: 'problem_id', order: 'aescending'}">
    <el-table-column
      prop="problem_id"
      label="编号"
      sortable
      width="80">
    </el-table-column>
    <el-table-column
      prop="tittle"
      label="题目"
      width="350">
    </el-table-column>
    <el-table-column
      prop="tag"
      label="标签"
      width="200">
      <template #default="scope">
        <el-tag
          :type="scope.row.tag === '基础题' ? 'primary' : 'success'"
          disable-transitions>{{scope.row.tag}}</el-tag>
      </template>
    </el-table-column>
    <el-table-column
      prop="degree"
      :filters="[
        { text: '一星', value: 1},
        { text: '二星', value: 2},
        { text: '三星', value: 3},
        { text: '四星', value: 4},
        { text: '五星', value: 5},
      ]"
      label="难度">
      <template #default="scope">
        <el-rate
          v-model="scope.row.degree"
          disabled
        ></el-rate>
      </template>
    </el-table-column>
    <el-table-column
      prop="solved"
      sortable
      label="正确">
    </el-table-column>
    <el-table-column
      prop="submit"
      sortable
      label="提交">
    </el-table-column>
  </el-table>
    </div>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
  </el-card>
</template>

<script>
  export default {
    name: "Problems",
    filter: {
      dataslice(array) {
        const offset = (page - 1) * limit;
        const newdata = (offset + limit >= array.length) ? array.slice(offset, array.length) : array.slice(offset, offset + limit);
        return newdata
      }
    },
    mounted() {
      this.$http({
        url: '/api/getproblemlist/',
        methods: 'get',
        params: {
          'token': this.$cookies.get('token')
        }
      }).then( res => {

        this.tableData = []
        for(let i in res.data.data){
          // console.log(res.data.data[i])
          let item = res.data.data[i]
          this.Data.push({
              problem_id: item.problem_id,
              tittle: item.title,
              degree: item.difficulty,
              tag: item.type,
              solved: item.accepted,
              submit: item.submit
            })
        }
        this.total = this.Data.length;
        this.tableData = [];
        for(let i = (this.current_page-1) * this.page_sizes; i < Math.min(this.current_page * this.page_sizes, this.total); i++ ){
          this.tableData.push(this.Data[i]);
        }
      })
    },
    methods: {
      tableRowClassName({row, rowIndex}) {
        if (row.problem_id % 5 === 1) {
          return 'success-row';
        } else if (row.problem_id % 9 === 2) {
          return 'warning-row';
        } else {
          return '';
        }
      },
      handleSizeChange(val) {
        this.page_sizes=val;
        this.handleCurrentChange(this.current_page);
      },
      handleCurrentChange(val) {
        this.tableData = [];
        for(let i = (val-1) * this.page_sizes; i < Math.min(val * this.page_sizes, this.total); i++ ){
          this.tableData.push(this.Data[i]);
        }
      },
      // filterChange(filters) {
      //   console(value);
      // }
    },
    data() {
      return {
        current_page: 1,
        page_sizes: 50,
        Data: [],
        tableData: [],
        total: 0,
        listQuery: {
          page: 1,
          limit: 10,
        },
      }
    },
  }
</script>

<style>
.el-table .warning-row {
  background: rgba(245, 127, 127, 0.5);
}

.el-table .success-row {
  background: rgb(40, 211, 154, 0.5);
}

</style>
