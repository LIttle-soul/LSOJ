<template>
  <div class="home-work-header">
    <el-radio-group v-model="radio" @change="handleRadioChange">
      <el-radio :label="0">全部</el-radio>
      <el-radio :label="1">已完成</el-radio>
      <el-radio :label="2">未完成</el-radio>
    </el-radio-group>
  </div>
  <div class="home-work-context">
    <el-table :data="examData" style="width: 100%">
      <el-table-column prop="course_title" label="课程名称" width="170" />
      <el-table-column prop="exam_name" label="考试名称" width="170" />
      <el-table-column prop="exam_starttime" label="开始时间" width="170" />
      <el-table-column prop="exam_endtime" label="结束时间" width="170" />
      <el-table-column prop="exam_score" label="得分" width="170" />
      <el-table-column label="操作">
        <button @click="doWork()">去考试</button>
        <!-- <template #default="scope">
          <el-button
            class="learn_btn"
            @click="handleGoLearn(scope.$index, scope.row)"
            >去学习</el-button
          >
        </template> -->
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
import { ref, onMounted } from "vue";
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

let examData = ref([
  {
    exam_id: 0,
    course_title: "数据结构",
    exam_name: "数组",
    exam_starttime: "2021-11-08",
    exam_endtime: "2021-11-15",
    exam_score: 50,
  },
]);

let task_type = 2;
let radio = ref(0);

let formatData = (val: any) => {
  return val.map((item: any) => ({
    exam_id: item.task_id,
    course_title: item.course_name,
    exam_name: item.task_name,
    exam_starttime: dayJS(item.begin_time).format("YYYY-MM-DD HH:mm:ss"),
    exam_endtime: dayJS(item.end_time).format("YYYY-MM-DD HH:mm:ss"),
    exam_score: 0,
  }));
};

let handlePageChange = (val: number) => {
  page.value.page = val;
  getExam();
};

let handleRadioChange = (val: number) => {
  page.value.status = val;
  getExam();
};

let getExam = async () => {
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
    examData.value = formatData(back_data.message);
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
  // router.push('/course/mycourse/dowork');
};

onMounted(() => {
  getExam();
});
</script>

<style scoped lang="scss">
button {
  background: rgb(108, 77, 243);
  border: none;
  width: 80px;
  height: 30px;
  color: whitesmoke;
  font-size: 16px;
}
</style>
