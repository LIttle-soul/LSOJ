<template>
  <div class="contest-data">
    <el-tabs type="border-card" @tab-click="switchToTable" v-model="page_name">
      <el-tab-pane label="竞赛问题" name="problem"></el-tab-pane>
      <el-tab-pane label="竞赛状态" name="status"></el-tab-pane>
      <el-tab-pane label="竞赛排名" name="rank"></el-tab-pane>
      <el-tab-pane label="竞赛统计" name="count"></el-tab-pane>
      <el-tab-pane label="竞赛打印" name="print"></el-tab-pane>
      <router-view></router-view>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";

let router = useRouter();
let route = useRoute();

let page_name = ref(route.path.split("/").at(2));

let switchToTable = () => {
  // console.log(page_name.value);
  switch (page_name.value) {
    case "problem":
      router.push({
        path: "/contestdata/problem",
        query: { contest_id: route.query.contest_id },
      });
      break;
    case "status":
      router.push({
        path: "/contestdata/status",
        query: { contest_id: route.query.contest_id },
      });
      break;
    case "rank":
      router.push({
        path: "/contestdata/rank",
        query: { contest_id: route.query.contest_id },
      });
      break;
    case "count":
      router.push({
        path: "/contestdata/count",
        query: { contest_id: route.query.contest_id },
      });
      break;
    case "print":
      router.push({
        path: "/contestdata/print",
        query: { contest_id: route.query.contest_id },
      });
      break;
  }
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
