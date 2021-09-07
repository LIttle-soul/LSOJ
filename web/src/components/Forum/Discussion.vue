<template>
  <div class="discussion">
    <div class="left">
      <!-- 讨论内容 -->
      <el-card class="discusscard">
        <!-- 导航条 -->
        <div class="header">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/forum' }">讨论区</el-breadcrumb-item>
          </el-breadcrumb>
          
        </div>
        <!-- 讨论内容 -->
        <div class="main">
          <div class="title">
            <h1>{{ discussion.forum_title }}</h1>
            <p>{{ discussion.creator_nick }} · {{ time }}</p>
          </div>
          <div class="content">
            <v-md-editor 
              v-model="discussion.forum_content" 
              mode='preview' 
              @copy-code-success="handleCopyCodeSuccess"
            >
            </v-md-editor>
            <!-- {{ discussion.forum_content }} -->
          </div>
        </div>
        <div class="footer">
          <addReply :type="'commit'" :discussion_id="discussion.forum_id" @addReply="addReply"></addReply>    
        </div>
      </el-card>
      <!-- 讨论回复 -->
      <div class="replys">
        <!-- 回复数量 -->
        <el-card class="count">
          <p>共 {{ replysLength }} 个回复</p>
        </el-card>
        <!-- 回复 -->
        <el-card class="reply" :key=reply v-for="reply, index in replys">
          <!-- 回复人以及发布时间 -->
          <div class="header">
            <table style="width:100%;">
              <tr>
                <td>
                  <h3>{{ reply.nick }}</h3>
                  <span style="">{{ reply.create_time.slice(0, 10)+ " " +reply.create_time.slice(11, 19)}}</span>
                </td>
                <td class="textAlignRight">
                  <el-dropdown v-if="showModify(reply.reply_creator)" :hide-on-click="false" trigger="click">
                    <span class="el-dropdown-link">
                      编辑<i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <!-- <el-dropdown-item>
                          <addReply :type="'modify'" :discussion_id="discussion.forum_id" :index="index" :reply="reply" @modifyReply="modifyReply"></addReply> 
                        </el-dropdown-item> -->
                        
                        <el-dropdown-item>
                          <div @click="deleteReply(reply.reply_id, index)">删除</div>
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
              mode='preview' 
              @copy-code-success="handleCopyCodeSuccess"
            >
            </v-md-editor>
          </div>
          <!-- 该回复的回复 -->
          <div class="footer">
            <addReply :type="'reply'" :p_nick="reply.nick" :discussion_id="discussion.forum_id" :reply="reply" @addReply="addReply"></addReply>
          </div>
        </el-card>
      </div>
      <!-- <replys></replys> -->
    </div>

    <!-- 相关次数 -->
    <!-- <el-card class="discusscardCount right">
      <table style="width:100%">
        <tr>
          <td class="textAlignLetf">收藏次数</td>
          <td class="textAlignRight ">
            <span class="textBackground">A</span>
          </td>
        </tr>
        <tr>
          <td class="textAlignLetf">参与人数</td>
          <td class="textAlignRight">
            <span class="textBackground">B</span>
          </td>
        </tr>
        <tr>
          <td class="textAlignLetf">浏览次数</td>
          <td class="textAlignRight">
            <span class="textBackground">C</span>
          </td>
        </tr>
      </table>
    </el-card> -->
  </div>
</template>

<script>
  
  import addReply from "./addAndModifyReply.vue"
  import { ElMessage } from 'element-plus'
  // import replys from './Replys.vue';

  export default {
    components: {
      addReply,
      // replys
    },
    data: function() {
      return {
        discussion: {},
        replys: [],
        drawer: false,
        user: -1
      }
    },
    created: function() {
      this.getDiscussion();
      this.getUser();
    },
    computed: {
      time() {
        return String(this.discussion.create_time).slice(0, 10);
      },
      replysLength() {
        return this.replys.length;
      }
    },
    methods: {
      getDiscussion() {
        this.$http({
          url: "/api/forum/getreplypage/",
          method: "get",
          params: {
            forum_id: this.$route.params.id
          }
        })
          .then((response) => {
            console.log(response);
            this.discussion = response.data.forum;
            this.replys = response.data.reply;
            console.log(this.replys)
            console.log(this.$route.params.id)
          })
          .catch((error) => {
            console.log(error);
          });
      },
      ShowaddReply() {
        this.drawer = true
      },
      addReply(reply) {
        this.replys.push(reply);
        console.log(this.replys);
      },
      modifyReply(reply) {
        this.replys[reply.index].content = reply.content;
      },
      deleteReply(reply_id, index) {
        this.$confirm('确定删除该评论吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
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
            }
          })
            .then((response) => {
              console.log(response);
              if (response.data.err !== undefined) {
                ElMessage(response.data.err);
                console.log(response.data.err);
              }
              else {
                this.replys.splice(index, 1);
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
              }
            })
            .catch((error) => {
              console.log(error);
            });
          
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      showModify(reply_creator) {
        // console.log(this.$cookies.user_id);
        if (this.user <= 1) {
          return true;
        }
        return this.$cookies.get("user_id") === reply_creator;
      },
      getUser() {
        if (!this.$cookies.get("token")) {
          return;
        }
        this.$http({
          url: "/api/user/getusertokeninfo/",
          method: "get",
          params: {
            token: this.$cookies.get("token"),
          },
        })
          .then((response) => {
            this.user = response.data.data.data.capacity;
            console.log(this.user);
          })
      }
    }
  };
</script>

<style scoped>
  .discussion {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 70%;
    margin: 0 auto;
    word-break: break-all;
  }
  .left {
    width: 100%;
  }
  .right {
    width: 25%;
  }
  
  
/* 讨论内容 */
  .discusscard {
    margin: 40px auto 10px;
  }

  .discusscard .header {
    border-bottom: 1px solid rgb(204, 204, 204);
    padding-bottom: 10px;
  }

  .discusscard .main {
    margin: 10px 0;
  }

  .discusscard .main .title h1 {
    font-size: 1.5rem;
    line-height: 1.5rem;
  }
  .discusscard .main .title p {
    font-size: 0.8rem;
  }

  .discusscard .footer {
    border-top: 1px solid rgb(204, 204, 204);
    padding-top: 10px;
  }

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
    padding: 0px
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

/* 相关次数 */
  .discusscardCount {
    margin: 40px auto 0;
  }
  .discusscardCount table {
    border-collapse: collapse;
  }
  .discussion table tr{
    line-height: 2.5rem;
  }


/* 其他 */

  .discussion .textAlignLetf {
    text-align: left;
  }
  .discussion .textAlignRight {
    text-align: right;
  }
  .discussion .textBackground {
    background: ghostwhite;
  }


  @media screen and (max-width: 600px) {
    .discussion {
      width: 100%;
    }
    .left {
      width: 100%;
    }
    .discusscardCount {
      display: none;
    }
  }
</style>