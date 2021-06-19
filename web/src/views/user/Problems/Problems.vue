
<template>
  <el-card style="margin-top: 60px;">
    <template #header>
      <div>
        <span>问题列表</span>
        <el-button class="button" style="float: right; transform: translatey(-12px);">
          操作按钮
        </el-button>
      </div>
    </template>
    <div>
      <el-table
    :data="tableData"
    stripe="true"
    border
    height=80vh
    style="width: 100%">
    <el-table-column
      prop="problem_id"
      label="编号"
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
    </el-table-column>
    <el-table-column
      prop="degree"
      label="难度">
    </el-table-column>
    <el-table-column
      prop="solved"
      label="正确">
    </el-table-column>
    <el-table-column
      prop="submit"
      label="提交">
    </el-table-column>
  </el-table>
    </div>
  </el-card>
</template>

<script>
  export default {
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
    }
  }
</script>

<style>

</style>
