<template>
  <div class="news-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      @cell-click="showNews"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column prop="news_id" label="新闻编号"> </el-table-column>
      <el-table-column prop="news_title" label="新闻标题"> </el-table-column>
      <el-table-column prop="news_time" label="创建时间"> </el-table-column>
      <el-table-column prop="news_creator" label="创建者"> </el-table-column>
      <el-table-column prop="news_importance" label="优先级"> </el-table-column>
      <el-table-column fixed="right" width="90px" label="操作" v-if="admin">
        <template #default="scope">
          <el-button
            size="mini"
            type="primary"
            circle
            icon="el-icon-edit"
            @click="handleEditClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            icon="el-icon-delete"
            @click="handleDeleteClick(scope.row)"
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
  </div>
</template>

<script>
import { deleteNewsData } from "@/api/news";
export default {
  name: "UserNewsList",
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
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
    showNews(row) {
      if (!this.admin) {
        this.$router.push("/shownews/" + row.news_id);
      }
    },
    handleEditClick(row) {
      this.$router.push("/admin/addnews/" + row.news_id);
    },
    async handleDeleteClick(row) {
      let back_data = await deleteNewsData(row.news_id);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("news/getNewsList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
  },
};
</script>

<style>
.news-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .news-list-child .pagination-2 {
    display: block;
  }
  .news-list-child .pagination-1 {
    display: none;
  }
}
</style>
