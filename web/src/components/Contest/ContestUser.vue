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
          icon="el-icon-close"
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
</template>

<script>
import { agreeContestUser, deleteContestUser } from "@/api/contest";
export default {
  props: {
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
  },
  emits: ["success"],
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
    async handleCheckClick(row) {
      let back_data = await agreeContestUser({
        contest_id: this.contest_id,
        user_id: row.user_id,
      });
      if (back_data.status) {
        this.$emit("success");
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
    },
    async handleDeleteClick(row) {
      let back_data = await deleteContestUser({
        contest_id: this.contest_id,
        user_id: row.user_id,
      });
      if (back_data.status) {
        this.$emit("success");
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
