<template>
  <div class="home-work-header">
    <el-radio-group v-model="radio" @change="handleRadioChange">
      <el-radio :label="0">全部</el-radio>
      <el-radio :label="1">已完成</el-radio>
      <el-radio :label="2">未完成</el-radio>
    </el-radio-group>
  </div>
  <div class="home-work-context">
    <el-table :data="homeWorkData" style="width: 100%">
      <el-table-column prop="course_title" label="课程名称" width="170" />
      <el-table-column prop="homework_name" label="作业名称" width="170" />
      <el-table-column prop="homework_starttime" label="开始时间" width="170" />
      <el-table-column prop="homework_endtime" label="结束时间" width="170" />
      <el-table-column prop="homework_score" label="得分" width="170" />
      <el-table-column label="操作">
        <button @click="doWork()">去作业</button>
      </el-table-column>
    </el-table>
    <el-pagination
      layout="prev, pager, next"
      :total="page.total"
      :page-size="page.page_size"
      :current-page="page.page"
      @current-change="handlePageChange"
    >
    </el-pagination>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { ElLoading } from "element-plus";
import { getTaskData } from "@/api/course";
import dayJS from "dayjs";

let page = ref({
  page: 1,
  page_size: 10,
  total: 0,
  status: 0,
  status_options: [
    { value: 0, label: "全部" },
    { value: 1, label: "已完成" },
    { value: 2, label: "未完成" },
  ],
});

let homeWorkData = ref([
  {
    homework_id: 0,
    course_title: "数据结构",
    homework_name: "数组",
    homework_starttime: "2021-11-08",
    homework_endtime: "2021-11-15",
    homework_score: 50,
  },
]);

let task_type = 0;
let radio = ref(0);

let formatData = (val: any) => {
  return val.map((item: any) => ({
    homework_id: item.task_id,
    course_title: item.course_name,
    homework_name: item.task_name,
    homework_starttime: dayJS(item.begin_time).format("YYYY-MM-DD HH:mm:ss"),
    homework_endtime: dayJS(item.end_time).format("YYYY-MM-DD HH:mm:ss"),
    homework_score: 0,
  }));
};

let handlePageChange = (val: number) => {
  page.value.page = val;
  getHomeWork();
};

let handleRadioChange = (val: number) => {
  page.value.status = val;
  getHomeWork();
};

let getHomeWork = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getTaskData({
    task_type: task_type,
    page: page.value.page,
    total: page.value.page_size,
    key: page.value.status,
  });
  console.log(back_data);
  if (back_data.status) {
    homeWorkData.value = formatData(back_data.message);
    page.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
  }
};

let handleGoLearn = (index: any, row: any) => {
  console.log(index, row);
};

let doWork = () => {
  console.log("我去做题了");
  // this.$router.push('/course/mycourse/dowork')
  router.push({
    path:'/course/${}'
  })
};
onMounted(() => {
  getHomeWork();
});
</script>

<style scoped>
button {
  background: rgb(108, 77, 243);
  border: none;
  width: 80px;
  height: 30px;
  color: whitesmoke;
  font-size: 16px;
}
</style>
