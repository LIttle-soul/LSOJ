<template>
  <div class="college-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><i class="bi bi-building"></i></el-icon>
            学院管理
            <el-select
              v-model="page.school"
              :multiple="false"
              :filterable="true"
              :remote="true"
              :reserve-keyword="true"
              placeholder="请输入你的学校"
              :remote-method="remoteSchool"
              @change="getData"
            >
              <el-option
                v-for="item in school_list.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
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
        <CollegeList
          :admin="true"
          :Data="Data"
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
import CollegeList from "@/components/School/CollegeList.vue";
import { useStore, mapState } from "vuex";
import { ref, computed, watch, onMounted } from "vue";
import { ElLoading, ElMessage } from "element-plus";
import { getCollegeList, getSchoolList } from "@/api/school";
import { getAddressList } from "@/api/address";

let store = useStore();
let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);
watch(temp_search_data, (new_val: string) => {
  console.log(new_val);
});
let search_text = ref("");
let Data = ref([
  {
    college_id: "4265051060",
    college_name: "新疆工业职业技术学院",
    college_school: "金华职业技术学院",
  },
  {
    college_id: "4262051378",
    college_name: "甘肃财贸职业学院",
    college_school: "金华职业技术学院",
  },
]);
let page = ref({
  page: 1,
  page_size: 50,
  total: 0,
  text: "",
  school: [],
});

// 懒加载数据请求
let school_list = ref({
  options: <any>[],
  loading: false,
});
let remoteSchool = async (val: string) => {
  if (val !== "") {
    school_list.value.loading = true;
    let back_data = await getSchoolList({
      page: 1,
      total: 10,
      text: val || "",
      municipality_id: "",
      school_id: "",
    });
    if (back_data.status) {
      school_list.value.options = back_data.message.map((item: any) => ({
        label: item.school_name,
        value: item.school_id,
      }));
    } else {
      school_list.value.options = [];
    }
  } else {
    school_list.value.options = [];
  }
};

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
    college_id: item.college_id,
    college_name: item.college_name,
    college_school: item.college_school?.school_name || "",
  }));
};

// 数据获取
let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getCollegeList({
    page: page.value.page,
    total: page.value.page_size,
    text: page.value.text || "",
    school_id: page.value.school || "",
    college_id: "",
  });
  console.log(back_data);
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
</script>

<style lang="scss">
.college-list {
  .el-card__header {
    height: 60px;
    padding: 10px;
  }
}
</style>

<style scoped lang="scss">
.college-list {
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
  .college-list {
    width: 100%;
  }
}
</style>
