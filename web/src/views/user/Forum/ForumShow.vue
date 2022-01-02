<template>
  <div class="forum-show">
    <div class="forum-left">
      <div class="forum-left-contest">
        <div class="forum-title">{{ page.forum_title }}</div>
        <div class="forum-header">
          <div class="forum-header-child">
            <el-icon :size="25" color="#cec9c8" class="header-icon"
              ><View style="width: 25px; height: 25px"
            /></el-icon>
            <div class="forum-footer-num" style="margin-left: 15px">
              {{ page.forum_visits }}
            </div>
          </div>
          <div class="forum-header-child">
            <el-icon :size="25" color="#cec9c8" class="header-icon"
              ><chat-dot-round style="width: 25px; height: 25px"
            /></el-icon>
            <div class="forum-footer-num" style="margin-left: 15px">
              {{ page.reply_num }}
            </div>
          </div>
          <div class="forum-header-child">
            <el-icon :size="25" color="#cec9c8" class="header-icon"
              ><svg
                style="width: 25px; height: 25px"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-hand-thumbs-up"
                viewBox="0 0 16 16"
              >
                <path
                  d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"
                /></svg
            ></el-icon>
            <div class="forum-footer-num" style="margin-left: 15px">
              {{ page.like_num }}
            </div>
          </div>
          <div class="forum-header-child">
            <el-icon :size="25" class="forum-icon"
              ><svg
                style="
                  width: 25px;
                  height: 25px;
                  margin-left: 20px;
                  margin-top: 10px;
                "
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
                  fill="#cec9c8"
                ></path></svg
            ></el-icon>
            <div class="forum-footer-num" style="margin-left: 35px">
              {{ page.collect_num }}
            </div>
          </div>
        </div>
        <div class="forum-contest">
          <ForumContest
            mode="preview"
            height="100%"
            :content="page.forum_content"
          />
        </div>
        <div class="forum-footer">
          <el-button class="forum-like" @click="setForum('like')">
            <el-icon :size="40" class="forum-icon2">
              <svg
                style="width: 30px; height: 30px; margin-top: -5px"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-hand-thumbs-up-fill"
                viewBox="0 0 16 16"
              >
                <path
                  d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"
                />
              </svg>
            </el-icon>
          </el-button>
          <div class="forum-footer-num2">{{ page.like_num }}</div>
          <el-button
            class="forum-star"
            @click="setForum('collect')"
            style="margin-left: 20%"
          >
            <el-icon :size="40" class="forum-icon2">
              <svg
                style="width: 30px; height: 30px; margin-top: -5px"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-star-fill"
                viewBox="0 0 16 16"
              >
                <path
                  d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
                />
              </svg>
            </el-icon>
          </el-button>
          <div class="forum-footer-num2">{{ page.collect_num }}</div>
        </div>
      </div>
      <div class="forum-left-input">
        <el-input
          v-model="page.reply_content"
          type="textarea"
          size="medium"
          minlength="1"
          maxlength="1000"
          placeholder="说你想说的!"
          :autosize="{ minRows: 3, maxRows: 8 }"
          resize="none"
          show-word-limit
        />
        <el-button type="success" class="input-button" @click="putReply"
          >回复</el-button
        >
      </div>
      <div class="forum-reply-header">
        <el-select
          v-model="page.sort_by"
          class="sort_by"
          placeholder="first_sort"
        >
          <el-option label="热门" value="like" @click="getReply()"></el-option>
          <el-option label="时间" value="time" @click="getReply()"></el-option>
        </el-select>
      </div>
      <div
        class="forum-left-reply"
        v-for="item in reply_data"
        :key="item.reply_id"
      >
        <ReplyList
          :item="item"
          :admin="page.admin"
          :user="page.user"
          @putReply="getReply"
          @deleteReply="getReply"
        />
        <div
          class="forum-reply-reply"
          v-for="it in item.reply_child"
          :key="it.reply_id"
        >
          <ReplyList
            :item="it"
            :admin="page.admin"
            :user="page.user"
            @putReply="getReply"
            @deleteReply="getReply"
          />
        </div>
      </div>
      <div class="forum-left-footer">
        <el-pagination
          v-model:currentPage="page.page"
          :page-sizes="[10, 20]"
          :page-size="page.page_size"
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
      <div class="forum-right-icon">
        <el-avatar :size="80" :src="page.user_icon"></el-avatar>
      </div>
      <div class="forum_user">{{ page.user_nick }}</div>
      <div class="forum_user">{{ page.create_time }}</div>
      <div class="forum-right-button">
        <el-button type="success" @click="putForum" v-if="page.user"
          >修改</el-button
        >
        <el-button
          type="danger"
          class="right-button"
          @click="confirmDelete"
          v-if="page.user || page.admin"
          >删除</el-button
        >
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { View, ChatDotRound } from "@element-plus/icons";
import { ElMessage, ElMessageBox, ElLoading } from "element-plus";
import dayJS from "dayjs";
import {
  createReply,
  setForumData,
  getReplyPage,
  deleteForum,
} from "@/api/forum";
import { useStore, mapState } from "vuex";
import { useRouter, useRoute } from "vue-router";
import { onMounted } from "@vue/runtime-core";

