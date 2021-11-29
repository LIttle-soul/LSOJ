<template>
  <div class="user-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><i class="bi bi-person"></i></el-icon>
            用户管理
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
        <UserList
          :Data="Data"
          :page="page"
          @reloadData="getData"
          @handleSizeChange="handleSizeChange"
          @handlePageChange="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import UserList from "@/components/User/UserList.vue";
import { computed, watch, ref, onMounted } from "vue";
import { useStore, mapState } from "vuex";
import dayJS from "dayjs";
import { getUserList } from "@/api/user";
import { ElLoading, ElMessage } from "element-plus";

let store = useStore();

let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);
watch(temp_search_data, (new_val: string) => {
  search_all_data(new_val);
});

let search_text = ref("");

let Data = ref([
  {
    user_id: "201910101600040",
    user_nick: "nick_1",
    user_name: "name_1",
    user_school: "金华职业技术学院",
    user_power: 0,
    user_status: true,
    registration_time: "2020-02-03 12:00:00",
    centerDialogVisible: false,
  },
]);

let page = ref({
  page: 1,
  page_size: 20,
  total: 0,
  text: "",
});

// 事件处理函数
let search_all_data = (val: string) => {
  page.value.text = val;
  getData();
};

let handleSizeChange = (val: number) => {
  page.value.page_size = val;
  getData();
};

let handlePageChange = (val: number) => {
  page.value.page = val;
  getData();
};

// 数据格式化
let formatData = (val: any) => {
  return val.map((item: any) => ({
    user_id: item.user_id,
    user_nick: item.user_nick,
    user_name: item.user_name,
    user_school: item.school.school_name,
    user_power: item.user_power,
    user_status: item.user_status,
    registration_time: dayJS(item.user_registration_time).format("YYYY-MM-DD HH:mm:ss"),
    centerDialogVisible: false,
  }));
};

// 数据获取
let getData = async () => {
  let loading = ElLoading.service({
    text: "加载中....",
    background: "rgba(0,0,0,0.7)",
    lock: true,
  });
  let back_data = await getUserList({
    page: page.value.page,
    total: page.value.page_size,
    text: page.value.text || "",
    user_id: "",
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

// 挂载自动加载
onMounted(() => {
  getData();
});
</script>

<style lang="scss">
.user-list {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.user-list {
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
  .user-list {
    width: 100%;
  }
}
</style>
