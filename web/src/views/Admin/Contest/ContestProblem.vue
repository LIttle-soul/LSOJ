<template>
  <div class="contest-problem">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><Notebook /></el-icon>
            竞赛问题
            <el-select
              size="small"
              :filterable="true"
              v-model="cur_contest"
              placeholder="请选择你要管理的竞赛"
              class="contest-choice"
              @change="setContestProblem(cur_contest)"
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
        <ContestProblemList
          :Data="Data"
          :page="page"
          :admin="true"
          @handleContestProblemUpClick="upButtonClick"
          @handleContestProblemDownClick="downButtonClick"
          @handleContestProblemDeleteClick="deleteButtonClick"
          @handleSizeChange="handleSizeChange"
          @handlePageChange="handlePageChange"
        />
      </div>
      <div class="bottom-button">
        <el-button type="primary" size="mini" @click="addProblemData">添加问题</el-button>
        <el-button type="success" size="mini" @click="submitProblem">提交</el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { mapGetters, mapState } from "vuex";
import {
  getContestList,
  getContestProblem,
  changeProblemList,
  deleteProblem,
  addProblem,
} from "@/api/contest";
import { ElLoading, ElMessageBox, ElMessage } from "element-plus";
import ContestProblemList from "@/components/Contest/ContestProblem.vue";
import { Notebook } from "@element-plus/icons";

let search_text = ref("");
let page = ref({
  page: 1,
  page_size: 50,
  total: 0,
  text: "",
});
let cur_contest = ref();
let contest_list = ref(<any>[]);
let problem_list = ref([]);
let Data = ref([]);
let search_all_data = (val: string) => {
  page.value.text = val;
  setContestProblem(cur_contest.value);
};
let handleSizeChange = (val: number) => {
  page.value.page_size = val;
  setContestProblem(cur_contest.value);
};
let handlePageChange = (val: number) => {
  page.value.page = val;
  setContestProblem(cur_contest.value);
};
let addProblemData = async () => {
  ElMessageBox.prompt("请输入你要添加的问题编号", "添加问题", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
  })
    .then(async ({ value }) => {
      console.log(value);
      let back_data = await addProblem({
        contest_id: cur_contest.value,
        problem_id: value,
      });
      if (back_data.status) {
        setContestProblem(cur_contest.value);
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
    })
    .catch(() => {
      console.log("取消输入");
    });
};
let submitProblem = async () => {
  let back_data = await changeProblemList({
    contest_id: cur_contest.value,
    problem_list: problem_list.value.join(","),
  });
  if (back_data.status) {
    setContestProblem(cur_contest.value);
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

// 位置交换
let upButtonClick = ({ index }: any) => {
  if (index === 0) {
    ElMessage({
      type: "error",
      message: "抱歉，这是第一个",
    });
  } else {
    [problem_list.value[index], problem_list.value[index - 1]] = [
      problem_list.value[index - 1],
      problem_list.value[index],
    ];
    [Data.value[index], Data.value[index - 1]] = [
      Data.value[index - 1],
      Data.value[index],
    ];
  }
};
let downButtonClick = ({ index }: any) => {
  if (index === Data.value.length - 1) {
    ElMessage({
      type: "error",
      message: "抱歉，这是最后一个",
    });
  } else {
    [problem_list.value[index], problem_list.value[index + 1]] = [
      problem_list.value[index + 1],
      problem_list.value[index],
    ];
    [Data.value[index], Data.value[index + 1]] = [
      Data.value[index + 1],
      Data.value[index],
    ];
  }
};

// 删除事件
let deleteButtonClick = async (row: any) => {
  let back_data = await deleteProblem({
    contest_id: cur_contest.value,
    problem_id: row.problem_id,
  });
  if (back_data.status) {
    setContestProblem(cur_contest.value);
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
let setContestProblem = async (val: any) => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    spinner: "el-icon-loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let back_data = await getContestProblem({
    page: page.value.page,
    total: page.value.page_size,
    contest_id: val,
    text: page.value.text || "",
  });
  // console.log(back_data);
  if (back_data.status) {
    Data.value = formatContestProblem(back_data.message);
    problem_list.value = back_data.message.map((item: any) => {
      return item.problem_id;
    });
    page.value.total = back_data.total;
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
let formatContestProblem = (val: any) => {
  return val.map((item: any) => ({
    problem_num: item.problem_num,
    problem_id: item.problem_id,
    problem_title: item.problem_title,
  }));
};
// 数据挂载自动加载
onMounted(() => {
  setContestList();
});
</script>

<style lang="scss">
.contest-problem {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>
<style scoped lang="scss">
.contest-problem {
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
    margin: 20px 40px;
    float: right;
  }
}
@media screen and (max-width: 1000px) {
  .contest-list {
    width: 100%;
  }
}
</style>
