<template>
  <div class="contest-list-child">
    <el-table
      :data="Data"
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%"
      @cell-click="show_contest"
      @filter-change="filterDataByType"
      :default-sort="{ prop: 'contest_id', order: 'descending' }"
    >
      <el-table-column prop="contest_id" label="竞赛编号"> </el-table-column>
      <el-table-column prop="contest_title" label="竞赛标题"> </el-table-column>
      <el-table-column prop="contest_time" label="竞赛时间"> </el-table-column>
      <el-table-column
        prop="contest_type"
        :filters="filter_status_data"
        :column-key="'contest_type'"
        :filter-multiple="false"
        label="状态"
      >
        <template #default="scope">
          <el-tag>{{ filter_status_data[scope.row.contest_type].text }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="contest_creator" label="创建者"> </el-table-column>
      <el-table-column
        prop="contest_status"
        fixed="right"
        width="50px"
        label="状态"
        v-if="admin"
      >
        <template #default="scope">
          <el-switch
            v-model="scope.row.contest_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="130px" label="操作" v-if="admin">
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
              type="success"
              circle
              @click="handleCheckClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-check-lg"></i></el-icon>
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
import { changeContestData, deleteContestData } from "@/api/contest";
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

let router = useRouter();
let store = useStore();

let prop = defineProps({
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

let emit = defineEmits([
  "filterContestByType",
  "handleSizeChange",
  "handleCurrentChange",
  "reloadData",
]);

let filter_status_data = [
  { text: "公开", value: 0 },
  { text: "私有", value: 1 },
  { text: "作业", value: 2 },
  { text: "竞赛", value: 3 },
];

let handleSizeChange = (val: number) => {
  emit("handleSizeChange", val);
};
let handleCurrentChange = (val: number) => {
  emit("handleCurrentChange", val);
};
let filterDataByType = (row: any) => {
  emit("filterContestByType", row.contest_type);
};
let handleEditClick = (row: any) => {
  router.push("/admin/addcontest/" + row.contest_id);
};
let handleCheckClick = async (row: any) => {
  let back_data = await changeContestData({
    contest_id: row.contest_id,
    contest_status: row.contest_status,
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
let handleDeleteClick = async (row: any) => {
  let back_data = await deleteContestData({ contest_id: row.contest_id });
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
let show_contest = (row: any) => {
  if (!prop.admin) {
    router.push({
      path: "/contestshow",
      query: { contest_id: row.contest_id },
    });
  }
};
</script>

<style scoped lang="scss">
.button-box {
  display: flex;
  justify-content: space-around;
}
.contest-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .contest-list-child .pagination-2 {
    display: block;
  }
  .contest-list-child .pagination-1 {
    display: none;
  }
}
</style>
