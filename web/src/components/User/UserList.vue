<template>
  <div class="user-list-child">
    <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
      <el-table-column prop="user_id" label="用户账号"> </el-table-column>
      <el-table-column prop="user_nick" label="用户昵称"> </el-table-column>
      <el-table-column prop="user_name" label="用户姓名"> </el-table-column>
      <el-table-column prop="user_school" label="用户学校"> </el-table-column>
      <el-table-column prop="registration_time" label="注册时间"> </el-table-column>
      <el-table-column prop="user_power" label="用户身份">
        <template #default="scope">
          <el-select v-model="scope.row.user_power" placeholder="请选择">
            <el-option
              v-for="item in power_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="user_status" fixed="right" width="60px" label="状态">
        <template #default="scope">
          <el-switch
            v-model="scope.row.user_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="120px" label="操作">
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
            <el-dialog
              title="重置密码"
              v-model="scope.row.centerDialogVisible"
              width="30%"
              center
            >
              <el-input
                v-model="resetting_password"
                placeholder="请在这里输入新密码"
              ></el-input>
              <template #footer>
                <span class="dialog-footer">
                  <el-button @click="scope.row.centerDialogVisible = false"
                    >取 消</el-button
                  >
                  <el-button type="primary" @click="changePassword(scope.row)"
                    >确 定</el-button
                  >
                </span>
              </template>
            </el-dialog>
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
import { ElMessage } from "element-plus";
import { changeUserInfo, deleteUserInfo } from "@/api/user";

// 父组件参数接受
let props = defineProps({
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

// 当前页面参数设置
let resetting_password = ref("");
let power_options = ref([
  {
    value: 0,
    label: "超级管理员",
  },
  {
    value: 1,
    label: "管理员",
  },
  {
    value: 2,
    label: "教师",
  },
  {
    value: 3,
    label: "志愿者",
  },
  {
    value: 4,
    label: "普通用户",
  },
]);

// 向父组件传送事件
let emit = defineEmits(["handleSizeChange", "handlePageChange", "reloadData"]);

// 当前页面事件处理
let handleEditClick = (raw: any) => {
  raw.centerDialogVisible = true;
};
let handleCheckClick = async (raw: any) => {
  let back_data = await changeUserInfo({
    user_id: raw.user_id,
    user_power: raw.user_power,
    user_status: raw.user_status,
    user_password: "",
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
let handleDeleteClick = async (raw: any) => {
  let back_data = await deleteUserInfo({ user_id: raw.user_id });
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
let changePassword = async (raw: any) => {
  let back_data = await changeUserInfo({
    user_id: raw.user_id,
    user_power: "",
    user_status: "",
    user_password: resetting_password.value,
  });
  if (back_data.status) {
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
  raw.centerDialogVisible = false;
};

// 页面跳转
let handleSizeChange = (val: number) => {
  emit("handleSizeChange", val);
};
let handleCurrentChange = (val: number) => {
  emit("handlePageChange", val);
};
</script>

<style lang="scss" scoped>
.button-box {
  display: flex;
  justify-content: space-around;
}
.user-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .user-list-child .pagination-2 {
    display: block;
  }
  .user-list-child .pagination-1 {
    display: none;
  }
}
</style>
