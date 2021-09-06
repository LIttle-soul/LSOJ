<template>
  <div class="problem-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-collection"></i>
          问题列表
          <el-input
            placeholder="请输入内容"
            size="mini"
            v-model="search_data"
            class="input-with-select"
          >
            <template #append>
              <el-button
                icon="el-icon-search"
                @click="search_all_data"
              ></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <div>
        <el-table
          :data="
            Data.slice(
              (current_page - 1) * page_sizes,
              current_page * page_sizes
            )
          "
          size="mini"
          @cell-click="show_problem"
          :row-class-name="tableRowClassName"
          :default-sort="{ prop: 'problem_id', order: 'aescending' }"
        >
          <el-table-column prop="problem_id" label="编号"> </el-table-column>
          <el-table-column prop="problem_title" label="题目"> </el-table-column>
          <el-table-column prop="problem_tag" label="类型" v-if="!admin">
            <template #default="scope">
              <el-tag
                :type="
                  scope.row.problem_tag === '基础题' ? 'primary' : 'success'
                "
                disable-transitions
                >{{ scope.row.problem_tag }}</el-tag
              >
            </template>
          </el-table-column>
          <el-table-column
            prop="problem_degree"
            width="150"
            label="难度"
            :filters="filter_degree_data"
          >
            <template #default="scope">
              <el-rate
                v-model="scope.row.problem_degree"
                :disabled="!admin"
              ></el-rate>
            </template>
          </el-table-column>
          <el-table-column
            prop="problem_solved"
            sortable
            width="70"
            label="正确"
          >
          </el-table-column>
          <el-table-column
            prop="problem_submit"
            sortable
            width="70"
            label="提交"
          >
          </el-table-column>
          <el-table-column prop="problem_source" label="题目来源">
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
          <el-table-column
            fixed="right"
            width="165px"
            label="操作"
            v-if="admin"
          >
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
              >
                <ProblemDataList />
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="upload_data">上传文件</el-button>
                    <el-button
                      type="primary"
                      @click="scope.row.centerDialogVisible = false"
                      >确 定</el-button
                    >
                  </span>
                </template>
              </el-dialog>
            </template>
          </el-table-column>
        </el-table>
      </div>
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
    </el-card>
  </div>
</template>

<script>
import ProblemDataList from "@/components/Problem/ProblemDataList.vue";

export default {
  name: "ProblemList",
  components: {
    ProblemDataList: ProblemDataList,
  },
  mounted() {
    this.Data = this.listenDataMsg;
    this.total = this.listenDataMsg.lenth;
  },
  computed: {
    listenSoreMsg() {
      return this.$store.state.search_data;
    },
    listenDataMsg() {
      return this.$store.state.problem_data.map((item) => ({
        problem_id: item.problem_id,
        problem_title: item.problem_title,
        problem_degree: item.problem_difficult,
        problem_tag: item.problem_tag,
        problem_solved: item.problem_accepted,
        problem_submit: item.problem_submit,
        problem_status: item.problem_status,
        problem_source: item.problem_course,
        creation_time: this.$dayJS(item.creation_time).format('YYYY-MM-DD HH:mm:ss'),
        submit_status: 0,
        centerDialogVisible: false,
      }));
    },
  },
  watch: {
    listenSoreMsg() {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
    listenDataMsg() {
      // console.log(this.listenDataMsg);
      this.Data = this.listenDataMsg;
    },
  },
  props: {
    admin: {
      type: Boolean,
      define: false,
    },
  },
  data() {
    return {
      // centerDialogVisible: false,
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      filter_degree_data: [
        { text: "一星", value: 1 },
        { text: "二星", value: 2 },
        { text: "三星", value: 3 },
        { text: "四星", value: 4 },
        { text: "五星", value: 5 },
      ],
      Data: [
        {
          problem_id: 1001,
          problem_title: "Hello, World",
          problem_degree: 4,
          problem_tag: "基础题",
          problem_solved: 0,
          problem_submit: 0,
          problem_status: true,
          problem_source: "汉语言文学",
          creation_time: "2020-01-01 08:00:00",
          submit_status: -1,
          centerDialogVisible: false,
        },
      ],
      total: 0,
      listQuery: {
        page: 1,
        limit: 10,
      },
    };
  },
  methods: {
    tableRowClassName({ row }) {
      if (this.admin) {
        return "";
      }
      if (row.submit_status === 1) {
        return "success-row";
      } else if (row.submit_status === -1) {
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
    filterDegree(value, row) {
      return row.degree === value;
    },
    search_all_data() {
      console.log(this.search_data);
    },
    show_problem(row) {
      // console.log(row);
      if (!this.admin) {
        this.$router.push("/showproblem/"+row.problem_id);
      }
    },
    handleEditClick(val) {
      console.log(val);
    },
    handleCheckClick(val) {
      console.log(val);
    },
    handleDeleteClick(val) {
      console.log(val);
    },
    handleDataClick(val) {
      console.log(val);
      val.centerDialogVisible = true;
    },
    upload_data() {
      console.log("文件上传");
    },
  },
};
</script>

<style>
.problem-list-child .el-table .warning-row {
  background: rgba(245, 127, 127, 0.5);
}

.problem-list-child .el-table .success-row {
  background: rgb(40, 211, 154, 0.5);
}
.problem-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.problem-list-child .input-with-select {
  width: 230px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.problem-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .problem-list-child .input-with-select {
    display: none;
  }
  .problem-list-child .pagination-2 {
    display: block;
  }
  .problem-list-child .pagination-1 {
    display: none;
  }
}
</style>
