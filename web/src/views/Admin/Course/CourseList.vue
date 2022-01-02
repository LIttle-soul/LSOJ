<template>
  <div class="course-list">
    <el-card>
      <div class="heard">
        <div class="heardleft">
          <el-icon :size="25" class="icon"></el-icon>课程列表
        </div>
        <el-input placeholder="请输入内容" size="small" v-model="page.text" class="input-with-select"
          @keydown.enter="search_all_data(page.text)">
          <template #prefix>
            <el-icon color="#AAAAAA" style="font-size: 1.1rem; transform: translateY(7px)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-394d1fd8="">
                <path fill="currentColor"
                  d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704z">
                </path>
              </svg>
            </el-icon>
          </template>
          <template #append>
            <el-button @click="search_all_data(page.text)">搜索</el-button>
          </template>
        </el-input>
      </div>
      <div class="conter">
        <el-table :data="courseExam" style="width: 100%" border size="medium">
          <el-table-column prop="course_name" label="课程标题" width="100" />
          <el-table-column prop="course_teacher" label="课程创建老师" width="120" />
          <!-- <el-table-column prop="course_school" label="课程学校" width="120" /> -->
          <el-table-column prop="course_credit" label="课程学分" width="100" />
          <el-table-column prop="course_create_time" label="课程创建时间" width="210" />
          <el-table-column prop="course_start_time" label="课程开始时间" width="210" />
          <el-table-column prop="course_end_time" label="课程结束时间" width="210" />
          <el-table-column label="操作" width="207">
            <template #default="scope">
              <el-button type="primary" :icon="Edit" circle size="mini" @click="goCourseShow(scope.row.course_id)"
                style="margin-left:10px"></el-button>
              <el-switch v-model="scope.row.is_show" active-color="#13ce66" inactive-color="#ff4949"
                @click="showCourseData(scope.row.course_id)" style="margin-left:10px" />
              <el-button type="danger" :icon="Delete" circle size="mini" @click="deleteTask(scope.row.course_id)"
                style="margin-left:10px"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="bottom">
        <el-pagination v-model:currentPage="page.page" :page-sizes="[20, 40, 60, 80]" :page-size="page.page_size"
          layout="sizes, prev, pager, next" :total="page.total" @size-change="handleSizeChange"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import dayJS from "dayjs";
import { getCourseData, deleteCourse, showCourse } from "../../../api/course";
import { ElLoading } from "element-plus";
import {
  Edit,
  Share,
  Delete,
  Search,
  Upload,
  Check,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

let page = ref({
  page: 1,
  total: 0,
  page_size: 5,
  text: "",
});

let route = useRoute();
let router = useRouter();

let search_all_data = (text: string) => {
  console.log(text);
  page.value.text = text || "";
  console.log(page.value.text);
  getCourse();
};

let handleSizeChange = (val: any) => {
  page.value.page_size = val;
  getCourse();
};

let handleCurrentChange = (val: any) => {
  page.value.page = val;
  getCourse();
};

//课程虚拟数据
let courseExam = ref([
  {
    course_id: 1,
    course_name: "数据结构",
    course_teacher: "梅旭时",
    course_school: "金华职业技术学院",
    course_credit: 0,
    course_create_time: "2021-12-20",
    course_start_time: "2021-12-20",
    course_end_time: "2021-12-20",
    value: "100",
  },
]);

//格式化课程数据
let formatCourseData = (val: any) => {
  return val.map((item: any) => ({
    course_id: item.course_id,
    course_name: item.course_name,
    course_teacher: item.course_teacher,
    course_school: item.course_school,
    course_credit: item.course_credit,
    course_create_time: dayJS(item.create_time).format("YYYY-MM-DD"),
    course_start_time: dayJS(item.start_time).format("YYYY-MM-DD"),
    course_end_time: dayJS(item.end_time).format("YYYY-MM-DD"),
    is_show: item.is_show,
  }));
};
//获取课程数据
let getCourse = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseData({
    page: page.value.page,
    total: page.value.page_size,
    text: page.value.text || "",
  });
  console.log(back_data);
  if (back_data.status) {
    courseExam.value = formatCourseData(back_data.message);
    page.value.total = back_data.total;
    loading.close();
  }
};

//显示课程数据
let showCourseData = async (val: any) => {
  let back_data = await showCourse({
    course_id: val,
  });
  console.log(back_data);
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  }
};

//删除课程
let deleteTask = async (val: any) => {
  ElMessageBox.confirm("确定要删除这门课程删除后无法恢复哦。", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      let back_data = await deleteCourse({
        course_id: val,
      });
      console.log(back_data);
      if (back_data.status) {
        getCourse();
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
//跳转到课程详情页面
let goCourseShow = (val: any) => {
  router.push({
    path: "/admin/addcourse/",
    query: {
      course_id: val,
    },
  });
};

onMounted(() => {
  getCourse();
});
</script>

<style scoped>
.course-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .course-list {
    width: 100%;
  }
}
.heard {
  height: 50px;
  width: 100%;
  border-bottom: solid rgb(204, 202, 202) 1px;
}
.heardleft {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  float: left;
}
.heardleft .icon {
  transform: translateY(5px);
}
.input-with-select {
  width: 230px;
  margin-left: 820px;
}
.conter {
  margin-top: 20px;
}
.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;
}
.buttona {
  width: 30px;
  height: 30px;
}
.bottom {
  margin-left: 400px;
}
</style>