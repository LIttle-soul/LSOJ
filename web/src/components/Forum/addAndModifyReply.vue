<template>
  <div class="add-reply">
    <el-button v-if="type!='modify'" type="text" class="button" @click="isShow()" icon="el-icon-chat-round">
      回复
    </el-button>
    <div v-else @click="isShow()">
      修改
    </div>
    <el-drawer v-if="drawer"
      :show-close="false"
      v-model="drawer"
      direction="btt"
      size="40%"
    >
        

        <!-- 预留 -->
        <template v-slot:title>
          <div>{{ nick }}</div>
          <el-button class="button" type="success" @click="commit()">{{ title }}</el-button>
        </template>

        <v-md-editor left-toolbar="" right-toolbar="" v-model="content" height="220px"></v-md-editor>
        <!-- <el-input
          type="textarea"
          :rows="2"
          placeholder="请输入内容"
          v-model="content"
        > 
        </el-input> -->
    </el-drawer>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'

export default {
  mounted() {
    this.getNick();
    this.getReplyContent();
  },
  props: {
    type: String,
    discussion_id: String,
    reply: Object,
    index: Number,
    p_nick: String
  },
  emits: [
    'addReply'
  ],
  data() {
    return {
      
      nick: "",
      content: "",
      drawer: false,
    }
  },
  computed: {
    title() {
      return this.type==="modify"? "修改" : "回复"; 
    }
  },
  methods: {
    isShow() {
      this.drawer = true
    },
    getReplyContent() {
      if (this.type === "modify") {
        this.content = this.reply.reply_content;
      }
    },
    getNick() {
      if (this.$cookies.get("token")) {
        this.$http({
          url: "/api/user/perfectinfo/",
          method: "get",
          params: {
            token: this.$cookies.get("token"),
          },
        })
          .then((response) => {
            this.nick = response.data.data.user_nick;
          })
      }
    },
    commit() {
      if (this.type === "modify") {
        this.modifyReply();
      }
      else {
        this.addReply();
      }
    },
    addReply() {
      console.log(this.reply)
      if (this.type === "reply") {
        this.content = `<a href="/showuserinfo">@${this.p_nick}</a> ${this.content}`
      }
      this.$http({
        url: "/api/forum/addreply/",
        method: "post",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        transformRequest: [
          function(data) {
            let ret = "";
            for (let it in data) {
              ret +=
                encodeURIComponent(it) +
                "=" +
                encodeURIComponent(data[it]) +
                "&";
            }
            return ret;
          },
        ],
        data: {
          token: this.$cookies.get("token"),
          forum_id: this.discussion_id,
          // reply_id: this.reply.pre_reply,
          reply_content: this.content
        }
      })
        .then((response) => {
          console.log(response);
          if (response.data.err !== undefined) {
            ElMessage(response.data.err);
            console.log(response.data.err);
          }
          this.drawer = false;
          let reply = response.data.reply[0];
          reply.nick = this.nick;
          this.$emit("addReply", response.data.reply[0])
        })
        .catch((error) => {
          console.log(error);
        });
    },
    modifyReply() {
      this.$http({
        url: "/api/forum/modifyreply/",
        method: "post",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        transformRequest: [
          function(data) {
            let ret = "";
            for (let it in data) {
              ret +=
                encodeURIComponent(it) +
                "=" +
                encodeURIComponent(data[it]) +
                "&";
            }
            return ret;
          },
        ],
        data: {
          token: this.$cookies.get("token"),
          reply_id: this.reply.reply_id,
          // reply_id: this.reply.pre_reply,
          content: this.content
        }
      })
        .then((response) => {
          console.log(response);
          if (response.data.err !== undefined) {
            ElMessage(response.data.err);
            console.log(response.data.err);
          }
          this.drawer = false;
          let reply = {};
          reply.index = this.index;
          reply.content = this.content;
          reply.nick = this.nick;
          this.$emit("modifyReply", reply)
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }
}
</script>

<style scoped>
  .add-reply header  {
    margin-bottom: 10px;
    height:10%
  }
  .add-reply .button {
    padding: 2px;
    width: auto;
    min-height: 20px;
  }
  .add-reply > .button {
    background-color: white;
    color: black;
  }
  .add-reply > .button:hover {
    color: rgb(144, 205, 247);
  }

  .add-reply .right {
    text-align: right;
  }

  .add-reply .el-drawer {
    overflow: auto;
  }
</style>