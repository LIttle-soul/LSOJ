<template>
  <div class="course">
    <div class="header">
      <div class="nav">
        <div class="left">推荐课程</div>
        <div class="right">
          <el-button
            type="info"
            size="mini"
            @click="
              () => {
                page.type = 'recommend';
                getData('recommend');
              }
            "
            >热门</el-button
          >
          <el-button
            type="info"
            size="mini"
            @click="
              () => {
                page.type = 'time';
                getData('recommend');
              }
            "
            >最新</el-button
          >
          <el-button
            type="info"
            size="mini"
            @click="
              () => {
                page.type = 'like';
                getData('recommend');
              }
            "
            >好评</el-button
          >
        </div>
      </div>
      <div class="main">
        <CourseCard :Data="Data" />
      </div>
    </div>
    <div class="content">
      <div class="nav">
        <div class="left">
          全部课程
          <el-select
            size="mini"
            v-model="page.subject"
            class="select"
            @change="getData('all')"
          >
            <el-option
              v-for="(item, index) in page.subject_options"
              :key="index"
              :value="item"
              :label="item"
            ></el-option>
          </el-select>
        </div>
        <div class="right">
          <el-input
            v-model="page.value"
            size="mini"
            placeholder="在此输入搜索内容"
            input-style="width: 130px;"
            class="right-input"
            @keydown.enter="getData('all')"
          >
            <template #prepend>
              <el-select v-model="page.status">
                <el-option
                  v-for="(item, index) in page.status_options"
                  :key="index"
                  :value="item.value"
                  :label="item.label"
                ></el-option>
              </el-select>
            </template>
          </el-input>
        </div>
      </div>
      <div class="main">
        <CourseCard :Data="allData" />
        <el-pagination
          background
          layout="prev, pager, next"
          :total="page.total"
          :page-size="page.page_size"
          :current-page="page.page"
          @current-change="handlePageChange"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { onMounted, ref } from "vue";
import CourseCard from "@/components/Course/CourseCard.vue";
import { ElLoading } from "element-plus";
import { getCourseList, getCourseTag } from "../../../api/course";

let Data = ref([
  {
    course_id: 1,
    src: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
    title: "法语入门",
    auther: "LiSoul",
    join: 100,
    status: "已结束",
  },
  {
    course_id: 1,
    src: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
    title: "法语入门",
    auther: "LiSoul",
    join: 100,
    status: "已结束",
  },
]);
let allData = ref([]);

let page = ref({
  page: 1,
  page_size: 50,
  total: 0,
  value: "",
  type: "",
  subject: "",
  status: "all",
  subject_options: [],
  status_options: [
    { value: "all", label: "全部" },
    { value: "not_started", label: "即将开始" },
    { value: "started", label: "正在进行" },
    { value: "end", label: "已结束" },
  ],
});
let handlePageChange = (val: number) => {
  page.value.page = val;
  getData("all");
};
let course_status = ["未激活", "公开", "私有", "收费", "结课"];
let formatData = (val: any) => {
  return val.map((item: any) => ({
    course_id: item.course_id,
    title: item.course_name,
    src: item.course_cover,
    auther: item.course_creator,
    join: item.course_peoples,
    status: course_status[item.course_status],
  }));
};

let getData = async (val: string) => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getCourseList({
    page: page.value.page,
    total: val === "recommend" ? 12 : page.value.page_size,
    sort_by: val === "recommend" ? page.value.type : "",
    key: page.value.status,
    text: page.value.value || "",
    subject: page.value.subject || "",
  });
  // console.log(back_data);
  if (back_data.status) {
    if (val === "all") {
      allData.value = formatData(back_data.message);
      page.value.total = back_data.total;
    } else if (val === "recommend") {
      Data.value = formatData(back_data.message);
    }
    loading.close();
  } else {
    loading.close();
  }
};
let getDataTag = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseTag();
  console.log(back_data);
  if (back_data.status) {
    page.value.subject_options = back_data.tag;
    loading.close();
  } else {
    loading.close();
  }
};
onMounted(() => {
  getData("all");
  getData("recommend");
  getDataTag();
});
</script>

<style lang="scss">
.course {
  width: 80%;
  margin: 20px auto;
  .header {
    width: 100%;
    min-height: 200px;
    .nav {
      display: flex;
      justify-content: space-between;
      height: 40px;
      .left {
        text-align: left;
        font-size: 30px;
        font-family: "STKaiti";
        height: 40px;
        line-height: 40px;
        font-weight: bolder;
      }
      .right {
        height: 40px;
        padding: 6px 10px;
      }
    }
  }
  .content {
    width: 100%;
    min-height: 600px;
    .nav {
      display: flex;
      justify-content: space-between;
      height: 40px;
      .left {
        text-align: left;
        font-size: 30px;
        font-family: "STKaiti";
        display: flex;
        height: 40px;
        line-height: 28px;
        padding: 6px 10px;
        font-weight: bolder;
        .select {
          width: 100px;
          margin-left: 10px;
        }
      }
      .right {
        height: 40px;
        padding: 6px 10px;
        .right-input {
          .el-input__inner {
            width: 80px;
          }
        }
      }
    }
  }
}
</style>
