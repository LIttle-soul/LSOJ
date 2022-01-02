<template>
  <div class="home-work">
    <div class="home-work-header">
      <div style="float: left">
        <el-select
          size="large"
          v-model="page.status"
          placeholder="Select"
          v-show="!page.user_identity"
          @change="handleChange"
        >
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
        <el-button
          type="primary"
          v-show="page.user_identity"
          @click="addHomeWork()"
          >新建作业</el-button
        >
        <el-button
          type="primary"
          v-show="page.user_identity"
          @click="goJobLibrary()"
          >作业库</el-button
        >
      </div>
    </div>
    <div class="home-work-line">
      <tr>
        <td class="line">
          <div></div>
        </td>
      </tr>
    </div>
    <div class="home-work-main">
      <el-card
        class="box-card"
        v-for="(item, index) in usrCourseWork"
        :key="index"
      >
        <div class="home-main-up">
          <div class="home-work-title">{{ item.work_title }}</div>
          <ul>
            <li>作业开始时间: {{ item.work_start_time }}</li>
            <li>作业结束时间: {{ item.work_end_time }}</li>
            <li>
              作业状态: {{ page.user_identity ? "已发布" : item.work_status }}
            </li>
          </ul>
        </div>
        <div style="float: right; margin-bottom: 15px; margin-top: 15px">
          <el-button
            type="primary"
            round
            size="mini"
            @click="goRelese(item.task_id)"
            v-show="page.user_identity"
            >重设发放</el-button
          >
          <el-button
            type="danger"
            round
            size="mini"
            @click="deleteTask(item.release_id)"
            v-show="page.user_identity"
            >删除</el-button
          >
          <el-button
            type="success"
            round
            size="mini"
            @click="doWork(item.task_id)"
            >{{
              page.user_identity || item.work_status === "已完成"
                ? "查看"
                : "去作业"
            }}</el-button
          >
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import dayJS from "dayjs";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { getHomeWork, deleteWork, getUserPower } from "@/api/course";
import { useRoute, useRouter } from "vue-router";

let route = useRoute();
let router = useRouter();

let page = ref({
  course_id: route.params.course_id,
  status: "",
  status_options: [
    { value: "", label: "全部" },
    { value: 1, label: "待完成" },
    { value: 2, label: "已完成" },
    { value: 3, label: "已过期" },
  ],
  user_identity: 1,
});
//用户作业数据
let usrCourseWork = ref([
  {
    task_id: 1,
    release_id: 1,
    work_title: "C语言考试",
    work_start_time: "2021-12-18",
    work_end_time: "2022-12-18",
    work_status: "",
  },
]);
let work_statu = ["", "待完成", "已完成", "已过期"];
//格式化作业数据
let formatWorkData = (val: any) => {
  return val.map((item: any) => ({
    task_id: item.task_id,
    release_id: item.release_id,
    work_title: item.task_name,
    work_start_time: dayJS(item.begin_time).format("YYYY-MM-DD"),
    work_end_time: dayJS(item.end_time).format("YYYY-MM-DD"),
    work_status: work_statu[item.task_status],
  }));
};
//获取作业数据
let getWorkData = async (val: number) => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getHomeWork({
    task_type: val,
    course_id: Number(page.value.course_id),
    key: page.value.status || "",
  });
  console.log(back_data);
  if (back_data.status) {
    usrCourseWork.value = formatWorkData(back_data.message);
    loading.close();
  } else {
    loading.close();
  }
};
//获取用户身份
let getPower = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getUserPower({
    course_id: Number(page.value.course_id),
  });
  console.log(back_data);
  if (back_data.status) {
    page.value.user_identity = back_data.message; //true 老师 flase 学生
    loading.close();
  } else {
    loading.close();
  }
};
//筛选
let handleChange = (val: number) => {
  getWorkData(0);
};

//跳转添加作业页面
let addHomeWork = () => {
  router.push({
    path: "/addhomework",
    query: {
      course_id: page.value.course_id,
      task_type: route.query.task_type,
    },
  });
};
//跳转到作业库
let goJobLibrary = () => {
  router.push({
    path: "/joblibrary",
    query: {
      course_id: page.value.course_id,
    },
  });
};
//跳转到答题页面
let doWork = (val: any) => {
  console.log(val);
  router.push({
    path: "/dowork",
    query: {
      task_id: val,
      task_type: route.query.task_type,
    },
  });
};
//删除
let deleteTask = (val: any) => {
  ElMessageBox.confirm("确定要删除这份作业吗？删除后无法恢复哦。", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      let back_data = await deleteWork({
        release_id: val,
      });
      console.log(back_data);
      if (back_data.status) {
        getWorkData(0);
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      } else {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消删除",
      });
    });
};
//重设发放
let goRelese = (val: any) => {
  router.push({
    path: "/joblibrary/relesetask",
    query: {
      course_id: page.value.course_id,
      task_id: val,
    },
  });
};
onMounted(() => {
  getWorkData(0);
  getPower();
});
</script>

<style lang="scss" scoped>
.home-work {
  max-width: 1100px;
  width: 1100px;
  margin: 10px auto;
  .home-work-header {
    margin-top: 20px;
    height: 40px;
  }
  .home-work-line {
    margin-top: 20px;
    .line div {
      margin-top: 5px;
      width: 1100px;
      height: 0;
      border-top: 2px solid var(--el-border-color-base);
    }
  }
  .home-work-main {
    margin-top: 20px;
    .box-card {
      width: 300px;
      margin-top: 20px;
      float: left;
      margin-left: 48px;
      .home-main-up {
        float: left;
        width: 300px;
        .home-work-title {
          font-size: 18px;
          font-weight: bold;
        }
        li {
          font-size: 15px;
          margin-top: 15px;
        }
      }
    }
  }
}
</style>
