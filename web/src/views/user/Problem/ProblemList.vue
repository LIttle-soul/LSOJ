<template>
  <div class="problem-list">
    <div class="problem-left">
      <el-card>
        <template #header>
          <div class="table-header">
            <div class="header-left">
              <el-icon :size="25" class="icon"><Collection /></el-icon>问题列表
            </div>

            <el-input
              placeholder="请输入内容"
              size="small"
              v-model="search_text"
              class="input-with-select"
              @keydown.enter="search_all_data('search', search_text)"
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
                <el-button @click="search_all_data('search', search_text)"
                  >搜索</el-button
                >
              </template>
            </el-input>
          </div>
        </template>
        <div>
          <ProblemList
            :Data="Data"
            :page="page_info"
            @filterProblemByDegree="filterProblemWithDegree"
            @handleSizeChange="sizeChange"
            @handleCurrentChange="currentChange"
          />
        </div>
      </el-card>
    </div>
    <div class="problem-right">
      <ProblemNav
        title="问题标签"
        :card_data="page_info.tag_list"
        @filterData="search_all_data('search', $event)"
        class="problem_nav"
      />
      <ProblemNav
        title="问题来源"
        :card_data="page_info.course_list"
        @filterData="search_all_data('search', $event)"
        class="problem_nav"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watchEffect, watch } from "vue";
import { useStore, mapGetters, mapState } from "vuex";
import dayJS from "dayjs";
import { ElLoading } from "element-plus";
import { Collection } from "@element-plus/icons";

import ProblemList from "@/components/Problem/ProblemList.vue";
import ProblemNav from "@/components/Problem/ProblemNav.vue";

import { getProblemDataList, getProblemTagAndCourse } from "@/api/problem";

let search_text = ref("");

let store = useStore();
let Data = ref([]);
let page_info = ref({
  page: 1,
  total: 0,
  page_size: 50,
  key: "",
  text: "",
  tag_list: [],
  course_list: [],
});
let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({
    $store: store,
  })
);

let search_all_data = (key: string, text: string) => {
  console.log(key, text);
  page_info.value.key = key || "";
  page_info.value.text = text || "";
  getData();
};
let filterProblemWithDegree = (val: any) => {
  page_info.value.key = val.sStatus.join(",") ? "difficult" : "";
  page_info.value.text = val.sStatus.join(",") || "";
  getData();
};
let sizeChange = (val: any) => {
  page_info.value.page_size = val;
  getData();
};
let currentChange = (val: any) => {
  page_info.value.page = val;
  getData();
};

watch(temp_search_data, (val) => {
  search_all_data("search", val);
});

// 数据格式化
let formatData = (val: any) => {
  return val.map((item: any) => ({
    problem_id: item.problem_id,
    problem_title: item.problem_title,
    problem_degree: item.problem_difficult,
    problem_tag: (item.problem_tag || "").split(","),
    problem_solved: item.problem_solved,
    problem_submit: item.problem_submit,
    problem_status: item.problem_status,
    problem_source: item.problem_course,
    creation_time: dayJS(item.creation_time).format("YYYY-MM-DD HH:mm:ss"),
    submit_status: item.pass_status,
    problem_description: item.problem_description,
    time_limit: item.time_limit,
    memory_limit: item.memory_limit,
    centerDialogVisible: false,
  }));
};

// 获取问题数据
let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getProblemDataList({
    page: page_info.value.page,
    total: page_info.value.page_size,
    key: page_info.value.key || "",
    text: page_info.value.text || "",
  });
  // console.log(back_data);
  if (back_data.status) {
    Data.value = formatData(back_data.message);
    page_info.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
  }
};

// 获取问题标签数据
let getTagData = async () => {
  let back_data = await getProblemTagAndCourse();
  if (back_data.status) {
    page_info.value.tag_list = back_data.tag;
    page_info.value.course_list = back_data.course;
  }
};

onMounted(() => {
  getData();
  getTagData();
});
</script>

<style scoped lang="scss">
.problem-list {
  width: 85%;
  max-width: 1400px;
  margin: 70px auto;
  position: relative;
  display: flex;
  .problem-left {
    width: 80%;
    .table-header {
      display: flex;
      justify-content: space-between;
      .header-left {
        font: 1.2em "楷体";
        letter-spacing: 3px;
        .icon {
          transform: translateY(5px);
        }
      }
      .input-with-select {
        width: 230px;
        margin-right: 10px;
      }
      @media screen and (max-width: 600px) {
        .input-with-select {
          display: none;
        }
      }
    }
  }
  @media screen and (max-width: 800px) {
    .problem-left {
      width: 100%;
    }
  }
  .problem-right {
    width: 18%;
    float: left;
    margin-left: 2%;
    .problem-nav {
      margin-bottom: 60px;
    }
  }
  @media screen and (max-width: 800px) {
    .problem-right {
      display: none;
    }
  }
}

@media screen and (max-width: 1000px) {
  .problem-list {
    width: 100%;
  }
}
</style>
