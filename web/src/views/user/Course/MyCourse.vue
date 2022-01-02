<template>
  <div class="my-course">
    <div class="my-course-left">
      <div class="ucnavigation-header">
        <h5>学生空间</h5>
      </div>
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
      >
        <el-menu-item index="/wecoursehome/mycourselist">
          <span>我的课程</span>
        </el-menu-item>
        <el-menu-item index="/wecoursehome/homework">
          <span>我的作业</span>
        </el-menu-item>
        <el-menu-item index="/wecoursehome/mytest">
          <span>我的测验</span>
        </el-menu-item>
        <el-menu-item index="/wecoursehome/myexam">
          <span>我的考试</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="my-course-right">
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts" setup></script>

<style scoped lang="scss">
.my-course {
  max-width: 1200px;
  width: 1200px;
  margin: 50px auto;
  /* background: rgb(228, 225, 225); */
  .my-course-left {
    width: 18%;
    height: 80%;
    float: left;
    /* background: greenyellow; */
    .ucnavigation-header {
      width: 99%;
      height: 50px;
      background: #ffffff;
      border-radius: 10px 10px 0 0;
      border: 1px solid #e1e1e1;
      text-align: center;
      h5 {
        margin-top: 4%;
        font: 1.5em sans-serif;
      }
      .el-menu {
        border: 1px solid #e1e1e1;
      }
    }
  }
  .my-course-right {
    width: 80%;
    height: 100%;
    /* background: blue; */
    float: right;
  }
}
</style>
