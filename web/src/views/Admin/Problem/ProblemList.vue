<template>
  <div class="problem-list">
    <div class="echart">
      <!-- 此处用于添加图表信息 -->
    </div>
    <div class="list">
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
                  @click="search_all_data(search_data)"
                ></el-button>
              </template>
            </el-input>
          </div>
        </template>
        <div>
          <ProblemList
            :admin="true"
            :Data="Data"
            @filterProblemByDegree="filterProblemWithDegree"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import ProblemList from "@/components/Problem/ProblemList.vue";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    ProblemList: ProblemList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("problem", {
      temp_data: (state) => state.problem_list,
    }),
    ...mapGetters("problem", {
      filterProblemList: "filterProblemList",
      filterProblemByDegree: "filterProblemByDegree",
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data();
    },
    temp_data() {
      this.Data = this.formatData(this.temp_data);
    },
  },
  created() {
    this.Data = this.formatData(this.temp_data);
  },
  data() {
    return {
      search_data: "",
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
    };
  },
  methods: {
    search_all_data(val) {
      this.Data = this.formatData(this.filterProblemList(this.temp_data, val));
    },
    filterProblemWithDegree(val) {
      if (val.length === 0) {
        this.Data = this.formatData(this.temp_data);
      } else {
        this.Data = this.formatData(
          this.filterProblemByDegree(this.temp_data, val)
        );
      }
    },
    formatData(val) {
      return val.map((item) => ({
        problem_id: item.problem_id,
        problem_title: item.problem_title,
        problem_degree: item.problem_difficult,
        problem_tag: item.problem_tag,
        problem_solved: item.problem_accepted,
        problem_submit: item.problem_submit,
        problem_status: item.problem_status,
        problem_source: item.problem_course,
        creation_time: this.$dayJS(item.creation_time).format(
          "YYYY-MM-DD HH:mm:ss"
        ),
        submit_status: item.pass_status,
        centerDialogVisible: false,
      }));
    },
  },
};
</script>

<style lang="css">
.problem-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.problem-list .input-with-select {
  width: 230px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 600px) {
  .problem-list-child .input-with-select {
    display: none;
  }
}
</style>

<style scoped>
.problem-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .problem-list {
    width: 100%;
  }
}
</style>
