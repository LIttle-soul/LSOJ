<template>
  <div class="forum-create">
    <div class="forum-header">
      <div class="header-font">发布帖子</div>
    </div>
    <div class="forum-body">
      <div class="forum-goal">
        <div class="body-font">模块:</div>
        <el-select v-model="page.forum_section" placeholder="section">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </div>
      <div class="forum-title">
        <div class="body-font">标题:</div>
        <el-input
          v-model="page.forum_title"
          maxlength="40"
          show-word-limit
          placeholder="This is title!"
        />
      </div>
      <div class="forum-contest">
        <div class="body-font">内容:</div>
        <ForumContest height="500px" v-model="page.forum_content" />
      </div>
      <el-button type="success" class="forum-button" @click="up_forum"
        >发布</el-button
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { createForum, putForum } from "@/api/forum";
import { useRouter, useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { onMounted } from "@vue/runtime-core";
import ForumContest from "@/components/Editor/MarkdownEditor.vue";

let page = ref({
  section: "总论坛",
  forum_section: 0,
  section_id: "",
  forum_id: 0,
  forum_title: "",
  forum_content: "",
});

let options = ref(<any>[
  {
    value: 0,
    label: "总论坛",
  },
  {
    value: 1,
    label: "问题",
  },
  {
    value: 2,
    label: "竞赛",
  },
  {
    value: 3,
    label: "课程",
  },
  {
    value: 4,
    label: "班级",
  },
]);

let router = useRouter();
const route = useRoute();
let setData = (val: any) => {
  page.value.forum_id = val.forum_id || 0;
  page.value.forum_section = val.forum_section || 0;
  page.value.section_id = val.section_id;
  page.value.forum_title = val.forum_title || "";
  page.value.forum_content = val.forum_content || "";
};
let up_forum = () => {
  console.log(page.value.forum_id);
  if (page.value.forum_id === 0) {
    console.log(1);
    create_forum();
  } else {
    console.log(2);
    put_forum();
  }
};
let create_forum = async () => {
  let data = {
    forum_section: page.value.forum_section,
    sections_id: page.value.section_id,
    forum_title: page.value.forum_title,
    forum_content: page.value.forum_content,
  };
  let forum = await createForum(data);
  if (forum.status) {
    page.value.forum_id = forum.forum_id;
    ElMessage({
      message: forum.message,
      type: "success",
    });
    router.push({
      path: "/showforum",
      query: {
        forum_id: forum.forum_id,
        forum_title: page.value.forum_title,
        forum_content: page.value.forum_content,
      },
    });
  } else {
    ElMessage.error(forum.message);
  }
};
let put_forum = async () => {
  let data = {
    forum_id: page.value.forum_id,
    forum_section: page.value.forum_section,
    sections_id: page.value.section_id,
    forum_title: page.value.forum_title,
    forum_content: page.value.forum_content,
  };
  let forum = await putForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    router.push({
      path: "/showforum",
      query: {
        forum_id: page.value.forum_id,
        forum_title: page.value.forum_title,
        forum_content: page.value.forum_content,
      },
    });
  } else {
    ElMessage.error(forum.message);
  }
};
onMounted(() => {
  setData(route.query);
});
</script>

<style scoped lang="scss">
.forum-create {
  width: 85%;
  max-width: 1400px;
  margin: 70px auto;
  border: 1px solid #d6d6d6;
  box-shadow: 0px 0px 20px #d6d6d6;
  .forum-header {
    height: 50px;
    font-size: 20px;
    font-weight: bold;
    border-bottom: 1px solid #d6d6d6;
    .header-font {
      margin-left: 30px;
      height: 50px;
      line-height: 50px;
    }
  }
  .forum-body {
    padding: 50px 60px 50px 50px;
    .forum-goal {
      display: flex;
      .body-font {
        height: 40px;
        width: 50px;
        line-height: 40px;
        margin-right: 60px;
        color: #d6d6d6;
      }
      .goal-select {
        margin-left: 20px;
      }
    }
    .forum-title {
      display: flex;
      margin-top: 50px;
      .body-font {
        height: 40px;
        width: 50px;
        line-height: 40px;
        margin-right: 60px;
        color: #d6d6d6;
      }
    }
    .forum-contest {
      display: flex;
      margin-top: 50px;
      .body-font {
        height: 40px;
        width: 50px;
        line-height: 40px;
        margin-right: 60px;
        color: #d6d6d6;
      }
    }
    .forum-button {
      width: 100px;
      margin-top: 30px;
      margin-left: 50%;
    }
  }
}
</style>
