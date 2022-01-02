<template>
  <div
    class="my-course-list"
    v-for="(item, index) in myCourseData"
    :key="index"
  >
    <el-image :src="item.course_img"></el-image>
    <div class="my-course-list-details">
      <h1>{{ item.course_title }}</h1>
      <div class="my-course-list-details-child">
        <p>开课时间:{{ item.start_time }}</p>
        <p>结束时间:{{ item.end_time }}</p>
        <p>课程讲师:{{ item.course_teacher }}</p>
        <p>状态:{{ item.course_status }}</p>
      </div>
    </div>
    <div class="right-button">
      <el-button type="primary" @click="linkTo(item.course_id)"
        >进入学习</el-button
      >
    </div>
  </div>
  <div class="footer-page">
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
import { getCourseList } from "@/api/course";
import { useRouter } from "vue-router";
import dayJS from "dayjs";

let router = useRouter();

let page = ref({
  page: 1,
  page_size: 10,
  total: 20,
});

let myCourseData = ref([
  {
    course_id: 0,
    course_img: "",
    course_title: "数据结构",
    start_time: "2021-12-16 12:00:00",
    end_time: "2022-12-16 12:00:00",
    course_teacher: "梅旭时",
    course_status: "已结课",
  },
]);

let formatData = (val: any) => {
  return val.map((item: any) => ({
    course_id: item.course_id,
    course_img: item.course_cover,
    course_title: item.course_name,
    start_time: dayJS(item.start_time).format("YYYY-MM-DD HH:mm:ss"),
    end_time: dayJS(item.end_time).format("YYYY-MM-DD HH:mm:ss"),
    course_teacher: item.creator_name,
    course_status: getCourseStatus(item.start_time, item.end_time),
  }));
};

let handlePageChange = (val: number) => {
  page.value.page = val;
  getMyCourseList();
};
let getMyCourseList = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseList({
    page: page.value.page,
    total: page.value.page_size,
    sort_by: "",
    key: "",
    text: "",
    subject: "",
    me: true,
  });
  console.log(back_data);
  if (back_data.status) {
    myCourseData.value = formatData(back_data.message);
    page.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
  }
};

let getCourseStatus = (start_time: any, end_time: any) => {
  if (dayJS().isBefore(dayJS(start_time))) {
    return "未开课";
  } else if (dayJS().isAfter(dayJS(end_time))) {
    return "已结课";
  } else {
    return "正在开课";
  }
};

let linkTo = (val: number) => {
  router.push({
    path: "/coursedetails/chapter",
    query: {
      id: val,
    },
  });
};

onMounted(() => {
  getMyCourseList();
});
</script>

<style scoped lang="scss">
.my-course-list {
  height: 150px;
  // background: rgb(228, 225, 225);
  display: flex;
  margin-top: 5px;

  position: relative;
  .el-image {
    width: 225px;
    height: 150px;
  }
  .my-course-list-details-child {
    margin-top: 10px;
    margin-left: 20px;
    line-height: 23px;
  }
  h1 {
    margin-left: 20px;
    font: 1.5em sans-serif;
    font-weight: 540;
    margin-top: 10px;
  }
  .right-button {
    width: 60px;
    height: 150px;
    margin-left: 60px;
    position: relative;
    .el-button {
      position: absolute;
      bottom: 10px;
    }
  }
}
</style>