import ReplyList from "@/components/Forum/ReplyList.vue";
import ForumContest from "@/components/Editor/MarkdownEditor.vue";

let store = useStore();
let router = useRouter();
let route = useRoute();

const user_info = <any>(
  computed(mapState("user", ["user_info"]).user_info.bind({ $store: store }))
);

let page = ref({
  user: false,
  admin: false,
  page: 1,
  page_size: 20,
  total: 0,
  forum_id: 0,
  forum_title: "",
  forum_content: "",
  forum_creator: "",
  user_icon: "",
  user_nick: "",
  forum_section: 0,
  section_id: 0,
  forum_visits: 0,
  like_num: 0,
  reply_num: 0,
  collect_num: 0,
  create_time: "2020-01-01 08:00:00",
  reply_content: "",
  sort_by: "like",
  first_sort: "热门",
  like: false,
  collect: false,
});

let reply_data = ref(<any>[
  {
    forum_id: 0,
    reply_id: 0,
    reply_content: "0",
    reply_creator: 201910101600019,
    pre_reply: -1,
    reply_like: 0,
    create_time: "2020-01-01 08:00:00",
    reply_top: 0,
    reply_child: [
      {
        forum_id: 0,
        reply_id: 1,
        reply_content: "0",
        reply_creator: 201910101600019,
        pre_reply: 0,
        reply_like: 0,
        create_time: "2020-01-01 08:00:00",
        reply_top: 0,
      },
    ],
  },
]);

let setData = (val: any) => {
  page.value.forum_id = val.forum_id;
};
let getUser = () => {
  if (user_info.value && user_info.value.user_id == page.value.forum_creator) {
    page.value.user = true;
  }
  if (user_info.value && user_info.value.user_power <= 1) {
    page.value.admin = true;
  }
};
let formatData = (val: any) => {
  return val.map((item: any) => ({
    forum_id: item.forum_id,
    reply_id: item.reply_id,
    reply_content: item.reply_content,
    reply_creator: item.reply_creator,
    user_nick: item.user_nick,
    user_icon: "data:image/png;base64," + item.user_icon,
    pre_reply: item.pre_reply,
    reply_like: item.reply_like,
    create_time: dayJS(item.create_time).format("YYYY-MM-DD HH:mm:ss"),
    reply_top: item.reply_top,
    reply_child: item.reply_child.map((it: any) => ({
      forum_id: it.forum_id,
      reply_id: it.reply_id,
      reply_content: it.reply_content,
      reply_creator: it.reply_creator,
      user_nick: it.user_nick,
      user_icon: "data:image/png;base64," + it.user_icon,
      pre_reply: it.pre_reply,
      reply_like: it.reply_like,
      create_time: dayJS(it.create_time).format("YYYY-MM-DD HH:mm:ss"),
      reply_top: it.reply_top,
    })),
  }));
};
let putReply = async () => {
  let data = {
    forum_id: page.value.forum_id,
    reply_id: "-1",
    reply_content: page.value.reply_content,
  };
  let reply = await createReply(data);
  if (reply.status) {
    ElMessage({
      message: reply.message,
      type: "success",
    });
    page.value.reply_content = "";
    getReply();
  } else {
    ElMessage.error(reply.message);
  }
};
let getReply = async () => {
  const loadingInstance = ElLoading.service();
  let data = {
    page: page.value.page,
    total: page.value.page_size,
    forum_id: page.value.forum_id,
    sort_by: page.value.sort_by,
  };
  let reply = await getReplyPage(data);
  if (reply.status) {
    page.value.forum_title = reply.forum.forum_title;
    page.value.forum_content = reply.forum.forum_content;
    page.value.forum_visits = reply.forum.forum_visits;
    page.value.user_nick = reply.forum.user_nick;
    page.value.user_icon = "data:image/png;base64," + reply.forum.user_icon;
    page.value.forum_creator = reply.forum.forum_creator;
    page.value.like_num = reply.forum.like_num;
    page.value.reply_num = reply.forum.reply_num;
    page.value.collect_num = reply.forum.collect_num;
    reply_data.value = formatData(reply.reply);
    page.value.total = reply.reply_num;
    page.value.forum_section = reply.forum.forum_section;
    page.value.section_id = reply.forum.section_id;
    page.value.create_time = dayJS(reply.forum.create_time).format(
      "YYYY-MM-DD HH:mm:ss"
    );
    getUser();
    loadingInstance.close();
  }
};
let setForum = async (val: any) => {
  let data = {
    key: val,
    forum_id: page.value.forum_id,
    reply_id: "",
  };
  let forum = await setForumData(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    if(val === 'like') {
      if (page.value.like){
        page.value.like_num -= 1;
        page.value.like = false;
      }else{
        page.value.like_num += 1;
        page.value.like = true;
      }
    }else{
      if (page.value.collect){
        page.value.collect_num -= 1;
        page.value.collect = false;
      }else{
        page.value.collect_num += 1;
        page.value.collect = true;
      }
    }
  } else {
    ElMessage.error(forum.message);
  }
};
let handleCurrentChange = (val: number) => {
  page.value.page = val;
  getReply();
};
let handleSizeChange = (val: number) => {
  page.value.total = val;
  getReply();
};
let putForum = () => {
  router.push({
    path: "/createforum",
    query: {
      forum_id: page.value.forum_id,
      forum_section: page.value.forum_section,
      section_id: page.value.section_id,
      forum_title: page.value.forum_title,
      forum_content: page.value.forum_content,
    },
  });
};
let confirmDelete = () => {
  ElMessageBox.confirm(
    "点击确认后，该帖子将会被删除，一旦删除将不可被找回！请确认是否删除？",
    "删除确认",
    {
      confirmButtonText: "确认",
      cancelButtonText: "取消",
      type: "warning",
    }
  )
    .then(() => {
      deleteTheForum();
    })
    .catch(() => {});
};
let deleteTheForum = async () => {
  let data = {
    forum_id: page.value.forum_id,
  };
  let forum = await deleteForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    router.push({
      path: "/forum",
    });
  } else {
    ElMessage.error(forum.message);
  }
};
onMounted(() => {
  setData(route.query);
  getReply();
});
</script>

