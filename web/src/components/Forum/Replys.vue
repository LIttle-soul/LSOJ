<template>
  <div class="replys">
    <!-- 回复数量 -->
    <el-card class="count">
      <p>共 {{ replysLength }} 个回复</p>
    </el-card>
    <!-- 回复 -->
    <el-card class="reply" :key="reply" v-for="(reply, index) in replys">
      <!-- 回复人以及发布时间 -->
      <div class="header">
        <table style="width:100%;">
          <tr>
            <td>
              <h3>{{ reply.nick }}</h3>
              <span style="">{{
                reply.create_time.slice(0, 10) +
                  " " +
                  reply.create_time.slice(11, 19)
              }}</span>
            </td>
            <td class="textAlignRight">
              <el-dropdown :hide-on-click="false" trigger="click">
                <span class="el-dropdown-link">
                  编辑<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>
                      <addReply
                        :type="'modify'"
                        :discussion_id="discussion.forum_id"
                        :index="index"
                        :reply="reply"
                        @modifyReply="modifyReply"
                      ></addReply>
                    </el-dropdown-item>

                    <el-dropdown-item>
                      <div @click="deleteReply(reply.reply_id, index)">
                        删除
                      </div>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </td>
          </tr>
        </table>
      </div>
      <!-- 回复内容 -->
      <div class="main">
        <v-md-editor
          v-model="reply.reply_content"
          mode="preview"
          @copy-code-success="handleCopyCodeSuccess"
        >
        </v-md-editor>
      </div>
      <!-- 该回复的回复 -->
      <div class="footer">
        <addReply
          :type="'reply'"
          :discussion_id="discussion.forum_id"
          :reply="reply"
          @addReply="addReply"
        ></addReply>
      </div>
    </el-card>
  </div>
</template>

<script>
import addReply from "./addAndModifyReply.vue";
import { ElMessage } from "element-plus";

export default {
  components: {
    addReply,
  },
  props: {
    replys: Array,
  },
  data: function() {
    return {
      discussion: {},
      // replys: [],
    };
  },
  created: function() {},
  computed: {
    replysLength() {
      return this.replys.length;
    },
  },
  methods: {
    addReply(reply) {
      console.log(reply);
      // this.replys.push(reply);
      console.log(this.replys);
    },
    modifyReply(reply) {
      console.log(reply);
      // this.replys[reply.index].content = reply.content;
    },
    deleteReply(reply_id, index) {
      console.log(index);
      this.$confirm("确定删除该评论吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$http({
            url: "/api/forum/deletereply/",
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
              reply_id: reply_id,
            },
          })
            .then((response) => {
              console.log(response);
              if (response.data.err !== undefined) {
                ElMessage(response.data.err);
                console.log(response.data.err);
              } else {
                // this.$emit("deleteReplys", index);
                // this.replys.splice(index, 1);
                this.$message({
                  type: "success",
                  message: "删除成功!",
                });
              }
            })
            .catch((error) => {
              console.log(error);
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },
};
</script>

<style scoped>
/* 回复 */
.vuepress-markdown-body:not(.custom) {
  padding: 0.2rem 0.5rem;
}
.replys .count {
  line-height: 0;
  color: rgb(199, 199, 199);
  padding: 2px;
  margin-bottom: 2px;
}
.replys .reply {
  margin-top: 0px;
  padding: 0px;
}

.replys .reply .header h3 {
  line-height: 0;
  margin-top: 0;
}
.replys .reply .footer {
  border-top: 1px solid rgb(204, 204, 204);
  padding-top: 10px;
}

.replys .textAlignLetf {
  text-align: left;
}
</style>
