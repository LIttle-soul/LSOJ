<template>
  <div class="contest-user">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><Notebook /></el-icon>
            竞赛用户
            <el-select
              size="small"
              :filterable="true"
              v-model="cur_contest"
              placeholder="请选择你要管理的竞赛"
              class="contest-choice"
              @change="setContestUser(cur_contest)"
            >
              <el-option
                v-for="item in contest_list"
                :key="item.contest_id"
                :label="item.contest_title"
                :value="item.contest_id"
              ></el-option>
            </el-select>
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
        <ContestUserList
          :Data="Data"
          :admin="true"
          :page="page"
          :contest_id="cur_contest"
          @success="setContestUser(cur_contest)"
          @handleSizeChange="handleSizeChange"
          @handlePageChange="handlePageChange"
        />
        <div class="bottom-button">
          <el-select v-model="select_data.label" size="small" style="width: 80px">
            <el-option label="用户" value="user"></el-option>
            <el-option label="班级" value="class"></el-option>
          </el-select>
          <el-select
            v-model="select_data.text"
            placeholder="请输入你要添加的班级和用户"
            :multiple="true"
            :filterable="true"
            :remote="true"
            :loading="select_data.loading"
            :remote-method="filterSearchData"
            size="small"
          >
            <el-option
              v-for="(item, index) in option"
              :key="index"
              :label="item.label"
              :value="item.value"
            >
              <span>{{ item.value }}</span
              ><span style="float: right">{{ item.label }}</span>
            </el-option>
          </el-select>
          <el-button type="primary" size="small" @click="addUser" class="bottom-adduser"
            >添加用户</el-button
          >
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { mapGetters, mapState } from "vuex";
import { getContestList, getContestUser, addContestUser } from "@/api/contest";
import { ElLoading, ElMessage } from "element-plus";
import dayJS from "dayjs";
import ContestUserList from "@/components/Contest/ContestUser.vue";
let search_text = ref("");
import { Notebook } from "@element-plus/icons";
import { getUserList } from "@/api/user";
let page = ref({
  page: 1,
  page_size: 50,
  total: 0,
  text: "",
});
let cur_contest = ref();
let contest_list = ref(<any>[]);
let Data = ref([]);
let search_all_data = (val: string) => {
  page.value.text = val;
  // getContestData();
};
let handleSizeChange = (val: number) => {
  page.value.page_size = val;
  // getContestData();
};
let handlePageChange = (val: number) => {
  page.value.page = val;
  // getContestData();
};

// 用户添加相关操作
let option = ref(<any>[]);
let select_data = ref({
  label: "user",
  text: [],
  loading: false,
});
let filterSearchData = async (val: string) => {
  if (val !== "") {
    if (select_data.value.label === "user") {
      let back_data = await getUserList({
        page: 1,
        total: 20,
        text: val,
        user_id: "",
      });
      console.log(back_data);
      if (back_data.status) {
        option.value = back_data.message.map((item: any) => ({
          label: item.user_name || item.user_nick || item.user_id,
          value: item.student_id || item.user_id,
        }));
        select_data.value.loading = false;
      } else {
        option.value = [];
        select_data.value.loading = false;
      }
    } else if (select_data.value.label === "class") {
      // let back_data = await getUserList({
      //   page: 1,
      //   total: 20,
      //   text: val,
      //   user_id: "",
      // });
      // console.log(back_data);
      // if (back_data.status) {
      //   option.value = [];
      //   select_data.value.loading = false;
      // } else {
      option.value = [];
      select_data.value.loading = false;
      // }
      ElMessage({
        type: "info",
        message: "此模块暂未完善",
      });
    } else {
      option.value = [];
      select_data.value.loading = false;
    }
  } else {
    option.value = [];
    select_data.value.loading = false;
  }
};
let addUser = async () => {
  let back_data = await addContestUser({
    contest_id: cur_contest.value,
    user_list: select_data.value.text,
  });
  if (back_data.status) {
    setContestUser(cur_contest.value);
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};

// 数据加载
let setContestList = async () => {
  let back_data = await getContestList({
    page: 1,
    total: 100,
    status: "",
    text: "",
    contest_id: "",
    me: "",
    time: "True",
  });
  if (back_data.status) {
    contest_list.value = formatContestList(back_data.message);
  }
};
let setContestUser = async (val: any) => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getContestUser({
    page: page.value.page,
    total: page.value.page_size,
    contest_id: val,
    text: page.value.text || "",
  });
  console.log(back_data);
  if (back_data.status) {
    Data.value = formatContestUser(back_data.message);
    page.value.total = back_data.total || 0;
    loading.close();
  } else {
    Data.value = [];
    loading.close();
  }
};

// 数据格式化
let formatContestList = (val: any) => {
  return val.map((item: any) => ({
    contest_id: item.contest_id,
    contest_title: item.contest_title,
  }));
};
let formatContestUser = (val: any) => {
  return val.map((item: any) => ({
    user_id: item.contest_user,
    user_name: item.user_name,
    user_school: item.user_school,
    student_id: item.student_id,
    apply_time: dayJS(item.apply_time).format("YYYY-MM-DD HH:mm:ss"),
    apply_status: item.contest_auditing,
  }));
};

// 数据挂载自动加载
onMounted(() => {
  setContestList();
});
</script>

<style lang="scss">
.contest-user {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.contest-user {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
  .table-header {
    display: flex;
    justify-content: space-between;
    min-width: 210px;
    .header-left {
      font: 1.2em "楷体";
      letter-spacing: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      .contest-choice {
        width: 180px;
        margin-left: 20px;
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
  .bottom-button {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    padding: 10px 0;
    .bottom-adduser {
      margin: 0 10px;
    }
  }
}
@media screen and (max-width: 1000px) {
  .contest-user {
    width: 100%;
  }
}
</style>
