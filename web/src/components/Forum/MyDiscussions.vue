<template>
  <div class="my-discussions">
    <el-card>
      <template #header>
        <div class="header">
          <div class="type">
            <i class="el-icon-folder"></i>  
            <el-select v-model="type" size="mini" placeholder="请选择" @change="change()">
              <el-option
                v-for="type in types"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              >
              </el-option>
            </el-select>
          </div>
          <div class="search">
            <search @search="search"></search>
          </div>
        </div>
      </template>
      <el-table :data="data" stripe style="width: 100%">
        <el-table-column width="400px" prop="title" label="标题" show-overflow-tooltip="true">
          <template #default="scope">
            <div>
              <a :href="'/forum/discussion/'+scope.row.discussion_id">
                <span v-html="scope.row.title"></span>
              </a>
            </div>
          </template>
        </el-table-column>
        <el-table-column width="200px" prop="time" label="创建时间"></el-table-column>
        
        <el-table-column
          align="right"
          min-width="180px"
          >
          <template #header>
            <p>功能</p>
          </template>
          <template #default="scope">
            <el-button
              v-if="type === 'discussion'"
              size="mini"
              @click="handleEdit(scope.$index, scope.row)">修改</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <div v-if="show" class="modify">
      <el-button @click="show=!show" class="close" icon="el-icon-close" circle></el-button>
      <modifyDiscussion :type="'modify'" :p_id="modifyDiscussion_id" :p_title="modifyDiscussion_title" :p_content="modifyDiscussion_content" @modifyDiscussion="modifyDiscussion"></modifyDiscussion>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import modifyDiscussion from "./AddDiscussion.vue";
import search from "./search.vue";

export default {
  components: {
    modifyDiscussion,
    search
  },
  created() {
    this.getMyDiscussions();
  },
  data() {
    return {
      types: [
        {
          label: "我的讨论",
          value: "discussion",
        },
        {
          label: "我的回复",
          value: "reply"
        }
      ],
      type: "discussion",
      data: [],
      show: false,
      t_data: [],
      modifyDiscussion_id: 0,
      modifyDiscussion_title: "",
      modifyDiscussion_content: ""
    };
  },
  methods: {
    // handleEdit(index, row) {
    //   console.log(index, row);
    // },
    // handleDelete(index, row) {
    //   console.log(index, row,row.discussion_id);
    // },

    change() {
      if (this.type === "discussion") {
        this.getMyDiscussions();
        console.log("discussion");
      }
      if (this.type === "reply") {
        this.getMyReplys();
        console.log("reply");
      }
    },
    getMyDiscussions() {
      this.data = [];
      this.$http({
        url: "/api/forum/getmyforum/",
        method: "get",
        params: {
          token: this.$cookies.get("token"),
          forum_status: 1,
          is_admin: 0,
        }
      })
        .then((response) => {
          console.log(response);
          for (let i of response.data.content) {
            let k = {
              title: i.forum_title,
              content: i.forum_content,
              time: i.create_time.slice(0, 10)+ " " +i.create_time.slice(11, 19),
              discussion_id: i.forum_id
            }
            this.t_data.push(k);
            this.data.push(k)
          }
          console.log(this.data)
        })
    },
    getMyReplys() {
      this.data = [];
      this.$http({
        url: "/api/forum/getmyreply/",
        method: "get",
        params: {
          token: this.$cookies.get("token"),
        }
      })
        .then((response) => {
          console.log(response);
          for (let i of response.data.content) {
            console.log(i.reply_status);
            if (i.reply_status === 1) {
              continue;
            }
            let k = {
              title: i.reply_content,
              time: i.create_time.slice(0, 10)+ " " +i.create_time.slice(11, 19),
              discussion_id: i.forum_id,
              reply_id: i.reply_id
            }
            this.t_data.push(k);
            this.data.push(k)
          }
          console.log(1)
        })
    },
    handleEdit(index, row) {
      if (this.type === "discussion") {
        this.getmodifyDiscussionContent(row.discussion_id, row.title, row.content);
        console.log("discussion");
      }
    },
    handleDelete(index, row) {
      if (this.type === "discussion") {
        this.deleteDiscussion(row.discussion_id, index);
        console.log("discussion");
      }
      if (this.type === "reply") {
        this.deleteReply(row.reply_id, index);
        console.log("reply");
      }
    },
    deleteDiscussion(discussion_id, index) {
      this.$http({
        url: "/api/forum/deleteforum/",
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
          forum_id: discussion_id
        }
      })
        .then((response) => {
          if (response.data.err !== undefined) {
            ElMessage(response.data.err);
            console.log(response.data.err);
          }
          else {
            ElMessage({
              type: "success",
              message: response.data.content
            });
            this.data.splice(index, 1);
            
          }
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
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
              this.data.splice(index, 1);
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
    modifyDiscussionContent(e) {
      this.show = e;
    },
    getmodifyDiscussionContent(discussion_id, title, content) {
      this.show = true;
      this.modifyDiscussion_id = discussion_id;
      this.modifyDiscussion_title = title;
      this.modifyDiscussion_content = content;
      console.log(this.p_title);
    },
    search(input) {
      // if (this.type === "discussion") {
        this.data = this.t_data.filter( value => {
          console.log(value.forum_title);
          return value.title.indexOf(input) !== -1;
        });
        console.log(this.discussions);
        console.log(input);
      // }
    }
  },
};
</script>

<style scoped>
  .my-discussions {
    width: 80%;
    margin: 4rem auto;
  }
  .my-discussions .header {
    display: flex;
    justify-content: space-between;
  }
  
  .my-discussions .t-col-1 {
    width: 50%;
  }
  .my-discussions .close {
    display: block;
    width: 40px;
    position: relative;
    transform-origin: center;
    top: 80px;
    left: 50%;
    margin-left: -20px;
  }
  .modify {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 100;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.5);
  }
  @media screen and (max-width: 600px) {

    .my-discussions .header {
      flex-direction: column;
    }
    .my-discussions .header .el-select {
      width: 100%;
    }
  }
</style>
