<template>
  <div class="problem-list">
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
              <el-button @click="search_all_data('search', search_text)">搜索</el-button>
            </template>
          </el-input>
        </div>
      </template>
      <div>
        <ProblemList
          :Data="Data"
          :page="page"
          :admin="true"
          @filterProblemByDegree="filterProblemWithDegree"
          @handleSizeChange="sizeChange"
          @handleCurrentChange="currentChange"
          @reloadData="getData()"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watchEffect, watch } from "vue";
import { useStore, mapGetters, mapState } from "vuex";
import dayJS from "dayjs";
import { ElLoading } from "element-plus";
import { Collection } from "@element-plus/icons";

import ProblemList from "@/components/Problem/ProblemList.vue";

import { getProblemDataList } from "@/api/problem";

let search_text = ref("");

let store = useStore();
let Data = ref([]);
let page = ref({
  page: 1,
  total: 0,
  page_size: 50,
  key: "",
  text: "",
});

let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({
    $store: store,
  })
);

let search_all_data = (key: string, text: string) => {
  page.value.key = key || "";
  page.value.text = text || "";
  getData();
};
let filterProblemWithDegree = (val: any) => {
  page.value.key = val.sStatus.join(",") ? "difficult" : "";
  page.value.text = val.sStatus.join(",") || "";
  getData();
};
let sizeChange = (val: any) => {
  page.value.page_size = val;
  getData();
};
let currentChange = (val: any) => {
  page.value.page = val;
  getData();
};

watch(temp_search_data, (val) => {
  search_all_data("search", val);
});

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

let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getProblemDataList({
    page: page.value.page,
    total: page.value.page_size,
    key: page.value.key || "",
    text: page.value.text || "",
  });
  // console.log(back_data);
  if (back_data.status) {
    Data.value = formatData(back_data.message);
    page.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
  }
};

onMounted(() => {
  getData();
});
</script>

<style lang="scss">
.problem-list {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.problem-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
  .table-header {
    display: flex;
    justify-content: space-between;
    letter-spacing: 3px;
    height: 30px;
    min-width: 210px;
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
      margin-top: 5px;
    }
    @media screen and (max-width: 600px) {
      .input-with-select {
        display: none;
      }
    }
  }
}
@media screen and (max-width: 1000px) {
  .problem-list {
    width: 100%;
  }
}
</style>
