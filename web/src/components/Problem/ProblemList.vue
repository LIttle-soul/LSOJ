<template>
  <div class="problem-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      @cell-click="show_problem"
      @filter-change="filterProblemBYDegree"
      :row-class-name="tableRowClassName"
      :default-sort="{ prop: 'problem_id', order: 'aescending' }"
    >
      <el-table-column v-if="contest" prop="problem_num" label="编号">
      </el-table-column>
      <el-table-column v-else prop="problem_id" label="编号"> </el-table-column>
      <el-table-column prop="problem_title" label="题目"> </el-table-column>
      <el-table-column
        prop="problem_tag"
        label="类型"
        v-if="!admin && !contest"
      >
        <template #default="scope">
          <el-tag
            v-for="item in scope.row.problem_tag"
            :key="item"
            size="mini"
            :color="color16()"
            >{{ item }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column
        prop="problem_degree"
        width="150"
        label="难度"
        filter-placement="bottom-end"
        :filters="filter_degree_data"
        :column-key="'sStatus'"
        v-if="!contest"
      >
        <template #default="scope">
          <el-rate
            v-model="scope.row.problem_degree"
            :disabled="!admin"
          ></el-rate>
        </template>
      </el-table-column>
      <el-table-column prop="problem_solved" sortable width="70" label="正确">
      </el-table-column>
      <el-table-column prop="problem_submit" sortable width="70" label="提交">
      </el-table-column>
      <el-table-column prop="problem_source" label="题目来源" v-if="!contest">
      </el-table-column>
      <el-table-column prop="creation_time" label="创建时间" v-if="admin">
      </el-table-column>
      <el-table-column
        prop="problem_status"
        fixed="right"
        width="50px"
        label="状态"
        v-if="admin"
      >
        <template #default="scope">
          <el-switch
            v-model="scope.row.problem_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="165px" label="操作" v-if="admin">
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
          <el-button
            size="mini"
            type="warning"
            circle
            icon="el-icon-box"
            @click="handleDataClick(scope.row)"
          ></el-button>
          <el-dialog
            title="测试数据"
            v-model="scope.row.centerDialogVisible"
            width="90%"
            :destroy-on-close="true"
          >
            <ProblemDataList :problem_id="scope.row.problem_id" />
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
import ProblemDataList from "@/components/Problem/ProblemDataList.vue";
import { changeProblemData, deleteProblemData } from "@/api/problem";

export default {
  name: "ProblemList",
  components: {
    ProblemDataList: ProblemDataList,
  },
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
    contest: {
      type: Boolean,
      default: false,
    },
    contest_id: {
      type: Number,
      default: -1,
    },
    Data: {
      type: undefined,
      default: [],
    },
  },
  emits: ["onLoading"],
  mounted() {
    this.$emit("onLoading");
  },
  data() {
    return {
      current_page: 1,
      page_sizes: 50,
      filter_degree_data: [
        { text: "一星", value: 1 },
        { text: "二星", value: 2 },
        { text: "三星", value: 3 },
        { text: "四星", value: 4 },
        { text: "五星", value: 5 },
      ],
    };
  },
  methods: {
    tableRowClassName({ row }) {
      if (this.admin) {
        return "";
      }
      if (+row.submit_status === 1) {
        return "success-row";
      } else if (+row.submit_status === -1) {
        return "warning-row";
      } else {
        return "";
      }
    },
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
    filterProblemBYDegree(value) {
      // console.log(value.sStatus);
      this.$emit("filterProblemByDegree", value.sStatus);
    },
    show_problem(row) {
      // console.log(row, this.contest_id);
      if (!this.admin) {
        this.$router.push({
          path: "/showproblem",
          query: {
            problem_id: row.problem_id,
            contest_id: this.contest_id,
            problem_title: escape(row.problem_title),
            problem_description: escape(row.problem_description),
            time_limit: row.time_limit,
            memory_limit: row.memory_limit,
          },
        });
      }
    },
    handleEditClick(row) {
      this.$router.push("/admin/addproblem/" + row.problem_id);
    },
    async handleCheckClick(row) {
      // console.log(row);
      let data = {
        problem_id: row.problem_id,
        probelm_difficult: row.problem_degree,
        problem_status: row.problem_status,
      };
      let back_data = await changeProblemData(data);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("problem/getProblemDataList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async handleDeleteClick(row) {
      let back_data = await deleteProblemData(row.problem_id);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("problem/getProblemDataList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    handleDataClick(val) {
      // console.log(val);
      val.centerDialogVisible = true;
    },
    color16() {
      var r = Math.floor(Math.random() * 256);
      var g = Math.floor(Math.random() * 256);
      var b = Math.floor(Math.random() * 256);
      var a = Math.floor(Math.random() * 50);
      var color =
        "#" + r.toString(16) + g.toString(16) + b.toString(16) + a.toString(16);
      return color;
    },
  },
};
</script>

<style>
.problem-list-child .warning-row {
  background: rgba(245, 127, 127, 0.5);
}
.problem-list-child .success-row {
  background: rgb(40, 211, 154, 0.5);
}
</style>

<style scoped>
.problem-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .oblem-list-child .pagination-2 {
    display: block;
  }
  .problem-list-child .pagination-1 {
    display: none;
  }
}
</style>