<style scoped lang="scss">
.forum-show {
  width: 85%;
  max-width: 1400px;
  margin: 70px auto;
  display: flex;
  .forum-left {
    width: 78%;
    .forum-left-contest {
      border: 1px solid #d6d6d6;
      box-shadow: 0px 0px 20px #d6d6d6;
      padding: 40px 50px;
      .forum-title {
        font-size: 30px;
        font-weight: bold;
      }
      .forum-header {
        background: #f7f8fc;
        height: 50px;
        display: flex;
        border-radius: 15px;
        margin-top: 40px;
        margin-bottom: 30px;
        .forum-header-child {
          display: flex;
          margin-left: 13%;
          .header-icon {
            transform: translateY(12px);
          }
          .forum-footer-num {
            color: #cec9c8;
            height: 50px;
            font-size: 18px;
            width: 50px;
            line-height: 50px;
            margin-left: 10px;
          }
        }
      }
      .forum-contest {
        font-size: 20px;
      }
      .forum-footer {
        margin-top: 50px;
        height: 40px;
        display: flex;
        .forum-like {
          border: 0px;
          background: #ffffff;
          margin-left: 30%;
        }
        .forum-like:hover {
          color: #d86b6b;
        }
        .forum-like:focus {
          color: #d86b6b;
        }
        .forum-footer-num2 {
          height: 40px;
          line-height: 40px;
          color: #cec9c8;
          font-size: 20px;
          margin-left: 10px;
          width: 50px;
        }
        .forum-star {
          border: 0px;
          background: #ffffff;
          margin-left: 30%;
        }
        .forum-star:hover {
          color: #fbff0f;
        }
        .forum-star:focus {
          color: #fbff0f;
        }
      }
    }
    .forum-left-input {
      border: 1px solid #d6d6d6;
      box-shadow: 0px 0px 20px #d6d6d6;
      padding: 40px 50px;
      margin-top: 20px;
      .input-button {
        margin-top: 20px;
        margin-left: 90.5%;
      }
    }
    .forum-reply-header {
      height: 40px;
      border: 1px solid #d6d6d6;
      box-shadow: 0px 0px 20px #d6d6d6;
      padding: 0px 50px;
      margin-top: 20px;
      position: relative;
      .sort_by {
        width: 100px;
        position: absolute;
        right: 50px;
      }
    }
    .forum-left-reply {
      border: 1px solid #d6d6d6;
      box-shadow: 0px 0px 20px #d6d6d6;
      padding: 40px 50px;
      .forum-reply-reply {
        margin-left: 50px;
        background: #c9e5ee;
        margin-top: 20px;
        padding: 10px 0px 10px 10px;
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
    width: 20%;
    height: 220px;
    border: 1px solid #d6d6d6;
    box-shadow: 0px 0px 20px #d6d6d6;
    margin-left: 10px;
    padding: 40px 50px;
    .forum-right-icon {
      width: 80px;
      margin: 0 auto;
    }
    .forum_user {
      text-align: center;
      margin-top: 10px;
    }
    .forum-right-button {
      margin-top: 30px;
      text-align: center;
      .right-button {
        margin-left: 30px;
      }
    }
  }
}
</style>
