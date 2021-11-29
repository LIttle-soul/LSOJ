<template>
  <div class="contest-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><Notebook /></el-icon>
            竞赛列表
            <div class="current-time">当前时间:{{ current_time }}</div>
          </div>
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
      </template>
      <div>
        <ContestList
          :Data="Data"
          :page="page"
          :admin="true"
          @filterContestByType="filterContestByType"
          @handleSizeChange="sizeChange"
          @handleCurrentChange="currentChange"
          @reloadData="getContestData"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useStore, mapState } from "vuex";
import { Notebook } from "@element-plus/icons";
import dayJS from "dayjs";
import ContestList from "@/components/Contest/ContestList.vue";
import { ElLoading, ElMessage } from "element-plus";
import { getContestList } from "@/api/contest";
import { useRoute } from "vue-router";

let route = useRoute();

let store = useStore();

let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);

let temp_data = computed(
  mapState("contest", ["contest_list"]).contest_list.bind({ $store: store })
);

let search_text = ref("");
let page = ref({
  page: 1,
  page_size: 50,
  total: 0,
  status: "",
  text: "",
});

let Data = ref([
  {
    contest_id: 1,
    contest_title: "竞赛一",
    contest_time: "@已结束 2020-02-03 12:00:00",
    contest_type: 2,
    contest_creator: "Admin",
    contest_status: true,
  },
]);

let current_time = ref(dayJS().format("YYYY-MM-DD HH:mm:ss"));

let interval = setInterval(() => {
  current_time.value = dayJS().format("YYYY-MM-DD HH:mm:ss");
}, 1000);

onUnmounted(() => {
  clearInterval(interval);
});

let search_all_data = (val: string) => {
  page.value.text = val;
  getContestData();
};

watch(temp_search_data, (new_val: string) => {
  search_all_data(new_val);
});

let filterContestByType = (val: any) => {
  page.value.status = val.length > 0 ? val[0].toString() : "";
  console.log(page.value);
  getContestData();
};

let sizeChange = (val: number) => {
  page.value.page_size = val;
  getContestData();
};
let currentChange = (val: number) => {
  page.value.page = val;
  getContestData();
};

let formatData = (val: any) => {
  return val.map((item: any) => ({
    contest_id: item.contest_id,
    contest_title: item.contest_title,
    contest_time: dayJS(item.start_time).format("YYYY-MM-DD HH:mm:ss"),
    contest_type: item.contest_province,
    contest_creator: item.contest_creator,
    contest_status: item.contest_defunct,
  }));
};

let getContestData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中...",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getContestList({
    page: page.value.page,
    total: page.value.page_size,
    status: page.value.status || "",
    text: page.value.text || "",
    me: route.params.me || "",
    time: "",
  });
  // console.log(back_data);
  if (back_data.status) {
    Data.value = formatData(back_data.message);
    page.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};

onMounted(() => {
  getContestData();
});
</script>

<style lang="scss">
.contest-list {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.contest-list {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
  .table-header {
    display: flex;
    justify-content: space-between;
    font: 1.2em "楷体";
    letter-spacing: 3px;
    height: 30px;
    min-width: 210px;
    .header-left {
      font: 1.2em "楷体";
      letter-spacing: 3px;
      .icon {
        transform: translateY(5px);
      }
      .current-time {
        font-size: 10px;
        color: darkturquoise;
        letter-spacing: 1px;
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
  .contest-list {
    width: 100%;
  }
}
</style>
