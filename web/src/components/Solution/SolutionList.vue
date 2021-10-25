<template>
  <div class="solution-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      @filter-change="filterSolutionList"
      style="width: 100%;"
    >
      <el-table-column prop="solution_id" label="提交编号"> </el-table-column>
      <el-table-column prop="user_id" label="用户"> </el-table-column>
      <el-table-column v-if="contest" prop="problem_num" label="问题">
      </el-table-column>
      <el-table-column v-else prop="problem_id" label="问题"> </el-table-column>
      <el-table-column
        prop="solution_result"
        :filters="filter_result_data"
        :column-key="'result'"
        :filter-multiple="false"
        label="结果"
      >
        <template #default="scope">
          <el-tag type="success">{{
            filter_result_data[scope.row.solution_result].text
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="solution_memory" label="内存"> </el-table-column>
      <el-table-column prop="solution_consuming" label="耗时">
      </el-table-column>
      <el-table-column
        prop="solution_language"
        :filters="filter_language_data"
        :column-key="'language'"
        :filter-multiple="false"
        label="语言"
      >
        <template #default="scope">
          {{ filter_language_data[scope.row.solution_language].text }}
        </template>
      </el-table-column>
      <el-table-column prop="solution_length" label="代码长度">
      </el-table-column>
      <el-table-column prop="solution_time" label="提交时间"> </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="total, sizes, prev, pager, next, jumper"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="prev, pager, next"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "UserRankList",
  computed: {
    ...mapState("code", {
      filter_result_data: (state) => state.filter_result_data,
      filter_language_data: (state) => state.filter_language_data,
    }),
  },
  props: {
    Data: {
      type: undefined,
      default: [],
    },
    contest: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["onLoading"],
  mounted() {
    this.$emit("onLoading");
  },
  data() {
    return {
      current_page: 1,
      page_sizes: 50,
    };
  },
  methods: {
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
    filterSolutionList(value) {
      this.$emit("filterSolutionList", value);
    },
  },
};
</script>

<style>
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
