<template>
<div class="discussions">

  <!-- 功能 -->
  
  <!-- 搜索 -->

  <!-- 添加 -->
  
  <!-- 管理 -->
  
  <!-- 删除 -->
  
  <!-- 讨论卡片 -->
  <div class="main">

    <el-card class="discussion" :key=discussion.forum_id v-for="discussion, key in currentDiscussions">
      <div :key="key" v-on:click="enterDiscussion(discussion.forum_id)">
        <div class="discussion-header">
          <h3 class="title">
            {{ discussion.forum_title }}
          </h3>
          <div>
            <el-button v-if="isShowAdministration()" class="button" @click.stop="deleteDiscussion(discussion.forum_id, key)" icon="el-icon-delete"></el-button>
          </div>
        </div>
        
        <div class="discussion-main">
          {{ discussion.forum_content }}
        </div>
        <div class="discussion-footer">
            <!-- <el-button type="text" class="button" icon="el-icon-view">浏览 A</el-button> -->
            <el-button type="text" class="button" icon="el-icon-chat-round">{{ discussion.reply_num }}</el-button>
        </div>
      </div>
    </el-card>
  </div>

  <el-pagination class="footer"
    background
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"   
    :page-count="pages"
    :page-size="pageSize"
    :pager-count="8"
    :current-page="page"
    layout="prev, pager, next"
    >
  </el-pagination>
</div>



</template>

<script>
  import { ElMessage } from 'element-plus'

  export default {
    props: {
      /**
       * discussions: 所有讨论数据
       */
      discussions: Array,
      userRight: Number
    },
    created: function() {
      // this.getDiscussions();
      // this.getUserTokenInfo();
      // console.log(this.discussions)
    },
    data: function() {
      return {
        /**
         * discussingCardLength: 当前板块的讨论卡片数量
         * page: 当前页（默认第1页）
         */
        // discussions: [],
        page: 1,
        pageSize: 20,
        search: false,
        input: '',
        // userRight: null
      }
    },
    computed: {
      /**
       * pages: 讨论分页的总页数
       * currentDiscussions: 当前页数据
       */

      pages: function() {
        return Math.ceil(this.discussions.length/this.pageSize);
      },
      currentDiscussions: function() {
        if (this.page*this.pageSize < this.discussions.length) {
          return this.discussions.slice((this.page-1)*this.pageSize, this.page*this.pageSize);
        }
        else {
          return this.discussions.slice((this.page-1)*this.pageSize);
        }
      },

    },
    methods: {
      /**
       * getDiscussions: 获取讨论
       * enterDiscussion: 进入讨论
       * searchDiscussion: 搜索讨论
       * addDiscussion: 添加讨论
       * reviewDiscussion: 审核讨论
       * deleteDiscussion: 删除讨论
       */
      // getDiscussions() {
      //   this.$http({
      //     url: "api/forum/getforumpage/",
      //     method: "get",
      //     params: {
      //       section: 0
      //     }
      //   })
      //     .then((response) => {
      //       console.log(response);
      //       this.discussions = response.data.content;
      //       console.log(this.discussions);
      //       this.show = true;
      //     })
      //     .catch((error) => {
      //       console.log(error);
      //     });
      // },
      enterDiscussion(id) {
        this.$router.push({
          name:'Discussion',
          params: {
            id: id
          }
        });
      },
      // addDiscussion() {
      //   this.$router.push({ 
      //     name: 'AddDiscussion',
      //   })
      // },
      reviewDiscussion() {

      },
      
      deleteDiscussion(discussionID, key) {
        this.$http({
          url: "api/forum/deleteforum/",
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
            forum_id: discussionID
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
              this.$emit("deleteDiscussion", key);
              
            }
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      },
      /**
       * 其他
       */
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
        this.page = 1;
        this.pageSize = val;
      },
      //当前页改变时触发 跳转其他页
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.page = val;
      },
      // getUserTokenInfo() {
      //   this.$http({
      //     url: "api/user/getusertokeninfo/",
      //     method: "get",
      //     params: {
      //       token: this.$cookies.get("token"),
      //     }
      //   })
      //     .then((response) => {
      //       this.userRight = response.data.data.data.capacity;
      //       console.log(this.userRight);
      //     })
      // },
      isShowAdministration() {
        if (this.userRight === null) {
          return false;
        }
        else if (this.userRight > 1) {
          return false;
        }
        else {
          return true;
        }
      },
      // myAdministration() {
      //   this.$http({
      //     url: "api/user/getusertokeninfo/",
      //     method: "get",
      //     params: {
      //       token: this.$cookies.get("token"),
      //     }
      //   })
      //     .then((response) => {
      //       this.userRight = response.data.data.data.capacity;
      //       console.log(this.userRight);
      //     })
      // }
    }
  }
</script>

<style>
  .discussions .discussion {
    text-align: left;
    margin: 5px 0;

  }
  .discussions .discussion:hover {
    cursor: pointer;
  }
  .discussions .discussion-header {
    display: flex;
    justify-content: space-between;
    margin: 0;
    padding: 0;
  }
  .discussion .discussion-header .title {
    font-size: 1.2em;

    /* 使内容最多一行 */
    -webkit-line-clamp: 1;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
  }
  .discussions .discussion-main {
    margin: 5px 0px;
    padding: 0;
    color: grey;

    /* 使内容最多两行 */
    -webkit-line-clamp: 2;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;


  }
  .discussions .discussion-footer .button{
    
    font-size: 0.8em;
    color: grey;
    text-align: left;
  }

  .discussions .header .search ::placeholder {
    text-align: center;
  }

  .discussions .button {
    background-color: white;
    color: black;
    border: none;
    padding: 0;
    width: auto;
    min-height: 14px;
  }
  .discussions .button:hover {
    background-color: white;
    color: #409EFF;
  }
</style>
