<template>
  <div class="forum-list-child">
    <div class="forum-margin">
      <div class="forum-user">
        <el-avatar :size="40" :src="props.item.user_icon"></el-avatar>
        <div class="forum-user-child">
          <div class="forum-nick">{{ props.item.user_nick }}</div>
          <div class="forum-time">{{ props.item.create_time }}</div>
          <div class="top-font" v-if="props.item.forum_top">置顶</div>
        </div>
        <div class="manage-forum" v-show="props.admin">
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
                <el-dropdown-item @click="deleteTheForum" v-if="props.admin"
                  >删除</el-dropdown-item
                >
                <el-dropdown-item
                  @click="upTheForum"
                  v-if="!props.item.forum_top && props.admin"
                  >置顶</el-dropdown-item
                >
                <el-dropdown-item
                  @click="upTheForum"
                  v-if="props.item.forum_top && props.admin"
                  >取消置顶</el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      <div class="forum-contest" @click="getForumData()">
        <p class="forum-title">{{ props.item.forum_title }}</p>
        <p>{{ props.item.forum_content }}</p>
      </div>
      <div class="forum-footer">
        <el-icon :size="25" color="#d6d6d6"
          ><View style="width: 25px; height: 25px"
        /></el-icon>
        <div class="forum-footer-num">{{ props.item.forum_visits }}</div>
        <el-icon :size="25" color="#d6d6d6"
          ><chat-dot-round style="width: 25px; height: 25px"
        /></el-icon>
        <div class="forum-footer-num">{{ props.item.reply_num }}</div>
        <el-icon :size="100" color="#d6d6d6"
          ><svg
            style="width: 25px; height: 25px"
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            fill="currentColor"
            class="bi bi-hand-thumbs-up"
            viewBox="0 0 16 16"
          >
            <path
              d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"
            /></svg
        ></el-icon>
        <div class="forum-footer-num">{{ props.item.like_num }}</div>
        <el-icon :size="25" class="forum-icon"
          ><svg
            style="width: 25px; height: 25px; margin-left: 20px"
            t="1636104666077"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="3332"
            width="200"
            height="200"
          >
            <path
              d="M509.606998 143.114488c9.082866 0 17.327644 4.840238 20.996197 12.331863l97.262184 197.441814c5.613858 11.403724 16.663518 19.358907 29.438473 21.216207l223.738737 32.552393c8.420787 1.215688 15.604396 6.851035 18.23327 14.254655 2.520403 7.18361 0.595564 15.062044-5.084808 20.586874L730.253304 601.611947c-8.949836 8.751315-12.994965 21.171182-10.916631 33.370015l38.011732 222.060515c1.325182 7.737218-2.165316 15.426341-8.905834 19.978007-4.088108 2.741437-8.861832 4.155646-13.812587 4.155646-4.022617 0-7.999185-0.972141-11.425214-2.740414L528.149307 775.671215c-5.768377-3.006474-12.155854-4.552689-18.542308-4.552689-6.364965 0-12.727882 1.547239-18.518772 4.552689L296.254819 878.348736c-3.559059 1.855254-7.602142 2.828418-11.668761 2.828418-4.861728 0-9.723455-1.459235-13.546527-4.022617-6.961552-4.684696-10.475586-12.419867-9.127891-20.155039l38.011732-222.016513c2.078335-12.198833-1.988284-24.619724-10.939143-33.370015L125.02397 441.443038c-5.635347-5.492084-7.55814-13.348006-5.061272-20.453844 2.63092-7.481392 9.812483-13.116739 18.298761-14.332427l223.674269-32.552393c12.839423-1.857301 23.867594-9.813506 29.481452-21.216207l97.194646-197.396789C492.325403 147.965983 500.590648 143.114488 509.606998 143.114488M509.606998 104.904235c-24.043602 0-45.922912 13.226233-56.177464 33.95637L356.189863 336.302419l-223.674269 32.54216c-22.983457 3.304256-42.100864 18.718317-49.481971 39.659255-7.381108 21.048385-1.812275 44.23241 14.431687 60.033281l163.916257 160.125931-38.011732 222.016513c-3.868097 22.408359 6.03239 44.819788 25.458835 57.94676 10.69662 7.116071 23.204491 10.784624 35.757388 10.784624 10.298554 0 20.663622-2.475378 30.055526-7.337105l194.987926-102.7205L704.662463 912.072815c9.369392 4.861728 19.712971 7.337105 29.990035 7.337105 12.57541 0 25.082258-3.668553 35.778878-10.784624 19.426445-13.126972 29.305443-35.538401 25.460882-57.94676l-38.012755-222.016513 163.937746-160.125931c16.22145-15.812127 21.810748-38.984896 14.408151-60.033281-7.402597-20.940938-26.51898-36.353976-49.503461-39.659255L663.04767 336.302419l-97.240695-197.441814C555.619962 118.131491 533.695626 104.904235 509.606998 104.904235L509.606998 104.904235z"
              p-id="3333"
              fill="#d6d6d6"
            ></path></svg
        ></el-icon>
        <div class="forum-footer-num">{{ props.item.collect_num }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { View, ChatDotRound, ArrowDown } from "@element-plus/icons";
import { setForumData, deleteForum, upForum } from "@/api/forum";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  item: {
    type: undefined,
    default: {
      forum_id: 1,
      forum_title: "this forum!",
      forum_content: "this forum!",
      forum_creator: "",
      user_icon: "",
      user_nick: "炎偌明渊",
      forum_priority: 0,
      forum_section: 0,
      section_id: 0,
      forum_visits: 0,
      like_num: 0,
      reply_num: 0,
      collect_num: 0,
      create_time: "2020-01-01 08:00:00",
      forum_top: false,
    },
  },
});

