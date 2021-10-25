<template>
  <div class="contest-count-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100% ;"
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
export default {
  name: "ContestCount",
  props: {
    Data: {
      type: undefined,
      default: [],
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
  },
};
</script>

<style scoped>
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
