<template>
  <div class="course-show">
    <el-container>
      <el-header>
        <el-image :src="course_data.course_img"></el-image>
        <el-descriptions :title="course_data.course_title" :column="2">
          <el-descriptions-item label="开课时间" width="22.5%"
            >{{ course_data.course_begin_time }} 至
            {{ course_data.course_end_time }}</el-descriptions-item
          >
          <el-descriptions-item label="开课状态" width="22.5%">{{
            course_data.course_status
          }}</el-descriptions-item>
          <el-descriptions-item label="开课院校" width="22.5%">{{
            course_data.course_school
          }}</el-descriptions-item>
          <el-descriptions-item label="授课老师" width="22.5%">{{
            course_data.course_teacher.user_name
          }}</el-descriptions-item>
          <el-descriptions-item label="课程学分" width="22.5%"
            >{{ course_data.course_score }}分</el-descriptions-item
          >
          <el-descriptions-item label="学习人数" width="22.5%"
            >{{ course_data.course_student }}人</el-descriptions-item
          >
        </el-descriptions>
        <el-button
          type="primary"
          plain
          size="medium"
          class="course-join"
          @click="open(course_data.join_status, Number(course_data.course_id))"
        >
          {{ course_data.join_status ? "进入学习" : "立即参加" }}</el-button
        >
      </el-header>
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="课程详情" name="first">
            <div class="title">课程简介</div>
            <div class="content-text">
              <div style="text-indent: 2em; line-height: 28px">
                <CourseInfo
                  mode="preview"
                  height="100%"
                  :content="course_data.course_summary"
                />
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="课程目录" name="second">
            <div class="course-outline" style="position: relative">
              <div
                v-for="(item, index) in course_data.course_catalog"
                :key="index"
              >
                <h5 class="item">{{ item.title }}</h5>
                <ul>
                  <li
                    class="outline"
                    v-for="(item2, index2) in item.child"
                    :key="index2"
                  >
                    <span class="sb-border"> {{ item2.title }} </span>
                  </li>
                </ul>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Lock, Unlock } from "@element-plus/icons";
import dayJS from "dayjs";
import CourseInfo from "@/components/Editor/MarkdownEditor.vue";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { getCourseDetails, getCourseChapter, joinCourse } from "@/api/course";
import { format } from "echarts";

let route = useRoute();
let router = useRouter();

let activeName = ref("first");
let task = ref(true);
let radio = ref(3);

// 单课程相关数据
let course_data = ref({
  course_id: route.params.course_id,
  course_title: "数据结构",
  course_img: "",
  course_begin_time: "2021-01-01 08:00:00",
  course_end_time: "2021-08-01 16:00:00",
  course_status: "正在开课",
  course_score: 2,
  course_teacher: {
    user_id: "admin",
    user_name: "梅旭时",
  },
  course_school: "金华职业技术学院",
  course_student: 0,
  join_status: true,
  course_summary: `# Hello`,
  course_catalog: [
    {
      title: "第一章 零零零零",
      child: [
        {
          title: "第一节 树与图",
        },
        {
          title: "第二节 二叉树",
        },
      ],
    },
    {
      title: "第一章 零零零零",
      child: [
        {
          title: "第一节 树与图",
        },
        {
          title: "第二节 二叉树",
        },
      ],
    },
  ],
});

// 设置课程状态
let setCourseStatua = (begin_time: string, end_time: string) => {
  if (dayJS(begin_time).isAfter(dayJS())) {
    return "未开始";
  } else if (dayJS(end_time).isAfter(dayJS())) {
    return "正在开课";
  } else {
    return "已结束";
  }
};

