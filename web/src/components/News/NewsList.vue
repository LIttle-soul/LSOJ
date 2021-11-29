<template>
  <div class="news-list-child">
    <el-table
      :data="Data"
      size="mini"
      @cell-click="showNews"
      :stripe="true"
      :fit="true"
      style="width: 100%"
    >
      <el-table-column prop="news_id" label="新闻编号"> </el-table-column>
      <el-table-column prop="news_title" label="新闻标题"> </el-table-column>
      <el-table-column prop="news_time" label="创建时间"> </el-table-column>
      <el-table-column prop="news_creator" label="创建者"> </el-table-column>
      <el-table-column prop="news_importance" label="优先级"> </el-table-column>
      <el-table-column fixed="right" width="80px" label="操作" v-if="admin">
        <template #default="scope">
          <div class="button-box">
            <el-button
              size="mini"
              type="primary"
              circle
              @click="handleEditClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
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
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { deleteNewsData } from "@/api/news";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

let store = useStore();
let router = useRouter();

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
    default: {
      page: 1,
      page_size: 50,
      total: 0,
    },
  },
});

let emit = defineEmits(["handleSizeChange", "handlePageChange", "reloadData"]);

let handleSizeChange = (val: number) => {
  emit("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emit("handlePageChange", val);
};

let showNews = (row: any) => {
  if (!props.admin) {
    router.push("/shownews/" + row.news_id);
  }
};
let handleEditClick = (row: any) => {
  router.push("/admin/addnews/" + row.news_id);
};
let handleDeleteClick = async (row: any) => {
  let back_data = await deleteNewsData({
    news_id: row.news_id,
  });
  if (back_data.status) {
    emit("reloadData");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
</script>

<style lang="scss" scoped>
.button-box {
  display: flex;
  justify-content: space-around;
}
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
