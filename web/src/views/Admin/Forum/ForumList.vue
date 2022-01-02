<template>
  <div class="forum-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          论坛管理
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
      </template>
      <div>
        <ForumTable :Data="Data" @deleteForum="getForumData" />
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
import { ElLoading } from "element-plus";
import { getForumList } from "@/api/forum";
import dayJS from "dayjs";
import ForumTable from "@/components/Forum/ForumTable.vue";

let page = ref({
  search_data: "",
  page: 1,
  page_size: 20,
  total: 30,
  sort_by: "time",
  forum_section: -1,
  section_id: 0,
  me: "",
});

let Data = ref([]);
let formatData = (val: any) => {
  return val.map((item: any) => ({
    forum_id: item.forum_id,
    forum_title: item.forum_title,
    forum_content: item.forum_content,
    forum_creator: item.forum_creator,
    user_nick: item.user_nick,
    forum_section: item.forum_section,
    section_id: item.section_id,
    forum_status: item.forum_status,
    create_time: dayJS(item.create_time).format("YYYY-MM-DD HH:mm:ss"),
    forum_top: item.forum_top,
  }));
};
let getForumData = async () => {
  const loadingInstance = ElLoading.service();
  let data = {
    page: page.value.page,
    total: page.value.page_size,
    forum_section: page.value.forum_section,
    section_id: page.value.section_id,
    text: page.value.search_data,
    sort_by: page.value.sort_by,
    me: page.value.me,
  };
  let forum = await getForumList(data);
  if (forum.status) {
    Data.value = formatData(forum.message);
    page.value.total = forum.total;
    loadingInstance.close();
  }
};
let search_all_data = (val: string) => {
  page.value.search_data = val;
  getForumData();
};
let handleCurrentChange = (val: number) => {
  page.value.page = val;
  getForumData();
};
let handleSizeChange = (val: number) => {
  page.value.total = val;
  getForumData();
};
onMounted(() => {
  getForumData();
});
</script>

<style>
.forum-list .el-card__header {
  height: 60px;
}
</style>

<style scoped lang="scss">
.forum-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
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
