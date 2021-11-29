<template>
  <div class="rank-list-child">
    <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
      <el-table-column prop="user_rank" sortable label="名次"> </el-table-column>
      <el-table-column prop="user_id" label="用户"> </el-table-column>
      <el-table-column prop="user_nick" label="昵称"> </el-table-column>
      <el-table-column prop="true_submit" sortable label="正确"> </el-table-column>
      <el-table-column prop="all_submit" sortable label="提交"> </el-table-column>
      <el-table-column prop="percentage" sortable label="比率"> </el-table-column>
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
import { ref } from "vue";

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  Data: {
    type: undefined,
    default: [],
  },
  page: {
    type: undefined,
    default: { page: 1, page_size: 50, total: 0 },
  },
});
let emits = defineEmits(["handleSizeChange", "handleCurrentChange"]);
let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emits("handleCurrentChange", val);
};
</script>

<style scoped lang="scss">
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
