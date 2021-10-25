<template>
  <div class="user-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column prop="user_id" label="用户账号"> </el-table-column>
      <el-table-column prop="user_nick" label="用户昵称"> </el-table-column>
      <el-table-column prop="user_name" label="用户姓名"> </el-table-column>
      <el-table-column prop="user_school" label="用户学校"> </el-table-column>
      <el-table-column prop="registration_time" label="注册时间">
      </el-table-column>
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
      <el-table-column
        prop="user_status"
        fixed="right"
        width="50px"
        label="状态"
      >
        <template #default="scope">
          <el-switch
            v-model="scope.row.user_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="130px" label="操作">
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
            type="success"
            circle
            icon="el-icon-check"
            @click="handleCheckClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            icon="el-icon-delete"
            @click="handleDeleteClick(scope.row)"
          ></el-button>
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
import { changeUserInfo, deleteUserInfo } from "@/api/user";

export default {
  name: "UserListChild",
  computed: {},
  props: {
    Data: {
      type: undefined,
      default: [],
    },
  },
  data() {
    return {
      resetting_password: "",
      current_page: 1,
      page_sizes: 50,
      power_options: [
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
      ],
    };
  },
  methods: {
    handleEditClick(raw) {
      raw.centerDialogVisible = true;
    },
    async handleCheckClick(raw) {
      let data = {
        user_id: raw.user_id,
        user_power: raw.user_power,
        user_status: raw.user_status,
      };
      let back_data = await changeUserInfo(data);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getUserList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async handleDeleteClick(raw) {
      let back_data = await deleteUserInfo(raw.user_id);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getUserList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async changePassword(raw) {
      let data = {
        user_id: raw.user_id,
        user_password: this.resetting_password,
      };
      let back_data = await changeUserInfo(data);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
      raw.centerDialogVisible = false;
    },
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
  },
};
</script>

<style>
.user-list .el-card__header {
  height: 60px;
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
