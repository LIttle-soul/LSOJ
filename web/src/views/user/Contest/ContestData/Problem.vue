<template>
  <div class="page">
    <ContestProblem
      :Data="temp_data.contest_problem"
      :contest="true"
      :page="page.problem_page"
      :contest_id="page.contest_id"
      @onLoading="setContestProblem"
      @handleSizeChange="problemSizeChange"
      @handleCurrentChange="problemPageChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { getContestProblem } from "@/api/contest";
import { ElLoading } from "element-plus";
import { useRoute } from "vue-router";
import { ref } from "vue";
import dayJS from "dayjs";

import ContestProblem from "@/components/Problem/ProblemList.vue";
let route = useRoute();

let temp_data = ref({
  contest_id: -1,
  contest_problem: [],
});

// 页面参数
let page = ref({
  contest_id: Number(route.query.contest_id),
  problem_page: {
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

// 数据处理
let setContestProblem = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getContestProblem({
    page: page.value.problem_page.page,
    total: page.value.problem_page.page_size,
    contest_id: page.value.contest_id,
    text: "",
  });
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
</script>

<style lang="scss" scoped></style>