let emits = defineEmits(["deleteForum", "upForum"]);

let router = useRouter();
let getForumData = () => {
  router.push({
    path: "/showforum",
    query: {
      forum_id: props.item.forum_id,
      forum_content: props.item.forum_content,
    },
  });
  setForum("see");
};
let setForum = async (val: string) => {
  let data = {
    key: val,
    forum_id: props.item.forum_id,
  };
  await setForumData(data);
};
let deleteTheForum = async () => {
  let data = {
    forum_id: props.item.forum_id,
  };
  let forum = await deleteForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    emits("deleteForum");
  } else {
    ElMessage.error(forum.message);
  }
};
let upTheForum = async () => {
  let data = {
    forum_id: props.item.forum_id,
  };
  let forum = await upForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    emits("upForum");
  } else {
    ElMessage.error(forum.message);
  }
};
let ellipsis = (value: string) => {
  if (!value) return "";
  if (value.length > 30) {
    return value.slice(0, 30) + "...";
  }
  return value;
};
</script>

<style scoped lang="scss">
.forum-list-child {
  border-right: 1px solid #d6d6d6;
  border-left: 1px solid #d6d6d6;
  border-bottom: 1px solid #d6d6d6;
  box-shadow: 0px 0px 20px #eeeeee;
  background: white;
  padding-top: 25px;
  .forum-margin {
    margin: 0px 40px 25px 40px;
    .forum-user {
      display: flex;
      position: relative;
      .forum-user-child {
        height: 40px;
        line-height: 40px;
        margin-left: 10px;
        display: flex;
        .forum-nick {
          color: #5f5e5e;
        }
        .forum-time {
          color: #b8b3b3;
          margin-left: 20px;
        }
        .top-font {
          color: pink;
          margin-left: 20px;
        }
      }
      .manage-forum {
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
    .forum-contest {
      font-size: 18px;
      overflow: hidden;
      word-break: break-all;
      word-wrap: break-word;
      .forum-title {
        font-size: 20px;
        font-weight: bold;
        margin: 25px 0;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
    .forum-contest:hover {
      color: #5d246b;
    }
    .forum-footer {
      height: 25px;
      transform: translate(70%);
      display: flex;
      margin-top: 40px;
      .forum-footer-num {
        color: #d6d6d6;
        height: 25px;
        font-size: 18px;
        width: 50px;
        line-height: 25px;
        margin-left: 10px;
      }
      .forum-icon {
        transform: translate(-20px);
        color: #ffffff;
      }
    }
  }
}
</style>
