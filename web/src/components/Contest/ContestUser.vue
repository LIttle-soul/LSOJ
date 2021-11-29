<template>
  <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
    <el-table-column prop="user_id" label="用户账号"></el-table-column>
    <el-table-column prop="user_name" label="真实姓名"></el-table-column>
    <el-table-column prop="user_school" label="用户学校"></el-table-column>
    <el-table-column prop="student_id" label="用户学号"></el-table-column>
    <el-table-column prop="apply_time" label="申请时间"></el-table-column>
    <el-table-column
      prop="apply_status"
      fixed="right"
      width="50px"
      label="审核状态"
      v-if="admin"
    >
      <template #default="scope">
        <el-switch
          v-model="scope.row.apply_status"
          active-color="#13ce66"
          inactive-color="#aaaaaa"
          :disabled="true"
        ></el-switch>
      </template>
    </el-table-column>
    <el-table-column fixed="right" width="90px" label="操作" v-if="admin">
      <template #default="scope">
        <div class="button-box">
          <el-button
            size="mini"
            type="success"
            circle
            @click="handleCheckClick(scope.row)"
            ><el-icon :size="16"><i class="bi bi-check-lg"></i></el-icon
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            @click="handleDeleteClick(scope.row)"
            ><el-icon :size="16"><i class="bi bi-trash"></i></el-icon
          ></el-button>
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
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { agreeContestUser, deleteContestUser } from "@/api/contest";

let props = defineProps({
  admin: {
    type: Boolean,
    default: true,
  },
  Data: {
    type: undefined,
    default: [],
  },
  contest_id: {
    type: Number,
    default: null,
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

let emits = defineEmits(["success", "handleSizeChange", "handlePageChange"]);

let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};
let handleCurrentChange = (val: number) => {
  emits("handlePageChange", val);
};
let handleCheckClick = async (row: any) => {
  let back_data = await agreeContestUser({
    contest_id: props.contest_id,
    user_id: row.user_id,
  });
  if (back_data.status) {
    emits("success");
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
  let back_data = await deleteContestUser({
    contest_id: props.contest_id,
    user_id: row.user_id,
  });
  if (back_data.status) {
    emits("success");
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

<style scoped lang="scss">
.button-box {
  display: flex;
  justify-content: space-around;
}
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
