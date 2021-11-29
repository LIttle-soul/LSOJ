<template>
  <div class="contest-rank-child">
    <el-table
      :data="Data"
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%"
      :default-sort="{ prop: 'rank_id', order: 'scending' }"
    >
      <el-table-column prop="rank_id" label="排名"> </el-table-column>
      <el-table-column prop="user_id" label="用户"> </el-table-column>
      <el-table-column prop="name_id" label="昵称"> </el-table-column>
      <el-table-column prop="solve_number" label="解题数"> </el-table-column>
      <el-table-column prop="solution_time" label="时间"> </el-table-column>
      <el-table-column
        v-for="(item, index) in props.problem"
        :key="index"
        :prop="item.problem_num"
        :label="item.problem_num"
        :formatter="formatProblemTime"
      >
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page.page_size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page.page_size"
      layout="prev, pager, next"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";

let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
  problem: {
    type: undefined,
    default: <any>[],
  },
  page: {
    type: undefined,
    default: {
      page: 1,
      page_size: 50,
      total: 0,
    },
  },
});

let emits = defineEmits(["onLoading", "handleSizeChange", "handleCurrentChange"]);
onMounted(() => {
  emits("onLoading");
});
let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emits("handleCurrentChange", val);
};

let formatProblemTime = (row: any, column: any, cellValue: any) => {
  // console.log(row, column, cellValue);
  if (cellValue) return `${cellValue.time} (${cellValue.num})`;
  else return "00:00:00 (0)";
};
</script>

<style scoped lang="scss">
.contest-rank-child .table-header .el-select .el-input {
  width: 70px;
}
.contest-rank-child .table-header .el-input__suffix {
  /* background: black; */
  transform: translateY(-2px);
}
.contest-rank-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.contest-rank-child .input-with-select {
  width: 280px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.contest-rank-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .contest-rank-child .input-with-select {
    display: none;
  }
  .contest-rank-child .pagination-2 {
    display: block;
  }
  .contest-rank-child .pagination-1 {
    display: none;
  }
}
</style>
