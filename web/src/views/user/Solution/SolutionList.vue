<template>
  <div class="solution-list">
    <el-card shadow="always">
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon><wind-power /></el-icon>
            提交列表
            <span
              ><el-switch v-model="reload_status" active-text="实时更新"> </el-switch
            ></span>
          </div>
          <el-input
            placeholder="请输入内容"
            size="small"
            v-model="search_data"
            class="input-with-select"
            @keydown.enter="search_all_data(search_select, search_data)"
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
            <template #prepend>
              <el-select v-model="search_select" placeholder="请选择">
                <el-option label="提交" value="solution_id"></el-option>
                <el-option label="用户" value="user"></el-option>
                <el-option label="题目" value="problem_id"></el-option>
              </el-select>
            </template>
            <template #append>
              <el-button @click="search_all_data(search_select, search_data)"
                >搜索</el-button
              >
            </template>
          </el-input>
        </div>
      </template>
      <div>
        <RankList
          :Data="Data"
          :page="page_data"
          @filterSolutionList="filterSolutionList"
          @handleCurrentChange="pageChange"
          @handleSizeChange="pageSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import {
  computed,
  onUnmounted,
  reactive,
  watch,
  ref,
  onMounted,
} from "@vue/runtime-core";
import { useStore, mapGetters, mapState } from "vuex";
import { useRoute } from "vue-router";
import dayJS from "dayjs";
import { getSolutionDataList } from "@/api/solution";
import { WindPower } from "@element-plus/icons";

import RankList from "@/components/Solution/SolutionList.vue";
import { ElLoading, ElMessage } from "element-plus";

let store = useStore();
let route = useRoute();

let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);
let user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);
let temp_data = computed(
  mapState("solution", ["solution_data"]).solution_data.bind({ $store: store })
);

watch(
  () => temp_search_data.value,
  (val: string) => {
    console.log(val);
  }
);

let page_data = ref({
  page: 1,
  page_size: 50,
  total: 0,
  key: "",
  text: "",
  run_result: "",
  language: "",
  contest_id: -1,
  me: false,
});
let reload_status = ref(false);
let search_select = ref("problem_id");
let search_data = ref("");
let Data = ref([]);

let interval = setInterval(() => {
  // console.log(reload_status.value);
  if (reload_status.value) {
    getData();
  }
}, 10000);
onUnmounted(() => {
  clearInterval(interval);
});

let search_all_data = (label: string, value: string) => {
  page_data.value.key = label;
  page_data.value.text = value;
  // console.log(label, value);
  getData();
};
let filterSolutionList = (value: any) => {
  if (value.result) {
    page_data.value.run_result = value.result.length > 0 ? value.result[0] : "";
  } else if (value.language) {
    page_data.value.language = value.language.length > 0 ? value.language[0] : "";
  } else {
    page_data.value.run_result = "";
    page_data.value.language = "";
  }
  // console.log(page_data.value);
  getData();
};
let pageChange = (val: number) => {
  // console.log(val);
  page_data.value.page = val;
  getData();
};
let pageSizeChange = (val: number) => {
  // console.log(val);
  page_data.value.page_size = val;
  getData();
};

let formatData = (val: any) => {
  // console.log(val);
  return val.map((item: any) => ({
    solution_id: item.solution_id,
    user_id: item.user_id,
    problem_id: item.problem_id,
    solution_result: item.run_result,
    solution_memory: item.run_memory,
    solution_consuming: item.run_time,
    solution_language: item.solution_language,
    solution_length: item.code_length,
    solution_time: dayJS(item.solution_time).format("YYYY-MM-DD HH:mm:ss"),
  }));
};

let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getSolutionDataList({
    page: page_data.value.page,
    total: page_data.value.page_size,
    key: page_data.value.key || "",
    text: page_data.value.text || "",
    run_result: page_data.value.run_result.toString() || "",
    language: page_data.value.language.toString() || "",
    contest_id: page_data.value.contest_id || -1,
    me: page_data.value.me || false,
  });
  // console.log(back_data);
  if (back_data.status) {
    Data.value = formatData(back_data.message);
    page_data.value.total = back_data.total;
    loading.close();
  } else {
    ElMessage({
      type: "error",
      message: "数据请求失败，请稍后重试",
    });
    loading.close();
  }
};

onMounted(() => {
  // console.log(route.params, user_info.value.user_id);
  page_data.value.me = route.params.user_id
    ? route.params.user_id == user_info.value?.user_id
    : false;
  page_data.value.key = "problem_id";
  page_data.value.text = <string>route.params.problem_id || "";
  // console.log(page_data.value);
  getData();
});
</script>

<style lang="scss">
.solution-list {
  .table-header {
    .el-select {
      .el-input {
        width: 60px;
      }
      .el-input__inner {
        padding: 0 10px;
      }
      .el-input__suffix {
        /* background: black; */
        transform: translateY(-2px);
      }
    }
  }
}
</style>

<style scoped lang="scss">
.solution-list {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
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
      width: 280px;
      float: right;
      margin-right: 10px;
      transform: translateY(-1px);
      .el-input__inner {
        width: 40px;
      }
    }
    @media screen and (max-width: 600px) {
      .input-with-select {
        display: none;
      }
    }
  }
}
@media screen and (max-width: 1000px) {
  .solution-list {
    width: 100%;
  }
}
</style>
