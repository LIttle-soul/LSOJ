<template>
  <div class="contest-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
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
        label="状态"
      >
        <template #default="scope">
          <el-tag>{{ status_data[scope.row.contest_type] }}</el-tag>
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
import { changeContestData, deleteContestData } from "@/api/contest";

export default {
  name: "UserContestList",
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
      filter_status_data: [
        { text: "公开", value: 0 },
        { text: "私有", value: 1 },
        { text: "作业", value: 2 },
        { text: "竞赛", value: 3 },
      ],
      status_data: ["公开", "私有", "作业", "竞赛"],
    };
  },
  methods: {
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
    filterDataByType(row) {
      this.$emit("filterContestByType", row.contest_type);
    },
    handleEditClick(row) {
      this.$router.push("/admin/addcontest/" + row.contest_id);
    },
    async handleCheckClick(row) {
      let val = {
        contest_id: row.contest_id,
        contest_status: row.contest_status,
      };
      let back_data = await changeContestData(val);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("contest/getContestList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async handleDeleteClick(row) {
      let back_data = await deleteContestData(row.contest_id);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("contest/getContestList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    show_contest(row) {
      if (!this.admin) {
        this.$router.push("/contestshow/" + row.contest_id);
      }
    },
  },
};
</script>

<style scoped>
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
