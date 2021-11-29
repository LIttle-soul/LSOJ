<template>
  <div class="team-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><i class="bi bi-people"></i></el-icon>
            团队管理
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
        <TeamList
          :Data="Data"
          :is_delete_power="true"
          :page="page"
          @handleSizeChange="handleSizeChange"
          @handlePageChange="handlePageChange"
          @reload="getData"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import TeamList from "@/components/User/TeamList.vue";
import { useStore, mapState } from "vuex";
import { ref, computed, watch, onMounted } from "vue";
import { ElLoading, ElMessage } from "element-plus";
import dayJS from "dayjs";
import { getTeamList } from "@/api/user";

let store = useStore();
let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);
watch(temp_search_data, (new_val: string) => {
  console.log(new_val);
});
let search_text = ref("");

let Data = ref([]);
let page = ref({
  page: 1,
  page_size: 50,
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
    team_id: item.team_id,
    team_nick: item.team_nick,
    team_creator: item.team_creator,
    team_user_list: item.user_list,
    team_teacher: item.team_teacher,
    team_school: item.school_name,
    registration_time: dayJS(item.registration_time).format("YYYY-MM-DD HH:mm:ss"),
    team_introduce: item.team_introduce,
    invitation_code: item.invitation_code,
  }));
};

// 数据获取
let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getTeamList({
    page: page.value.page,
    total: page.value.page_size,
    text: page.value.text,
    mode: "join",
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

// 自动加载数据
onMounted(() => {
  getData();
});
</script>

<style lang="scss">
.team-list {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.team-list {
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
  .team-list {
    width: 100%;
  }
}
</style>
