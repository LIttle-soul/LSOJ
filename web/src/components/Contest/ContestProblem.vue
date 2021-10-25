<template>
  <el-table
    :data="
      Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
    "
    size="mini"
    :stripe="true"
    :fit="true"
    style="width: 100%;"
  >
    <el-table-column prop="problem_num" label="编号" />
    <el-table-column prop="problem_id" label="问题编号" />
    <el-table-column prop="problem_title" label="问题标题" />
    <el-table-column fixed="right" width="130px" label="操作" v-if="admin">
      <template #default="scope">
        <el-button
          size="mini"
          type="primary"
          circle
          icon="el-icon-arrow-up"
          @click="handleContestProblemUpClick(scope.$index)"
        ></el-button>
        <el-button
          size="mini"
          type="primary"
          circle
          icon="el-icon-arrow-down"
          @click="handleContestProblemDownClick(scope.$index)"
        ></el-button>
        <el-button
          size="mini"
          type="danger"
          circle
          icon="el-icon-delete"
          @click="handleContestProblemDeleteClick(scope.row)"
        ></el-button>
      </template>
    </el-table-column>
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
</template>

<script>
export default {
  props: {
    Data: {
      type: undefined,
      default: [],
    },
    admin: {
      type: Boolean,
      default: true,
    },
  },
  emits: [
    "handleContestProblemUpClick",
    "handleContestProblemDownClick",
    "handleContestProblemDeleteClick",
  ],
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
    handleContestProblemUpClick(index) {
      this.$emit("handleContestProblemUpClick", { index });
    },
    handleContestProblemDownClick(index) {
      this.$emit("handleContestProblemDownClick", { index });
    },
    handleContestProblemDeleteClick(row) {
      this.$emit("handleContestProblemDeleteClick", row);
    },
  },
};
</script>

<style scoped>
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
