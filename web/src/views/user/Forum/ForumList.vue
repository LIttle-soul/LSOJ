<template>
  <div class="forum-list">
    <div class="forum-left">
      <div class="forum-header">
        <div class="header-left">
          <el-icon :size="22"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
              />
              <path
                d="M4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683zM7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5zm4 0c0 .828-.448 1.5-1 1.5s-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5z"
              /></svg
          ></el-icon>
          讨论
        </div>
        <div>
          <el-select
            v-model="page.sort_by"
            class="sort_by"
            placeholder="first_sort"
          >
            <el-option
              label="热门"
              value="like"
              @click="getForumData"
            ></el-option>
            <el-option
              label="时间"
              value="time"
              @click="getForumData"
            ></el-option>
          </el-select>
        </div>
        <el-input
          placeholder="请输入内容"
          size="mini"
          v-model="page.text"
          class="input-with-select"
          @keydown.enter="search_all_data(page.text)"
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
            <el-button icon="el-icon-search" @click="search_all_data(page.text)"
              >搜索</el-button
            >
          </template>
        </el-input>
      </div>
      <div v-for="item in Data" :key="item.forum_id">
        <ForumList
          :item="item"
          :admin="page.admin"
          @deleteForum="getForumData"
          @upForum="getForumData"
        />
      </div>
      <div class="forum-left-footer">
        <el-pagination
          :currentPage="page.page"
          :page-size="page.page_size"
          :page-sizes="[10, 20]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="page.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="forum-left-pagination"
        >
        </el-pagination>
      </div>
    </div>
    <div class="forum-right">
      <el-button type="success" class="forum-create" @mousedown="create_forum"
        >创建帖子</el-button
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from "vue";
import { getForumList } from "@/api/forum";
import { ElLoading } from "element-plus";
import { useRouter } from "vue-router";
import { useStore, mapState } from "vuex";
import dayJS from "dayjs";

import ForumList from "@/components/Forum/ForumList.vue";

let store = useStore();
const user_info = <any>(
  computed(mapState("user", ["user_info"]).user_info.bind({ $store: store }))
);
let page = ref({
  sort_by: "like",
  first_sort: "热门",
  search_data: "",
  text: "",
  page: 1,
  total: 0,
  page_size: 20,
  forum_num: 0,
  forum_section: 0, // 版块类型
  section_id: 0, // 论坛版块比编号
  admin: false,
  me: "",
});
let router = useRouter();
let Data = ref(<any>[]);
let formatData = (val: any) => {
  return val.map((item: any) => ({
    forum_id: item.forum_id,
    forum_title: item.forum_title,
    forum_content: item.forum_content,
    forum_creator: item.forum_creator,
    user_icon: "data:image/png;base64," + item.user_icon,
    user_nick: item.user_nick,
    forum_section: item.forum_section,
    section_id: item.section_id,
    forum_visits: item.forum_visits,
    like_num: item.like_num,
    reply_num: item.reply_num,
    collect_num: item.collect_num,
    create_time: dayJS(item.create_time).format("YYYY-MM-DD HH:mm:ss"),
    forum_top: item.forum_top,
  }));
};
let getUserPower = () => {
  if (user_info.value && user_info.value.user_power <= 1) {
    page.value.admin = true;
  }
};
let getForumData = async () => {
  const loadingInstance = ElLoading.service({
    lock: true,
    background: "rgba(0,0,0,0.6)",
    text: "加载中....",
  });
  let data = {
    page: page.value.page,
    total: page.value.page_size,
    forum_section: page.value.forum_section,
    section_id: page.value.section_id,
    text: page.value.text,
    sort_by: page.value.sort_by,
    me: page.value.me,
  };
  let forum = await getForumList(data);
  if (forum.status) {
    Data.value = formatData(forum.message);
    page.value.total = forum.total || 0;
    loadingInstance.close();
  } else {
    loadingInstance.close();
  }
};
let search_all_data = (val: string) => {
  page.value.text = val;
  getForumData();
};
let create_forum = () => {
  router.push("/createforum");
};
let handleCurrentChange = (val: number) => {
  page.value.page = val;
  getForumData();
};
let handleSizeChange = (val: number) => {
  page.value.page_size = val;
  getForumData();
};
onMounted(() => {
  getForumData();
  getUserPower();
});
</script>

<style scoped lang="scss">
.forum-list {
  width: 85%;
  max-width: 1400px;
  margin: 70px auto;
  position: relative;
  display: flex;
  .forum-left {
    width: 80%;
    float: left;
    .forum-header {
      height: 60px;
      box-shadow: 0px 0px 20px #d6d6d6;
      font: 1.2em "楷体";
      letter-spacing: 3px;
      border: 1px solid #d6d6d6;
      display: flex;
      position: relative;
      .header-left {
        width: 100px;
        height: 60px;
        line-height: 60px;
        float: left;
        margin-left: 30px;
        margin-right: 0;
      }
      .sort_by {
        margin-top: 10px;
        width: 80px;
        position: absolute;
        right: 300px;
      }
      .input-with-select {
        width: 230px;
        height: 28px;
        float: left;
        margin-top: 16px;
        position: absolute;
        right: 50px;
      }
    }
    .forum-left-footer {
      border: 1px solid #d6d6d6;
      box-shadow: 0px 0px 20px #d6d6d6;
      .forum-left-pagination {
        margin-left: 25%;
      }
    }
  }
  .forum-right {
    width: 18%;
    height: 150px;
    float: left;
    margin-left: 1.5%;
    text-align: center;
    border-radius: 5px;
    border: 1px solid #dddddd;
    box-shadow: 0px 0px 20px #f1f1f1;
    .forum-create {
      margin-top: 60px;
      box-shadow: 2px 2px 10px #b5f0a3;
    }
  }
}
</style>
