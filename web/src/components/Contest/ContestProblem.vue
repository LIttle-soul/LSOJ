<template>
  <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
    <el-table-column prop="problem_num" label="编号" />
    <el-table-column prop="problem_id" label="问题编号" />
    <el-table-column prop="problem_title" label="问题标题" />
    <el-table-column fixed="right" width="130px" label="操作" v-if="admin">
      <template #default="scope">
        <div class="button-box">
          <el-button
            size="mini"
            type="primary"
            circle
            @click="handleContestProblemUpClick(scope.$index)"
            ><el-icon :size="16"><i class="bi bi-chevron-up"></i></el-icon
          ></el-button>
          <el-button
            size="mini"
            type="primary"
            circle
            @click="handleContestProblemDownClick(scope.$index)"
            ><el-icon :size="16"><i class="bi bi-chevron-down"></i></el-icon
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            @click="handleContestProblemDeleteClick(scope.row)"
            ><el-icon :size="16"><i class="bi bi-trash"></i></el-icon
          ></el-button>
        </div>
      </template>
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
</template>

<script lang="ts" setup>
import { ref } from "vue";

let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
  admin: {
    type: Boolean,
    default: true,
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

let emits = defineEmits([
  "handleContestProblemUpClick",
  "handleContestProblemDownClick",
  "handleContestProblemDeleteClick",
  "handleSizeChange",
  "handlePageChange",
]);
let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emits("handlePageChange", val);
};
let handleContestProblemUpClick = (index: any) => {
  emits("handleContestProblemUpClick", { index });
};
let handleContestProblemDownClick = (index: any) => {
  emits("handleContestProblemDownClick", { index });
};
let handleContestProblemDeleteClick = (row: any) => {
  emits("handleContestProblemDeleteClick", row);
};
</script>

<style scoped lang="scss">
.button-box {
  display: flex;
  justify-content: space-around;
}
.pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .pagination-2 {
    display: block;
  }
  .pagination-1 {
    display: none;
  }
}
</style>
