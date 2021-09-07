<template>
  <div class="solution-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-wind-power"></i>
          提交列表
          <el-input
            placeholder="请输入内容"
            size="mini"
            v-model="search_data"
            class="input-with-select"
          >
          <template #prepend>
                    <el-select v-model="search_select" placeholder="请选择">
                        <el-option label="提交" value="solution"></el-option>
                        <el-option label="用户" value="user"></el-option>
                        <el-option label="题目" value="problem"></el-option>
                    </el-select>
                </template>
            <template #append>
              <el-button icon="el-icon-search" @click="search_all_data"></el-button>
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
          :stripe="true"
          :fit="true"
          style="width: 100%;"
          :default-sort="{ prop: 'solution_id', order: 'descending' }"
        >
          <el-table-column prop="solution_id" label="提交编号">
          </el-table-column>
          <el-table-column prop="user_id" label="用户">
          </el-table-column>
          <el-table-column prop="problem_id" label="问题">
          </el-table-column>
          <el-table-column 
          prop="solution_result" 
          :filters="filter_result_data"
          label="结果">
          <template #default="scope">
              <el-tag
              type="success"
              >{{ result_data[scope.row.solution_result] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="solution_memory" label="内存">
          </el-table-column>
          <el-table-column prop="solution_consuming" label="耗时">
          </el-table-column>
          <el-table-column 
            :filters="filter_language_data"
          prop="solution_language" 
          label="语言">
          <template #default="scope">
            {{language_data[scope.row.solution_language]}}
          </template>
          </el-table-column>
          <el-table-column prop="solution_length" label="代码长度">
          </el-table-column>
          <el-table-column prop="solution_time" label="提交时间">
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
export default {
  name: "UserRankList",
  mounted() {this.Data = this.listenDataMsg},
  computed: {
    listenSoreMsg() {
      return this.$store.state.search_data;
    },
    listenDataMsg() {
      // console.log(this.$store.state.solution_data);
      return this.$store.state.solution_data.map(item => ({
        solution_id: item.solution_id,
          user_id: item.user_id,
          problem_id: item.problem_id,
          solution_result: item.run_result,
          solution_memory: item.run_memory,
          solution_consuming: 0,
          solution_language: item.solution_language,
          solution_length: item.code_length + 'B',
          solution_time: this.$dayJS(item.solution_time).format('YYYY-MM-DD HH:mm:ss')
      }));
    }
  },
  watch: {
    listenSoreMsg() {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
    listenDataMsg() {
      // console.log(this.listenDataMsg);
      this.Data = this.listenDataMsg;
    }
  },
  data() {
    return {
      search_data: "",
      search_select: "problem",
      current_page: 1,
      page_sizes: 50,
      filter_result_data: [
          {text: '正确', value: 4}, 
          {text: '错误', value: 5}
      ],
      filter_language_data: [
          {text: '正确', value: 4}, 
          {text: '错误', value: 5}
      ],
      result_data: [
        '等待中..',
        '等待重判',
        '编译中',
        '运行并评判',
        '答案正确',
        '格式错误',
        '答案错误',
        '时间超限',
        '内存超限',
        '输出超限',
        '运行错误',
        '编译错误',
        '编译器错误',
      ],
      language_data: [
        'C',
        'C++',
        'Java',
        'Python2',
        'Python3',
        'Switch',
        'C#',
        'Go',
        'Ruby',
        'Bash',
      ],
      Data: [
        {
          solution_id: 1,
          user_id: "user_1",
          problem_id: 1002,
          solution_result: 0,
          solution_memory: 0,
          solution_consuming: 0,
          solution_language: 0,
          solution_length: '125B',
          solution_time: '2021-07-03 00:26:18'
        },
        {
          solution_id: 2,
          user_id: "user_1",
          problem_id: 1001,
          solution_result: 0,
          solution_memory: 0,
          solution_consuming: 0,
          solution_language: 0,
          solution_length: '125B',
          solution_time: '2021-07-03 00:26:18'
        },
        {
          solution_id: 3,
          user_id: "user_2",
          problem_id: 1002,
          solution_result: 0,
          solution_memory: 0,
          solution_consuming: 0,
          solution_language: 0,
          solution_length: '125B',
          solution_time: '2021-07-03 00:26:18'
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
    }
  },
};
</script>

<style>
.solution-list-child .table-header .el-select .el-input {
    width: 70px;
}
.solution-list-child .table-header .el-input__suffix {
    /* background: black; */
    transform: translateY(-2px);
}
.solution-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.solution-list-child .input-with-select {
  width: 280px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.solution-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .solution-list-child .input-with-select {
    display: none;
  }
  .solution-list-child .pagination-2 {
    display: block;
  }
  .solution-list-child .pagination-1 {
    display: none;
  }
}
</style>
