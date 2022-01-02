<template>
  <div class="page">
    <ContestStatus
      :Data="temp_data.contest_solution"
      :contest="true"
      :page="page.solution_page"
      @onLoading="setContestSolution"
      @handleSizeChange="solutionSizeChange"
      @handleCurrentChange="solutionPageChange"
      @filterSolutionList="filterSolutionList"
    />
  </div>
</template>

<script lang="ts" setup>
import { ElLoading } from "element-plus";
import { useRoute } from "vue-router";
import { ref } from "vue";
import dayJS from "dayjs";

import ContestStatus from "@/components/Solution/SolutionList.vue";
import { getSolutionDataList } from "@/api/solution";
let route = useRoute();

let temp_data = ref({
  contest_id: -1,
  contest_solution: [],
});
// 页面参数
let page = ref({
  contest_id: Number(route.query.contest_id),
  solution_page: {
    page: 1,
    page_size: 50,
    total: 0,
    run_result: "",
    language: "",
  },
});

// 页面相关事件
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
    page.value.solution_page.run_result =
      val.result.length > 0 ? val.result[0] : "";
  } else if (val.language) {
    page.value.solution_page.language =
      val.language.length > 0 ? val.language[0] : "";
  } else {
    page.value.solution_page.run_result = "";
    page.value.solution_page.language = "";
  }
  setContestSolution();
};

// 数据处理
let setContestSolution = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
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
  if (back_data.status) {
    temp_data.value.contest_solution = formatContestSolution(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.solution_page.total = back_data.total;
    loading.close();
  } else {
    temp_data.value.contest_solution = [];
    loading.close();
  }
};

// 数据格式化
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
</script>

<style lang="scss" scoped></style>
