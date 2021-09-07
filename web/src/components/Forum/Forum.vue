<template>
<div class="forum" v-show="show">
  <el-container>
      <el-header style="height: auto;">
        <el-button @click="addDiscussion()">添加讨论</el-button>
        <el-button @click="getMyDiscussions()">我的管理</el-button>
        <search @search=search></search>
      </el-header>
      <el-main>
        <discussions :discussions="discussions" :userRight="userRight" @deleteDiscussion="deleteDiscussion"></discussions>
      </el-main>
  </el-container>

  
</div>

</template>

<script>
// import { defineAsyncComponent } from '@vue/runtime-core'
import discussions from "@/components/Forum/Discussions.vue"
import search from "@/components/Forum/search.vue"
import { ElMessage } from 'element-plus'

export default {
  components: {
    discussions,
    search
  },
  created: function() {
    this.getDiscussions();
    this.getUserTokenInfo();
    // console.log(this.discussions)
  },

  data: function() {
    return {
      /**
       * sections: 所有板块
       * section: 当前板块
       * discussions: 所有讨论 
       */
      t_discussions: [],
      discussions: [],
      userRight: null,
      show: false
    } 
  },
  methods: {
    /**
     * getDiscussions: 获得所有讨论
     * 
     */
    getDiscussions() {
      this.$http({
        url: "api/forum/getforumpage/",
        method: "get",
        params: {
          section: 0
        }
      })
        .then((response) => {
          console.log(response);
          this.discussions = response.data.content;
          this.t_discussions = this.discussions;
          console.log(this.discussions);
          this.show = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addDiscussion() {
      this.$router.push({ 
        name: 'AddDiscussion',
      })
    },
    getMyDiscussions() {
      this.$router.push({
        name: "MyDiscussions"
      })
      this.$http({
        url: "api/forum/getmyforum/",
        method: "get",
        params: {
          token: this.$cookies.get("token"),
          forum_status: 1,
          is_admin: 0
        }
      })
        .then((response) => {
          if (response.data.err !== undefined) {
            ElMessage(response.data.err);
            console.log(response.data.err);
          }
          else {
            this.discussions = response.data.content;
            this.userRight = 1;
            console.log(response);
          }
          
        })
        .catch((err) => {
          ElMessage(err.data.err);
          console.log(err);
        })
    },
    getUserTokenInfo() {
      this.$http({
        url: "api/user/getusertokeninfo/",
        method: "get",
        params: {
          token: this.$cookies.get("token"),
        }
      })
        .then((response) => {
          this.userRight = response.data.data.data.capacity;
          console.log(this.userRight);
        })
    },
    deleteDiscussion(key) {
      this.discussions.splice(key, 1);
    },
    search(input) {
      this.discussions = this.t_discussions.filter( value => {
        console.log(value.forum_title);
        return value.forum_title.indexOf(input) !== -1;
      });
      console.log(this.discussions);
      console.log(input);
    }
  }
}
  
</script>

<style scoped>
  .forum {
    width: 80%;
    margin: 40px auto;
    font-family: "楷体";
  }
  .forum .el-header {
    margin-bottom: 20px;
  }

  .forum .left {
    margin-right: 20px;
  }

  .forum .el-header,.forum .el-footer {
    padding: 0;
    /* background-color: #B3C0D1; */
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .forum .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    /* line-height: 200px; */
  }

  .forum .el-main {
    padding: 0;
    margin: 10px 0;
    background-color: #ffffff;
    color: #333;
    text-align: center;
    /* line-height: 160px; */
  }

  .forum .el-col {
    border-radius: 4px;
  }
  .forum .grid-content {
    cursor: pointer;
    margin: 10px 0;
    border-radius: 4px;
    /* min-height: 40px; */
  }
  .forum .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }

  @media screen and (max-width: 600px){
    .forum {
        width: 100%;
    }
  }
</style>
