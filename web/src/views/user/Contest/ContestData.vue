<template>
  <div class="contest-data">
    <el-tabs type="border-card">
      <el-tab-pane label="竞赛问题"
        ><ContestProblem
          :Data="contest_problem"
          :contest="true"
          :contest_id="+this.$route.params.contest_id"
          @onLoading="setContestProblem(this.$route.params.contest_id)"
      /></el-tab-pane>
      <el-tab-pane label="竞赛状态"
        ><ContestStatus
          :Data="contest_solution"
          :contest="true"
          @onLoading="setContestSolution(this.$route.params.contest_id)"
      /></el-tab-pane>
      <el-tab-pane label="竞赛排名"
        ><ContestRank
          :Data="contest_rank"
          :problem="contest_problem"
          @onLoading="refurbishContestRank(this.$route.params.contest_id)"
      /></el-tab-pane>
      <el-tab-pane label="竞赛统计"
        ><ContestCount
          :Data="contest_count"
          @onLoading="setContestCount(this.$route.params.contest_id)"
      /></el-tab-pane>
      <el-tab-pane label="竞赛打印">此版块正在开发中...</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import {
  getContestProblem,
  getContestSolution,
  getContestRank,
  getContestCount,
  refurbishContestRank,
} from "@/api/contest";
import { ElLoading } from "element-plus";
import { mapState } from "vuex";

export default {
  components: {
    ContestProblem: defineAsyncComponent(() =>
      import("@/components/Problem/ProblemList.vue")
    ),
    ContestStatus: defineAsyncComponent(() =>
      import("@/components/Solution/SolutionList.vue")
    ),
    ContestRank: defineAsyncComponent(() =>
      import("@/components/Contest/ContestRank.vue")
    ),
    ContestCount: defineAsyncComponent(() =>
      import("@/components/Contest/ContestCount.vue")
    ),
  },
  computed: {
    ...mapState("contest", {
      temp_data: (state) => state.temp_contest_data,
      contest_problem: (state) => state.temp_contest_data.contest_problem,
      contest_solution: (state) => state.temp_contest_data.contest_solution,
      contest_count: (state) => state.temp_contest_data.contest_count,
      contest_rank: (state) => state.temp_contest_data.contest_rank,
    }),
  },
  data() {
    return {};
  },
  methods: {
    async setContestProblem(val) {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      if (this.temp_data.contest_id === val) {
        loading.close();
      }
      let back_data = await getContestProblem({
        contest_id: val,
      });
      if (back_data.status) {
        this.temp_data.contest_problem = this.formatContestProblem(
          back_data.message
        );
        this.temp_data.contest_id = val;
        loading.close();
      } else {
        this.contest_problem = [];
        loading.close();
      }
    },
    async setContestSolution(val) {
      let back_data = await getContestSolution({
        contest_id: val,
      });
      if (back_data.status) {
        this.temp_data.contest_solution = this.formatContestSolution(
          back_data.message
        );
        this.temp_data.contest_id = val;
      } else {
        this.contest_solution = [];
      }
    },
    async setContestRank(val) {
      let back_data = await getContestRank({
        contest_id: val,
      });
      if (back_data.status) {
        this.temp_data.contest_rank = this.formatContestRank(back_data.message);
        this.temp_data.contest_id = val;
      } else {
        this.contest_rank = [];
      }
    },
    async setContestCount(val) {
      let back_data = await getContestCount({
        contest_id: val,
      });
      if (back_data.status) {
        this.temp_data.contest_count = this.formatContestCount(
          back_data.message
        );
        this.temp_data.contest_id = val;
      } else {
        this.contest_count = [];
      }
    },
    async refurbishContestRank(val) {
      let back_data = await refurbishContestRank({
        contest_id: val,
      });
      // console.log(back_data);
      if (back_data.status) {
        this.setContestRank(val);
      } else {
        console.log(back_data.message);
      }
    },
    formatContestProblem(val) {
      return val.map((item) => ({
        problem_id: item.problem_id,
        problem_num: item.problem_num,
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
        problem_description: item.problem_description,
        time_limit: item.time_limit,
        memory_limit: item.memory_limit,
        centerDialogVisible: false,
      }));
    },
    formatContestSolution(val) {
      return val
        .map((item) => ({
          solution_id: item.solution_id,
          user_id: item.user_id,
          problem_id: item.problem_id,
          problem_num: item.problem_num,
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
    formatContestRank(val) {
      return val.map((item, index) => ({
        rank_id: index + 1,
        user_id: item.contest_user,
        name_id: item.user_nick,
        solve_number: item.contest_sum,
        solution_time: item.contest_time,
        ...item.contest_score,
      }));
    },
    formatContestCount(val) {
      return val.map((item) => ({
        problem_id: item.problem_num,
        result_type1: item.ac,
        result_type2: item.pe,
        result_type3: item.wa,
        result_type4: item.tle,
        result_type5: item.mle,
        result_type6: item.ole,
        result_type7: item.re,
        result_type8: item.ce,
        result_type9: item.tr,
        submit_total: item.total,
      }));
    },
  },
};
</script>

<style scoped>
.contest-data {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .contest-data {
    width: 100%;
  }
}
</style>
