<template>
  <div class="reply-list">
    <div class="reply-header">
      <el-avatar :size="40" :src="props.item.user_icon"></el-avatar>
      <div class="reply-child">
        <div class="reply-nick">{{ props.item.user_nick }}</div>
        <div class="reply-time">{{ props.item.create_time }}</div>
        <div class="top-font" v-if="props.item.reply_top">置顶</div>
      </div>
      <div class="manage-reply" v-show="props.admin || props.user || page.reply_user">
        <el-dropdown>
          <div class="manage-font">
            管理
            <el-icon>
              <arrow-down />
            </el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="false">举报</el-dropdown-item>
              <el-dropdown-item
                @click="deleteTheReply"
                v-if="props.admin || props.user || page.reply_user"
                >删除</el-dropdown-item
              >
              <el-dropdown-item
                @click="upTheReply"
                v-if="!props.item.reply_top && (props.admin || props.user)"
                >置顶</el-dropdown-item
              >
              <el-dropdown-item
                @click="upTheReply"
                v-if="props.item.reply_top && (props.admin || props.user)"
                >取消置顶</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    <div class="reply-contest">{{ item.reply_content }}</div>
    <div class="reply-footer">
      <div class="reply-footer-font">{{ item.reply_like }}</div>
      <el-button class="reply-like" @click="setForum('like')">
        <el-icon :size="30"
          ><svg
            style="width: 25px; height: 25px; margin-bottom: 10px"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-emoji-smile"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
            />
            <path
              d="M4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683zM7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5zm4 0c0 .828-.448 1.5-1 1.5s-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5z"
            /></svg
        ></el-icon>
      </el-button>
      <div class="reply-footer-font">|</div>
      <el-button class="reply-button" @mousedown="takeReplyShow"
        >回复</el-button
      >
    </div>
    <div class="forum-left-input" v-show="page.reply_show">
      <el-input
        v-model="page.reply_data"
        type="textarea"
        size="medium"
        minlength="1"
        maxlength="1000"
        placeholder="说你想说的!"
        :autosize="{ minRows: 3, maxRows: 8 }"
        resize="none"
        show-word-limit
        ref="mark"
      />
      <el-button type="success" class="input-button" @click="putReply"
        >回复</el-button
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from "vue";
import { ArrowDown } from "@element-plus/icons";
import { createReply, setForumData, deleteReply, upReply } from "@/api/forum";
import { ElMessage } from "element-plus";
import { useStore, mapState } from "vuex";

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  user: {
    type: Boolean,
    default: false,
  },
  item: {
    type: undefined,
    default: {
      forum_id: 0,
      reply_id: 0,
      reply_content: "0",
      reply_creator: 201910101600019,
      pre_reply: -1,
      reply_like: 0,
      create_time: "2020-01-01 08:00:00",
      reply_top: 0,
      user_icon: "",
      user_nick: "",
    },
  },
});
let emits = defineEmits(["putReply", "deleteReply"]);

let store = useStore();
const user_info = <any>(
  computed(mapState("user", ["user_info"]).user_info.bind({ $store: store }))
);
onMounted(() => {
  getUser();
});
let page = ref({
  reply_show: false,
  reply_data: "",
  reply_user: false,
  like: false,
});

let getUser = () => {
  if (props.item.reply_creator === user_info.value.user_id) {
    page.value.reply_user = true;
  }
};
let takeReplyShow = () => {
  page.value.reply_show = !page.value.reply_show;
};
let hideReplyInput = () => {
  page.value.reply_show = false;
};
let putReply = async () => {
  let data = {
    forum_id: props.item.forum_id,
    reply_id: props.item.reply_id,
    reply_content: page.value.reply_data,
  };
  let reply = await createReply(data);
  if (reply.status) {
    ElMessage({
      message: reply.message,
      type: "success",
    });
    page.value.reply_data = "";
    hideReplyInput();
    emits("putReply");
  } else {
    ElMessage.error(reply.message);
  }
};
let setForum = async (val: any) => {
  let data = {
    key: val,
    forum_id: "",
    reply_id: props.item.reply_id,
  };
  let forum = await setForumData(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    if (page.value.like) {
      page.value.like = false;
      props.item.reply_like -= 1;
    } else {
      page.value.like = true;
      props.item.reply_like += 1;
    }
  } else {
    ElMessage.error(forum.message);
  }
};
let deleteTheReply = async () => {
  let data = {
    reply_id: props.item.reply_id,
  };
  let reply = await deleteReply(data);
  if (reply.status) {
    ElMessage({
      message: reply.message,
      type: "success",
    });
    emits("deleteReply");
  } else {
    ElMessage.error(reply.message);
  }
};

let upTheReply = async () => {
  let data = {
    reply_id: props.item.reply_id,
  };
  let reply = await upReply(data);
  if (reply.status) {
    ElMessage({
      message: reply.message,
      type: "success",
    });
    emits("putReply");
  } else {
    ElMessage.error(reply.message);
  }
};
</script>

<style scoped lang="scss">
.reply-list {
  .reply-header {
    display: flex;
    height: 40px;
    line-height: 40px;
    width: 100%;
    position: relative;
    .reply-child {
      display: flex;
      .reply-nick {
        color: #5f5e5e;
        margin-left: 20px;
      }
      .reply-time {
        color: #b8b3b3;
        float: left;
        margin-left: 20px;
      }
      .top-font {
        color: pink;
        margin-left: 20px;
      }
    }
    .manage-reply {
      position: absolute;
      right: 20px;
      .manage-font {
        height: 40px;
        font-size: 16px;
        line-height: 40px;
        color: #b3b3b3;
      }
    }
  }
  .reply-contest {
    font-size: 18px;
    overflow: hidden;
    word-break: break-all;
    word-wrap: break-word;
    margin-top: 20px;
    margin-left: 55px;
  }
  .reply-footer {
    margin-top: 20px;
    height: 30px;
    width: 100%;
    .reply-footer-font {
      float: right;
      width: 30px;
      height: 30px;
      line-height: 30px;
      margin-left: 30px;
      margin-right: 10px;
    }
    .reply-like {
      height: 30px;
      float: right;
      border: 0px;
      padding: 0px;
      margin: 0px;
      background: none;
    }
    .reply-like:hover {
      color: #d86b6b;
      background: none;
    }
    .reply-like:focus {
      color: #d86b6b;
      background: none;
    }
    .reply-button {
      font-size: 18px;
      float: right;
      border: 0px;
      margin: 0px;
      padding: 0px;
      height: 30px;
      line-height: 30px;
      background: none;
    }
    .reply-button:hover {
      background: none;
    }
    .reply-button:focus {
      background: none;
    }
  }
  .forum-left-input {
    margin-left: 10px;
    margin-right: 10px;
    .input-button {
      margin-top: 20px;
      margin-left: 90%;
    }
  }
}
</style>
