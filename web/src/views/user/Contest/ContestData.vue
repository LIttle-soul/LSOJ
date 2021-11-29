<template>
  <div class="contest-data">
    <el-tabs type="border-card">
      <el-tab-pane label="竞赛问题"
        ><ContestProblem
          :Data="temp_data.contest_problem"
          :contest="true"
          :page="page.problem_page"
          :contest_id="page.contest_id"
          @onLoading="setContestProblem"
          @handleSizeChange="problemSizeChange"
          @handleCurrentChange="problemPageChange"
      /></el-tab-pane>
      <el-tab-pane label="竞赛状态"
        ><ContestStatus
          :Data="temp_data.contest_solution"
          :contest="true"
          :page="page.solution_page"
          @onLoading="setContestSolution"
          @handleSizeChange="solutionSizeChange"
          @handleCurrentChange="solutionPageChange"
          @filterSolutionList="filterSolutionList"
      /></el-tab-pane>
      <el-tab-pane label="竞赛排名"
        ><ContestRank
          :Data="temp_data.contest_rank"
          :page="page.rank_page"
          :problem="temp_data.contest_problem"
          @onLoading="refurbishRank"
          @handleSizeChange="rankSizeChange"
          @handleCurrentChange="rankPageChange"
      /></el-tab-pane>
      <el-tab-pane label="竞赛统计"
        ><ContestCount
          :Data="temp_data.contest_count"
          :page="page.count_page"
          @onLoading="setContestCount"
          @handleSizeChange="countSizeChange"
          @handleCurrentChange="countPageChange"
      /></el-tab-pane>
      <el-tab-pane label="竞赛打印">此版块正在开发中...</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import {
  getContestProblem,
  getContestRank,
  getContestCount,
  refurbishContestRank,
} from "@/api/contest";
import { ElLoading } from "element-plus";
import { useStore, mapState } from "vuex";
import { useRoute } from "vue-router";
import { computed, ref } from "vue";
import dayJS from "dayjs";

import ContestProblem from "@/components/Problem/ProblemList.vue";
import ContestStatus from "@/components/Solution/SolutionList.vue";
import ContestRank from "@/components/Contest/ContestRank.vue";
import ContestCount from "@/components/Contest/ContestCount.vue";
import { getSolutionDataList } from "@/api/solution";

let store = useStore();
let route = useRoute();

let temp_data = computed(
  mapState("contest", ["temp_contest_data"]).temp_contest_data.bind({
    $store: store,
  })
);

// 页面参数
let page = ref({
  contest_id: +route.params.contest_id,
  problem_page: {
    page: 1,
    page_size: 50,
    total: 0,
  },
  solution_page: {
    page: 1,
    page_size: 50,
    total: 0,
    run_result: "",
    language: "",
  },
  rank_page: {
    page: 1,
    page_size: 50,
    total: 0,
  },
  count_page: {
    page: 1,
    page_size: 50,
    total: 0,
  },
});

// 页面相关事件
let problemSizeChange = (val: number) => {
  page.value.problem_page.page_size = val;
  setContestProblem();
};
let problemPageChange = (val: number) => {
  page.value.problem_page.page = val;
  setContestProblem();
};
let solutionSizeChange = (val: number) => {
  page.value.solution_page.page_size = val;
  setContestSolution();
};
let solutionPageChange = (val: number) => {
  page.value.solution_page.page = val;
  setContestSolution();
};
let filterSolutionList = (val: any) => {
  if (val.result) {
    page.value.solution_page.run_result = val.result.length > 0 ? val.result[0] : "";
  } else if (val.language) {
    page.value.solution_page.language = val.language.length > 0 ? val.language[0] : "";
  } else {
    page.value.solution_page.run_result = "";
    page.value.solution_page.language = "";
  }
  setContestSolution();
};
let rankSizeChange = (val: number) => {
  page.value.rank_page.page_size = val;
  setContestRank();
};
let rankPageChange = (val: number) => {
  page.value.rank_page.page = val;
  setContestRank();
};
let countSizeChange = (val: number) => {
  page.value.count_page.page_size = val;
  setContestCount();
};
let countPageChange = (val: number) => {
  page.value.count_page.page = val;
  setContestCount();
};

