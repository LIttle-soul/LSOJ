<template>
  <div class="job-library">
    <div class="job-library-header">
      <div style="float: left">
        <el-input
          placeholder="请输入内容"
          size="small"
          v-model="search_text"
          class="input-with-select"
          @keydown.enter="search_all_data(search_text)"
        >
          <template #prefix>
            <el-icon
              color="#AAAAAA"
              style="font-size: 1.1rem; transform: translateY(7px)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1024 1024"
                data-v-394d1fd8=""
              >
                <path
                  fill="currentColor"
                  d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704z"
                ></path>
              </svg>
            </el-icon>
          </template>
          <template #append>
            <el-button @click="search_all_data(search_text)">搜索</el-button>
          </template>
        </el-input>
      </div>
      <div style="float: right">
        <el-button type="success" @click="addHomeWork">新建作业/考试</el-button>
      </div>
    </div>
    <el-table :data="jobLibrary" border class="job-library-main">
      <el-table-column prop="homework_title" label="标题" width="400" />
      <el-table-column prop="type" label="类型" width="80" />
      <el-table-column prop="creator" label="创建者" width="100" />
      <el-table-column prop="creator_time" label="创建日期" />
      <el-table-column label="操作">
        <template #default="scope">
          <div class="button-box">
            <el-button
              size="medium"
              type="primary"
              circle
              @click="handleEditClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
            </el-button>
            <el-button
              size="medium"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
              style="margin-left: 20px"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
            <el-button
              type="success"
              round
              style="margin-left: 80px"
              @click="handleReleaseClick(scope.row)"
            >
              发布
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { gettask,deleteTask } from "@/api/course";
import { useRoute, useRouter } from "vue-router";
import dayJS from "dayjs";
import router from "../../../router";

let route = useRoute();
let search_text = ref("");
let search_all_data = (text: string) => {
  page.value.text = text || "";
};

let page = ref({
  text: "",
});
//作业库虚拟数据
let jobLibrary = ref([
  {
    task_id: 4,
    homework_title: "法国坏块给",
    creator: "烟雨",
    creator_time: "2021-12-16 12:00:00",
  },
]);
let task_type = 0;
//格式化作业库数据
let formatData = (val: any) => {
  return val.map((item: any) => ({
    task_id: item.task_id,
    homework_title: item.task_name,
    creator: item.task_creator,
    creator_time: dayJS(item.create_time).format("YYYY-MM-DD"),
  }));
};
//获取作业库数据
let getJobLibraryData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await gettask({
    course_id: Number(route.query.course_id),
    task_type: task_type,
  });
  console.log(back_data);
  if (back_data.status) {
    jobLibrary.value = formatData(back_data.message);
    loading.close();
  } else {
    loading.close();
  }
};
//发布作业
let handleReleaseClick = (val: any) => {
  router.push({
    path: "/joblibrary/relesetask",
    query: {
      course_id: route.query.course_id,
      task_id: val.task_id,
    },
  });
};
//跳转添加作业页面
let handleEditClick = (val: any) => {
  router.push({
    path: "/addhomework",
    query: {
      task_id: val.task_id,
    },
  });
};
//删除作业
let handleDeleteClick = (val: any) => {
  ElMessageBox.confirm("确定要删除这份作业吗？删除后无法恢复哦。", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      let back_data = await deleteTask({
        task_id: val.task_id,
      });
      console.log(back_data);
      if (back_data.status) {
        getJobLibraryData();
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
//跳转添加作业页面
let addHomeWork = () => {
  router.push({
    path: "/addhomework",
    query: {
      course_id: route.query.course_id,
    }
  });
};
onMounted(() => {
  getJobLibraryData();
});
</script>

<style scoped lang="scss">
.job-library {
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
  .job-library-header {
    height: 40px;
  }
  .job-library-main {
    width: 100%;
    margin-top: 20px;
    .button-box {
      margin-left: 20px;
    }
  }
}
</style>