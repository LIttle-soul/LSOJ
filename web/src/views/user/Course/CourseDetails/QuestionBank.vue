<template>
  <div class="question-bank">
    <div class="question-bank-header">
      <div style="float: left">
        <el-input
          placeholder="请输入内容"
          size="small"
          v-model="page.text"
          class="input-with-select"
          @keydown.enter="search_all_data(page.text)"
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
            <el-button @click="search_all_data(page.text)">搜索</el-button>
          </template>
        </el-input>
      </div>
      <div style="float: right">
        <el-button type="success" @click="addHomeWork" v-show="page.user_identity">添加题目</el-button>
      </div>
    </div>
    <el-table :data="questionBank" border class="question-bank-main">
      <el-table-column prop="catalogue" label="目录" width="250" />
      <el-table-column prop="question_type" label="题型" width="100" />
      <el-table-column prop="facility_value" label="难易度" width="80" />
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
              v-show="page.user_identity"
            >
              <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
            </el-button>
            <el-button
              size="medium"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
              style="margin-left: 20px"
              v-show="page.user_identity"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
            <el-button
              type="success"
              round
              style="margin-left: 80px"
              @click="seeProblem(scope.row)"
            >
              查看
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
import { useRoute, useRouter } from "vue-router";
import { deleteProblem, getQuestionList, getUserPower } from "@/api/course";
import dayJS from "dayjs";

let router = useRouter();
let route = useRoute();

let search_text = ref("");
//模糊搜索题目
let search_all_data = (text: string) => {
  page.value.text = text || "";
  // getQuestionData();
};

let page = ref({
  course_id: route.params.course_id,
  text: "",
  user_identity: 1,
});
//题库虚拟数据
let questionBank = ref([
  {
    question_id: 1,
    catalogue: "下列算法的时间复杂度是() ",
    question_type: "单选题",
    facility_value: "易/中/难",
    creator: "烟雨",
    creator_time: "2021-12-16 12:00:00",
  },
]);
let question_types = ["单选题", "多选题", "填空题", "判断题", "简答题"];
//格式化题库数据
let formatQuestionData = (val: any) => {
  return val.map((res: any) => ({
    question_id: res.question_id,
    catalogue: res.question_description,
    question_type: question_types[res.question_type],
    facility_value: res.question_difficulty < 4 ? "易" : "中",
    creator: res.question_user,
    creator_time: dayJS(res.upload_time).format("YYYY-MM-DD"),
  }));
};
//获取题库数据
let getQuestionData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getQuestionList({
    course_id: Number(page.value.course_id),
    text: page.value.text,
  });
  console.log(back_data);
  if (back_data.status) {
    questionBank.value = formatQuestionData(back_data.message);
    loading.close();
  } else {
    loading.close();
  }
};
//添加题目
let addHomeWork = () => {
  console.log("添加题目");
  router.push({
    path: "/addhomework",
    query: {
      course_id: page.value.course_id,
    },
  });
};
let handleEditClick = (val: any) => {
  console.log("修改题目");
  router.push({
    path: "/addhomework",
    query: {
      course_id: page.value.course_id,
    },
  });
};
let handleDeleteClick = (val: any) => {
  console.log("删除题目");
  ElMessageBox.confirm("确定要删除这道题目吗？删除后无法恢复哦。", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      console.log(val.question_id);
      let back_data = await deleteProblem({
        question_id: val.question_id,
      });
      console.log(back_data);
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        getQuestionData();
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

//查看题目
let seeProblem = (val: any) => {
  router.push({
    path: "/dowork",
    query: {
      question_id: val.question_id,
    },
  });
};
let getPower = async () => {

let getPower=async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中",
    background: "rgba(0,0,0,7)"
  });
  let back_data = await getUserPower({
    course_id: Number(route.query.course_id)
  });
  console.log(back_data);
  if (back_data.status){
    page.value.user_identity = back_data.message;
    loading.close();
  }else{
    loading.close();
  }
}
}
//挂载
onMounted(() => {
  getQuestionData();
  getPower();
});
</script>

<style lang="scss" scoped>
.question-bank {
  max-width: 1100px;
  width: 1100px;
  margin: 10px auto;
  .question-bank-header {
    height: 40px;
  }
  .question-bank-main {
    width: 100%;
    margin-top: 20px;
  }
}
</style>
