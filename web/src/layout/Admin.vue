<template>
  <el-container class="admin-layout">
    <el-aside class="left-nav" style="width: auto">
      <LeftNav :isCollapse="isCollapse" @hasSelect="hasSelect" />
    </el-aside>
    <div class="main">
      <div class="header">
        <el-button size="mini" class="button-icon" @click="isCollapse = !isCollapse"
          ><el-icon size="20"><i class="bi bi-exclude"></i></el-icon
        ></el-button>
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item v-for="item in header" :key="item">{{
            item
          }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-button type="primary" size="mini" class="back-button" @click="to"
          >返回前台</el-button
        >
      </div>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import LeftNav from "@/components/Header/LeftNav.vue";
import { Menu } from "@element-plus/icons";

let router = useRouter();

let isCollapse = ref(true);
let header = ref(["首页"]);
let hasSelect = (val: any) => {
  // console.log(val);
  header = val;
};
let to = () => {
  router.push("/");
};
</script>

<style scoped lang="scss">
.admin-layout {
  width: 100%;
  height: 100%;
  .left-nav {
    height: 100vh;
    background-color: rgba(0, 5, 5, 0.1);
  }
  .main {
    width: 100%;
    height: 100vh;
    overflow: auto;
    background-color: antiquewhite;
    .header {
      width: 100%;
      height: 40px;
      line-height: 40px;
      background: #66456645;
      .button-icon {
        background: none;
        border: none;
        font-size: 25px;
        float: left;
      }
      .el-breadcrumb {
        line-height: 40px;
        font-size: 15px;
        font-family: "宋体";
        font-weight: 500;
        float: left;
      }
      .back-button {
        float: right;
        margin: 5px 10px;
      }
    }
  }
}
</style>
