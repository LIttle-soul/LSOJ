<template>
  <div class="contest-count-child">
    <el-table
      :data="Data"
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%"
      :default-sort="{ prop: 'problem_id', order: 'scending' }"
    >
      <el-table-column prop="problem_id" label="问题"> </el-table-column>
      <el-table-column prop="result_type1" label="AC"> </el-table-column>
      <el-table-column prop="result_type2" label="PE"> </el-table-column>
      <el-table-column prop="result_type3" label="WA"> </el-table-column>
      <el-table-column prop="result_type4" label="TLE"> </el-table-column>
      <el-table-column prop="result_type5" label="MLE"> </el-table-column>
      <el-table-column prop="result_type6" label="OLE"> </el-table-column>
      <el-table-column prop="result_type7" label="RE"> </el-table-column>
      <el-table-column prop="result_type8" label="CE"> </el-table-column>
      <el-table-column prop="result_type9" label="TR"> </el-table-column>
      <el-table-column prop="submit_total" label="Total"> </el-table-column>
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
let prop = defineProps({
  Data: {
    type: undefined,
    default: [],
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
</script>

<style scoped lang="scss">
.contest-count-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .contest-count-child .pagination-2 {
    display: block;
  }
  .contest-count-child .pagination-1 {
    display: none;
  }
}
</style>
