<template>
  <div class="page">
    <ContestRank
      :Data="temp_data.contest_rank"
      :page="page.rank_page"
      :problem="temp_data.contest_problem"
      @onLoading="refurbishRank"
      @handleSizeChange="rankSizeChange"
      @handleCurrentChange="rankPageChange"
    />
  </div>
</template>

<script lang="ts" setup>
import {
  getContestProblem,
  getContestRank,
  refurbishContestRank,
} from "@/api/contest";
import { ElLoading } from "element-plus";
import { useRoute } from "vue-router";
import { computed, ref } from "vue";
import dayJS from "dayjs";

import ContestRank from "@/components/Contest/ContestRank.vue";
let route = useRoute();

let temp_data = ref({
  contest_id: -1,
  contest_problem: [],
  contest_rank: [],
});

// 页面参数
let page = ref({
  contest_id: Number(route.query.contest_id),
  rank_page: {
    page: 1,
    page_size: 50,
    total: 0,
  },
});

// 页面相关事件
let rankSizeChange = (val: number) => {
  page.value.rank_page.page_size = val;
  setContestRank();
};
let rankPageChange = (val: number) => {
  page.value.rank_page.page = val;
  setContestRank();
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
    page: 1,
    total: 500,
    contest_id: page.value.contest_id,
    text: "",
  });
  if (back_data.status) {
    temp_data.value.contest_problem = formatContestProblem(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    loading.close();
  } else {
    temp_data.value.contest_problem = [];
    loading.close();
  }
};
let setContestRank = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getContestRank({
    page: page.value.rank_page.page,
    total: page.value.rank_page.page_size,
    contest_id: page.value.contest_id,
  });
  if (back_data.status) {
    temp_data.value.contest_rank = formatContestRank(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.rank_page.total = back_data.total;
    loading.close();
  } else {
    temp_data.value.contest_rank = [];
    loading.close();
  }
};
let refurbishRank = async () => {
  let back_data = await refurbishContestRank({
    contest_id: page.value.contest_id,
  });
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
</script>

<style lang="scss" scoped></style>
