
<template>
  <el-card style="margin-top: 60px;">
    <template #header>
      <div>
        <span>问题列表</span>
      </div>
    </template>
    <div>
    <el-table
    :data="tableData"
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
  </el-card>
</template>

<script>
  export default {
    name: "Problems",
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
          this.tableData.push({
              problem_id: item.problem_id,
              tittle: item.title,
              degree: item.difficulty,
              tag: item.type,
              solved: item.accepted,
              submit: item.submit
            })
        }
      })
    },
    methods: {
      tableRowClassName({row, rowIndex}) {
        if (rowIndex === 1) {
          return 'success-row';
        } else if (rowIndex === 2) {
          return 'warning-row';
        } else {
          return '';
        }
      }
    },
    data() {
      return {
        tableData: [{
          problem_id: 1000,
          tittle: 'A+B',
          degree: 1,
          tag: '基础题',
          solved: 10,
          submit: 100
        },
        {
          problem_id: 1001,
          tittle: 'Hello,World',
          degree: 1,
          tag: '基础题',
          solved: 8,
          submit: 50
        }]
      }
    },
  }
</script>

<style>
.el-table .warning-row {
  background: rgba(245, 127, 127, 0.8);
}

.el-table .success-row {
  background: rgb(40, 211, 154);
}

</style>
