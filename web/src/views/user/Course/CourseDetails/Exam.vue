<template>
  <div class="exam">
    <div class="exam-header">
      <div style="float: left">
        <el-select size="large" v-model="page.status" placeholder="Select"  @change="handleChange">
          <el-option
            v-for="(item, index) in page.status_options"
            :key="index"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </div>
      <div style="float: right">
        <el-button type="primary" @click="addExam" v-show="page.user_identity">新建试卷</el-button>
        <el-button type="primary" @click="goExamLibrary" v-show="page.user_identity">试卷库</el-button>
      </div>
    </div>
    <div class="exam-line">
      <tr>
        <td class="line">
          <div></div>
        </td>
      </tr>
    </div>
    <div class="exam-main">
      <el-card
        class="box-card"
        v-for="(item, index) in courseExam"
        :key="index"
      >
        <div class="exam-main-up">
          <div class="exam-title">{{ item.exam_title }}</div>
          <ul>
            <li class="testconter">考试开始时间: {{ item.exam_start_time }}</li>
            <li class="testconter">考试结束时间: {{ item.exam_end_time }}</li>
            <li class="testconter">
              考试任务点百分比: {{ item.exam_percent }}
            </li>
            <li class="testconter">提交数: {{ item.exam_submit }}</li>
            <li class="testconter">状态: {{ item.user_identity > 1 ? "已发布" : item.exam_status}}</li>
          </ul>
        </div>
        <div class="exam-main-under">
          <el-button
            type="primary"
            round
            size="mini"
            @click="goRelese(item.task_id)"
            v-show="page.user_identity"
            >重设发放</el-button
          >
          <el-button
            type="success"
            round
            size="mini"
            @click="doWork(item.task_id)"

            >{{ page.user_identity === 1||item.exam_statu === 0 ? "查看" : "去考试"}}</el-button
          >
          <el-button
            type="danger"
            round
            size="mini"
            @click="deleteTask(item.release_id)"
            v-show="page.user_identity"
            >删除</el-button
          >
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { getHomeWork } from "../../../../api/course";
import { ElLoading } from "element-plus";
import dayJS from "dayjs";

let router = useRouter();
let route = useRoute();

let page = ref({
  status: "",
  status_options: [
    { value: "", label: "全部" },
    { value: 1, label: "待完成" },
    { value: 2, label: "已完成" },
    { value: 3, label: "已过期" },
  ],
  user_identity: 1,
});

//考试虚拟数据
let courseExam = ref([
  {
    task_id: 1,
    release_id: 1,
    user_identity:1,
    exam_statu: 1,
    exam_title: "C语言考试",
    exam_start_time: "2020-02-03",
    exam_end_time: "2020-02-05",
    exam_percent: "100%",
    exam_submit: 40,
    exam_status: "已过期/未作答/已完成",
  },
  {
    task_id: 1,
    release_id: 1,
    user_identity:2,
    exam_statu: 0,
    exam_title: "C语言考试",
    exam_start_time: "2020-02-03",
    exam_end_time: "2020-02-05",
    exam_percent: "100%",
    exam_submit: 40,
    exam_status: "已过期/未作答/已完成",
  },
]);
//格式化试卷数据
let formatWorkData = (val: any) => {
  return val.map((item: any) => ({
    task_id: item.task_id,
    release_id: item.release_id,
    exam_title: item.task_name,
    exam_start_time: dayJS(item.begin_time).format("YYYY-MM-DD"),
    exam_end_time: dayJS(item.end_time).format("YYYY-MM-DD"),
    exam_percent: item.exam_percent,
    exam_submit: item.exam_submit,
    work_status: "已过期",
  }));
};
//获取试卷数据
let getExamData = async (val: number) => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  // let back_data = await getHomeWork({
  //   task_type: val,
  //   course_id: Number(route.query.id),
  // });
  // console.log(back_data);
  // if (back_data.status) {
  //   courseExam.value = formatWorkData(back_data.message);
  //   loading.close();
  // } else {
  //   loading.close();
  // }
};

// 新建试卷
let addExam = () => {
  router.push({
    path: "/addhomework",
    query: {
      course_id: route.query.course_id,
      task_type: route.query.task_type,
    },
  });
};
//跳转到试卷库
let goExamLibrary = () => {
  router.push({
    path: "/joblibrary",
    query: {
      course_id: route.query.course_id,
      task_type: route.query.task_type,
    },
  });
};
// 试卷查看
let ExamDetail = () => {
  router.push({
    path: "/ExamDetail",
  });
};
let goRelese = (val: any) => {
  router.push({
    path: "/joblibrary/relesetask",
    query: {
      course_id: route.query.course_id,
      task_id: val,
    },
  });
};
let handleChange = () => {
  console.log(1254563);
}; 
onMounted(() => {
  // getWorkData(2);
});
</script>

<style lang="scss" scoped>
.exam {
  max-width: 1100px;
  width: 1100px;
  margin: 10px auto;
  .exam-header {
    margin-top: 20px;
    height: 40px;
  }
  .exam-line {
    margin-top: 20px;
    .line div {
      margin-top: 5px;
      width: 1100px;
      height: 0;
      border-top: 2px solid var(--el-border-color-base);
    }
  }
  .exam-main {
    margin-top: 20px;
    .box-card {
      width: 300px;
      margin-top: 20px;
      float: left;
      margin-left: 48px;
      .exam-main-up {
        float: left;
        height: 180px;
        width: 300px;
        // background: antiquewhite;
      }
    }
    .exam-main-under {
      float: right;
      margin-bottom: 15px;
    }
    .exam-title {
      font-size: 18px;
      font-weight: bold;
    }
    li {
      font-size: 15px;
      margin-top: 15px;
    }
  }
}
</style>
