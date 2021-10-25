<template>
  <div class="solution-list">
    <el-card shadow="always">
      <template #header>
        <div class="table-header">
          <i class="el-icon-wind-power"></i>
          提交列表
          <span
            ><el-switch v-model="reload_status" active-text="实时更新">
            </el-switch
          ></span>
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
              <el-button
                icon="el-icon-search"
                @click="search_all_data(search_select, search_data)"
              ></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <div>
        <RankList :Data="Data" @filterSolutionList="filterSolutionList" />
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineAsyncComponent, onUnmounted } from "@vue/runtime-core";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    RankList: defineAsyncComponent(() =>
      import("@/components/Solution/SolutionList.vue")
    ),
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("solution", {
      temp_data: (state) => state.solution_list,
    }),
    ...mapGetters("solution", {
      filterListByKey: "filterListByKey",
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data();
    },
    temp_data() {
      if (this.reload_status) this.Data = this.formatData(this.temp_data);
    },
  },
  created() {
    // console.log(this.$route.params);
    if (this.$route.params) {
      this.filterSolutionByUserAndProblem(
        this.$route.params.problem_id,
        this.$route.params.user_id
      );
    } else {
      this.Data = this.formatData(this.temp_data);
    }
    let inter = setInterval(() => {
      this.$store.dispatch("solution/getSolutionDataList");
    }, 10000);
    onUnmounted(() => {
      clearInterval(inter);
    });
  },
  data() {
    return {
      search_data: "",
      search_select: "problem",
      reload_status: false,
      Data: [
        {
          solution_id: 1,
          user_id: "user_1",
          problem_id: 1002,
          solution_result: 0,
          solution_memory: 0,
          solution_consuming: 0,
          solution_language: 0,
          solution_length: "125B",
          solution_time: "2021-07-03 00:26:18",
        },
      ],
    };
  },
  methods: {
    search_all_data(label, value) {
      this.Data = this.formatData(
        this.filterListByKey(this.temp_data, label, value)
      );
    },
    filterSolutionByUserAndProblem(problem_id, user_id) {
      this.Data = this.formatData(
        this.filterListByKey(
          this.filterListByKey(this.temp_data, "user", user_id || ""),
          "problem",
          problem_id || ""
        )
      );
    },
    filterSolutionList(value) {
      if (value.result != undefined && value.result.length != 0) {
        this.Data = this.Data.filter((val) => {
          return val.solution_result == value.result;
        });
      } else if (value.language != undefined && value.language.length != 0) {
        this.Data = this.Data.filter((val) => {
          return val.solution_language == value.language;
        });
      } else {
        this.Data = this.formatData(this.temp_data);
      }
    },
    formatData(val) {
      // console.log(val);
      return val
        .map((item) => ({
          solution_id: item.solution_id,
          user_id: item.user_id,
          problem_id: item.problem_id,
          solution_result: item.run_result,
          solution_memory: item.run_memory,
          solution_consuming: item.run_time,
          solution_language: item.solution_language,
          solution_length: item.code_length,
          solution_time: this.$dayJS(item.solution_time).format(
            "YYYY-MM-DD HH:mm:ss"
          ),
        }))
        .reverse();
    },
  },
};
</script>

<style lang="css">
.solution-list .table-header .el-select .el-input {
  width: 80px;
}
.solution-list .table-header .el-input__suffix {
  /* background: black; */
  transform: translateY(-2px);
}
</style>

<style scoped>
.solution-list {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
}
.solution-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.solution-list .input-with-select {
  width: 280px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 1000px) {
  .solution-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .solution-list .input-with-select {
    display: none;
  }
}
</style>
