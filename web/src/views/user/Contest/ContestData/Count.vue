<template>
  <div class="page">
    <ContestCount
      :Data="temp_data.contest_count"
      :page="page.count_page"
      @onLoading="setContestCount"
      @handleSizeChange="countSizeChange"
      @handleCurrentChange="countPageChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { getContestCount } from "@/api/contest";
import { ElLoading } from "element-plus";
import { useRoute } from "vue-router";
import { ref } from "vue";
import ContestCount from "@/components/Contest/ContestCount.vue";
let route = useRoute();

let temp_data = ref({
  contest_id: -1,
  contest_count: [],
});

// 页面参数
let page = ref({
  contest_id: Number(route.query.contest_id),
  count_page: {
    page: 1,
    page_size: 50,
    total: 0,
  },
});

// 页面相关事件
let countSizeChange = (val: number) => {
  page.value.count_page.page_size = val;
  setContestCount();
};
let countPageChange = (val: number) => {
  page.value.count_page.page = val;
  setContestCount();
};

// 数据处理

let setContestCount = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getContestCount({
    page: page.value.count_page.page,
    total: page.value.count_page.page_size,
    contest_id: page.value.contest_id,
  });
  if (back_data.status) {
    temp_data.value.contest_count = formatContestCount(back_data.message);
    temp_data.value.contest_id = page.value.contest_id;
    page.value.count_page.total = back_data.total;
    loading.close();
  } else {
    temp_data.value.contest_count = [];
    loading.close();
  }
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

<style lang="scss" scoped></style>
