<template>
  <div class="forum-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="table-header">
            <i class="el-icon-notebook-2"></i>
            敏感词管理
          </div>
          <el-input
            placeholder="请输入内容"
            size="mini"
            v-model="page.search_data"
            class="input-with-select"
            @keydown.enter="search_all_data(page.search_data)"
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
              <el-button
                icon="el-icon-search"
                @click="search_all_data(page.search_data)"
                >搜索</el-button
              >
            </template>
          </el-input>
        </div>
      </template>
      <div>
        <WordTable :Data="Data" @deleteWord="getWordData" />
      </div>
      <div class="add-word">
        <el-input
          placeholder="请输入内容"
          size="mini"
          v-model="page.new_word"
          class="input-up-word"
        >
          <template #append>
            <el-button @click="upWordData(page.new_word)">添加</el-button>
          </template>
        </el-input>
      </div>
      <div>
        <el-pagination
          v-model:currentPage="page.page"
          :page-sizes="[30, 50]"
          :page-size="page.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="page.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="forum-left-pagination"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { ElLoading, ElMessage } from "element-plus";
import { getWord, upWord } from "@/api/forum";

import WordTable from "@/components/Forum/WordTable.vue";

let page = ref({
  search_data: "",
  page: 1,
  page_size: 20,
  total: 30,
  new_word: "",
});

let Data = ref([]);

let getWordData = async () => {
  const loadingInstance = ElLoading.service();
  let data = {
    page: page.value.page,
    total: page.value.page_size,
    text: page.value.search_data,
  };
  let word = await getWord(data);
  if (word.status) {
    Data.value = word.message;
    page.value.total = word.total;
    loadingInstance.close();
  } else {
    ElMessage.error(word.message);
    loadingInstance.close();
  }
};
let upWordData = async (val: any) => {
  let data = {
    text: val,
  };
  let word = await upWord(data);
  if (word.status) {
    page.value.new_word = "";
    ElMessage({
      message: word.message,
      type: "success",
    });
    getWordData();
  } else {
    ElMessage.error(word.message);
  }
};
let search_all_data = (val: string) => {
  page.value.search_data = val;
  getWordData();
};
let handleCurrentChange = (val: number) => {
  page.value.page = val;
  getWordData();
};
let handleSizeChange = (val: number) => {
  page.value.total = val;
  getWordData();
};
onMounted(() => {
  getWordData();
});
</script>

<style scoped lang="scss">
.forum-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
  .card-header {
    height: 30px;
    .table-header {
      font: 1.2em "楷体";
      letter-spacing: 3px;
      height: 30px;
      width: 50%;
      min-width: 210px;
      float: left;
    }
    .input-with-select {
      width: 205px;
      float: right;
      margin-right: 10px;
      transform: translateY(-1px);
    }
    @media screen and (max-width: 600px) {
      .input-with-select {
        display: none;
      }
    }
  }
  .add-word {
    margin-top: 10px;
    position: relative;
    .input-up-word {
      width: 205px;
      position: absolute;
      right: 50px;
    }
  }
  .forum-left-pagination {
    margin-left: 25%;
  }
}
@media screen and (max-width: 1000px) {
  .forum-list {
    width: 100%;
  }
}
</style>
