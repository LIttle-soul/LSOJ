<template>
  <div class="relese-task">
    <div class="relese-task-header">
      <div class="relese-task-header-title">作业标题:</div>
      <div class="relese-task-header-input">
        <el-input
          type="text"
          v-model="release.title"
          placeholder="Please input"
        />
      </div>
      <div style="float: right; margin-right: 20px">
        <el-button type="warning" size="medium" @click="Unpublish()"
          >返回</el-button
        >
      </div>
    </div>
    <div class="relese-task-main">
      <div class="relese-task-main-people">发送对象</div>
      <div class="relese-task-main-checkbox">
        <el-checkbox
          v-model="release.all_send"
          @change="handleCheckboxClick"
          size="medium"
        >
          全部
        </el-checkbox>
        <el-checkbox-group v-model="form_data.class_list">
          <el-checkbox
            v-for="(city, index) in release.class_list"
            :key="index"
            :label="city.class_id"
            >{{ city.class_name }}</el-checkbox
          >
        </el-checkbox-group>
      </div>
      <div class="relese-task-main-time">发送时间:</div>
      <div class="relese-task-main-date-picker">
        <!-- <el-date-picker
          v-model="release.time"
          type="daterange"
          unlink-panels
          range-separator="To"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          value-format="YYYY-MM-DD"
        >
        </el-date-picker> -->
        <el-date-picker
          v-model="release.time"
          type="datetimerange"
          start-placeholder="Start Date"
          end-placeholder="End Date"
          value-format="YYYY-MM-DD HH:mm:ss"
        >
        </el-date-picker>
      </div>
      <div class="relese-task-main-judge">
        是否自动判题(选择/判断)<el-switch
          style="margin-left: 20px"
          :width="45"
          v-model="task_judge"
          active-color="#13ce66"
          inactive-color="#ff4949"
        />
      </div>

      <div class="relese-task-answer-time">答题时间设置(min/分钟):</div>
      <div style="float: left; margin-top: 15px; margin-left: 20px">
        <el-input
          type="text"
          v-model="release.time_min"
          placeholder="Please input"
        />
      </div>
      <div
        class="relese-task-footer"
        style="margin-top: 200px; margin-left: 450px"
      >
        <el-button
          type="success"
          round
          size="medium"
          style="width: 150px; height: 50px"
          @click="releaseTask(release, form_data.class_list)"
          >发布</el-button
        >
        <el-button
          type="success"
          round
          size="medium"
          style="width: 150px; height: 50px"
          @click="Unpublish()"
          >取消</el-button
        >
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { ElLoading, ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";
import { getCourseClass, postreleaseTaskData } from "@/api/course";
import { number } from "echarts";

let route = useRoute();
let router = useRouter();

let release = ref({
  class_list: [{ class_id: 1, class_name: "软件120" }],
  all_send: false,
  time: "",
  title: "",
  time_min: "",
});
let task_type = 0;
let task_judge = ref(true);
let form_data = ref({
  class_list: <any>[],
});

let handleCheckboxClick = (val: boolean) => {
  form_data.value.class_list = val
    ? release.value.class_list.map((res: any) => res.class_id)
    : [];
};

let releaseTask = (val: any, res: any) => {
  console.log(typeof val.title);
  postreleaseTask(val, res);
};
//获取班级列表
let getClassList = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseClass({
    course_id: route.query.course_id,
  });
  console.log(back_data.message);
  if (back_data.status) {
    release.value.class_list = back_data.message.map((res: any) => ({
      class_id: res.class_id,
      class_name: res.class_name,
    }));
    loading.close();
  } else {
    loading.close();
  }
};
//上传发放作业的数据
let postreleaseTask = async (val: any, item: any) => {
  //val标题，res时间，item班级列表
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  console.log(task_judge);
  let back_data = await postreleaseTaskData({
    task_type: task_type,
    task_judge: task_judge.value,
    course_id: route.query.course_id,
    task_id: route.query.task_id,
    title: val.title,
    time: val.time,
    class_lists: item,
    time_min: val.time_min,
  });
  console.log(back_data.message);
  if (back_data.status) {
    loading.close();
    ElMessage({
      message: back_data.message,
      type: "success",
    });
    router.push({
      path: "/joblibrary",
      query: {
        course_id: route.query.course_id,
      },
    });
  } else {
    loading.close();
    ElMessage.error(back_data.message);
  }
};
//取消发布
let Unpublish = async () => {
  router.push({
    path: "/joblibrary",
    query: {
      course_id: route.query.course_id,
    },
  });
};
onMounted(() => {
  getClassList();
});
</script>

<style scoped lang="scss">
.relese-task {
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
  .relese-task-header {
    height: 40px;
    .relese-task-header-title {
      float: left;
      font-size: 20px;
      font-weight: bold;
      margin-top: 10px;
    }
    .relese-task-header-input {
      float: left;
      width: 200px;
      margin-left: 20px;
    }
  }
  .relese-task-main {
    margin-top: 50px;
    // height: 500px;
    // background: red;
    .relese-task-main-people {
      float: left;
      font-size: 20px;
      height: 30px;
      width: 100%;
      //   background: blueviolet;
      font-weight: bold;
    }
    .relese-task-main-checkbox {
      margin-top: 50px;
      margin-left: 20px;
      //   height: 200px;
      width: 90%;
      //   background: bisque;
    }
    .relese-task-main-time {
      float: left;
      font-size: 20px;
      height: 30px;
      margin-top: 20px;
      font-weight: bold;
    }
    .relese-task-main-date-picker {
      float: left;
      margin-top: 10px;
      margin-left: 20px;
      width: 80%;
    }
    .relese-task-main-judge {
      float: left;
      font-size: 20px;
      margin-top: 30px;
      height: 30px;
      width: 100%;
      //   background: blueviolet;
      font-weight: bold;
    }
    .relese-task-answer-time {
      float: left;
      font-size: 20px;
      height: 30px;
      margin-top: 20px;
      font-weight: bold;
    }
  }
}
</style>