// 数据处理
let setContestProblem = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  if (temp_data.value.contest_id === page.value.contest_id) {
    loading.close();
  }
  let back_data = await getContestProblem({
    page: page.value.problem_page.page,
    total: page.value.problem_page.page_size,
    contest_id: page.value.contest_id,
    text: "",
  });
  // console.log(back_data);
  if (back_data.status) {
    temp_data.value.contest_problem = formatContestProblem(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.problem_page.total = back_data.total;
    loading.close();
  } else {
    temp_data.value.contest_problem = [];
    loading.close();
  }
};
let setContestSolution = async () => {
  let back_data = await getSolutionDataList({
    page: page.value.solution_page.page,
    total: page.value.solution_page.page_size,
    key: "",
    text: "",
    run_result: page.value.solution_page.run_result.toString() || "",
    language: page.value.solution_page.language.toString() || "",
    me: false,
    contest_id: page.value.contest_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    temp_data.value.contest_solution = formatContestSolution(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.solution_page.total = back_data.total;
  } else {
    temp_data.value.contest_solution = [];
  }
};
let setContestRank = async () => {
  let back_data = await getContestRank({
    page: page.value.rank_page.page,
    total: page.value.rank_page.page_size,
    contest_id: page.value.contest_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    temp_data.value.contest_rank = formatContestRank(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.rank_page.total = back_data.total;
  } else {
    temp_data.value.contest_rank = [];
  }
};
let setContestCount = async () => {
  let back_data = await getContestCount({
    page: page.value.count_page.page,
    total: page.value.count_page.page_size,
    contest_id: page.value.contest_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    temp_data.value.contest_count = formatContestCount(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.count_page.total = back_data.total;
  } else {
    temp_data.value.contest_count = [];
  }
};
let refurbishRank = async () => {
  let back_data = await refurbishContestRank({
    contest_id: page.value.contest_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    setContestRank();
  } else {
    console.log(back_data.message);
  }
};

// 数据格式化
let formatContestProblem = (val: any) => {
  return val.map((item: any) => ({
    problem_id: item.problem_id,
    problem_num: item.problem_num,
    problem_title: item.problem_title,
    problem_degree: item.problem_difficult,
    problem_tag: item.problem_tag,
    problem_solved: item.problem_accepted,
    problem_submit: item.problem_submit,
    problem_status: item.problem_status,
    problem_source: item.problem_course,
    creation_time: dayJS(item.creation_time).format("YYYY-MM-DD HH:mm:ss"),
    submit_status: item.pass_status,
    problem_description: item.problem_description,
    time_limit: item.time_limit,
    memory_limit: item.memory_limit,
    centerDialogVisible: false,
  }));
};
let formatContestSolution = (val: any) => {
  return val.map((item: any) => ({
    solution_id: item.solution_id,
    user_id: item.user_id,
    problem_id: item.problem_id,
    problem_num: item.problem_num,
    solution_result: item.run_result,
    solution_memory: item.run_memory,
    solution_consuming: item.run_time,
    solution_language: item.solution_language,
    solution_length: item.code_length,
    solution_time: dayJS(item.solution_time).format("YYYY-MM-DD HH:mm:ss"),
  }));
};
let formatContestRank = (val: any) => {
  return val.map((item: any, index: number) => ({
    rank_id: index + 1,
    user_id: item.contest_user,
    name_id: item.user_nick,
    solve_number: item.contest_sum,
    solution_time: item.contest_time,
    ...item.contest_score,
  }));
};
let formatContestCount = (val: any) => {
  return val.map((item: any) => ({
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
};
</script>

<style scoped lang="scss">
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