let formatdata = (val: any) => {
  return {
    course_id: val.course_id,
    course_title: val.course_title,
    course_summary: val.course_introduce,
    course_img: val.course_cover,
    course_begin_time: dayJS(val.start_time).format("YYYY-MM-DD"),
    course_end_time: dayJS(val.end_time).format("YYYY-MM-DD"),
    course_status: getCourseStatus(val.start_time, val.end_time),
    course_score: val.course_credits,
    course_teacher: {
      user_id: val.course_creator,
      user_name: val.creator_name,
    },
    course_school: val.course_school.school_name || val.course_school.school_id,
    course_student: val.course_peoples,
    join_status: val.is_join,
  };
};

// 获取课程内容
let getCourseContent = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseDetails({
    course_id: course_data.value.course_id,
  });
  console.log(back_data);
  if (back_data.status) {
    course_data.value = <any>formatdata(back_data.message);
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

// 获取章节列表
let getCourseChapterlist = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseChapter({
    course_id: course_data.value.course_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    course_data.value.course_catalog = <any>(
      formatChapterData(back_data.message)
    );
    loading.close();
  } else {
    loading.close();
  }
};
// 格式化章节列表
let formatChapterData = (val: any) => {
  return val.map((res: any) => ({
    title: res.chapter_title,
    child:
      res.section_list?.map((res2: any) => ({
        title: res2.chapter_title,
      })) || [],
  }));
};

let open = (val: boolean, res: number) => {
  if (!val) {
    ElMessageBox.confirm("确定要加入这个课程吗？", "确认消息", {
      cancelButtonText: "取消",
      confirmButtonText: "确认",
      type: "warning",
    })
      .then(async () => {
        let back_data = await joinCourse({
          course_id: course_data.value.course_id,
        });
        // console.log(back_data);
        if (back_data.status) {
          getCourseContent();
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
          message: "取消报名",
        });
      });
  } else {
    router.push({
      path: `/coursedetails/${res}/chapter`,
    });
  }
};

// let handleClick = (tab: any, event: any) => {
//   console.log(tab, event);
// };
// let all_task = () => {
//   console.log(123);
// };
// let all_finish = () => {
//   console.log(456);
// };
// let all_unfinish = () => {
//   console.log(789);
// };
// let course_play = () => {
//   console.log("课程播放");
// };

onMounted(() => {
  getCourseContent();
  getCourseChapterlist();
});
</script>

<style scoped lang="scss">
.course-show {
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
  .el-header {
    height: 200px;
    .el-image {
      width: 40%;
      height: 200px;
      float: left;
    }
    .el-descriptions {
      width: 54%;
      float: left;
      margin-left: 2%;
    }
    .el-button {
      margin-left: 2%;
      float: left;
    }
  }
  .el-main {
    max-width: 1200px;
    width: 1200px;
    margin: 0 auto;
    .title {
      border: 0;
      display: block;
      width: 100%;
      background: #e2efff;
      height: 42px;
      line-height: 42px;
      font-size: 16px;
      font-weight: 550;
      color: #1d7ffd;
      letter-spacing: 5px;
      text-align: center;
    }
    .content-text {
      padding: 20px 24px;
      color: #666;
      font-size: 14px;
      line-height: 28px;
      max-width: 800px;
    }
    .course-outline {
      ul {
        .outline {
          padding-left: 20px;
          padding-right: 20px;
        }
        li {
          display: flex;
          font-family: "Arial", "Microsoft Yahei" !important;
          font-size: 14px;
          color: #666666;
          letter-spacing: 0.88px;
          height: 35px;
          line-height: 35px;
        }
      }
      .item {
        padding-left: 20px;
        padding-right: 20px;
        border: none;
        display: block;
        width: 100%;
        background: #f1faff;
        height: 42px;
        line-height: 42px;
        font-size: 16px;
        font-weight: 550;
        color: #418fbe;
        letter-spacing: 3px;
      }
      h5 {
        padding: 0;
        margin: 0;
        display: block;
        font-size: 0.83em;
        margin-block-start: 1.67em;
        margin-block-end: 1.67em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: bold;
      }
      ul,
      li {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      ul {
        display: block;
        list-style-type: disc;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
      }
    }
  }
}
</style>
