<template>
  <div class="solution-list-child">
    <el-table
      :data="Data"
      size="mini"
      :stripe="true"
      :fit="true"
      @filter-change="filterSolutionList"
      style="width: 100%"
    >
      <el-table-column prop="solution_id" label="提交编号"> </el-table-column>
      <el-table-column prop="user_id" label="用户"> </el-table-column>
      <el-table-column v-if="contest" prop="problem_num" label="问题"> </el-table-column>
      <el-table-column v-else prop="problem_id" label="问题"> </el-table-column>
      <el-table-column
        prop="solution_result"
        :filters="result_data"
        :column-key="'result'"
        :filter-multiple="false"
        label="结果"
      >
        <template #default="scope">
          <el-tag type="success">{{
            result_data[scope.row.solution_result].text
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="solution_memory" label="内存"> </el-table-column>
      <el-table-column prop="solution_consuming" label="耗时"> </el-table-column>
      <el-table-column
        prop="solution_language"
        :filters="language_data"
        :column-key="'language'"
        :filter-multiple="false"
        label="语言"
      >
        <template #default="scope">
          {{ language_data[scope.row.solution_language].text }}
        </template>
      </el-table-column>
      <el-table-column prop="solution_length" label="代码长度"> </el-table-column>
      <el-table-column prop="solution_time" label="提交时间"> </el-table-column>
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
import { useStore, mapState } from "vuex";
import { computed, onMounted, ref } from "vue";

let store = useStore();

let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
  contest: {
    type: Boolean,
    default: false,
  },
  page: {
    type: undefined,
    default: {
      page: 1,
      page_size: 50,
      total: 50,
    },
  },
});

let emits = defineEmits([
  "onLoading",
  "filterSolutionList",
  "handleSizeChange",
  "handleCurrentChange",
]);
onMounted(() => {
  emits("onLoading");
});

let result_data = computed(
  mapState("code", ["result_data"]).result_data.bind({
    $store: store,
  })
);

let language_data = computed(
  mapState("code", ["language_data"]).language_data.bind({
    $store: store,
  })
);
// console.log(language_data.value, result_data.value);
let filterSolutionList = (value: any) => {
  emits("filterSolutionList", value);
};

let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emits("handleCurrentChange", val);
};
</script>

<style lang="scss" scoped>
.solution-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .solution-list-child .input-with-select {
    display: none;
  }
  .solution-list-child .pagination-2 {
    display: block;
  }
  .solution-list-child .pagination-1 {
    display: none;
  }
}
</style>
