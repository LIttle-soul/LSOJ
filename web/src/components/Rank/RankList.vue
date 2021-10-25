<template>
  <div class="rank-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column prop="user_rank" sortable label="名次">
      </el-table-column>
      <el-table-column prop="user_id" label="用户"> </el-table-column>
      <el-table-column prop="user_nick" label="昵称"> </el-table-column>
      <el-table-column prop="true_submit" sortable label="正确">
      </el-table-column>
      <el-table-column prop="all_submit" sortable label="提交">
      </el-table-column>
      <el-table-column prop="percentage" sortable label="比率">
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
  </div>
</template>

<script>
export default {
  name: "UserRankList",
  props: {
    Data: {
      type: undefined,
      default: [],
    },
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
