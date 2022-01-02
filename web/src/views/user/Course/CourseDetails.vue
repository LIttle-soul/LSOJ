<template>
  <div class="chapter-list">
    <el-tabs v-model="activateName" @tab-click="handleClick">
      <el-tab-pane label="课程目录" name="chapter"></el-tab-pane>
      <el-tab-pane label="课程统计" name="counter"></el-tab-pane>
      <el-tab-pane label="课程作业" name="homework"></el-tab-pane>
      <el-tab-pane label="课程考试" name="exam"></el-tab-pane>
      <el-tab-pane label="课程资料" name="datum"></el-tab-pane>
      <el-tab-pane label="课程题库" name="questionbank"></el-tab-pane>
      <el-tab-pane label="课程讨论" name="discuss"></el-tab-pane>
      <router-view></router-view>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

let route = useRoute();
let router = useRouter();

let activateName = ref(route.path?.split("/").at(-1));
// console.log(route.params, activateName.value);
let page = ref({
  course_id: route.params.course_id,
});

let handleClick = () => {
  switch (activateName.value) {
    case "chapter":
      router.push({
        path: `/coursedetails/${page.value.course_id}/chapter`,
      });
      break;
    case "counter":
      router.push({
        path: `/coursedetails/${page.value.course_id}/counter`,
      });
      break;
    case "homework":
      router.push({
        path: `/coursedetails/${page.value.course_id}/homework`,
        query: {
          task_type: 0,
        },
      });
      break;
    case "exam":
      router.push({
        path: `/coursedetails/${page.value.course_id}/exam`,
        query: {
          task_type: 2,
        },
      });
      break;
    case "datum":
      router.push({
        path: `/coursedetails/${page.value.course_id}/datum`,
      });
      break;
    case "questionbank":
      router.push({
        path: `/coursedetails/${page.value.course_id}/questionbank`,
      });
      break;
    case "discuss":
      router.push({
        path: `/coursedetails/${page.value.course_id}/discuss`,
      });
      break;
  }
};
</script>

<style scoped lang="scss">
.chapter-list {
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
}
</style>
