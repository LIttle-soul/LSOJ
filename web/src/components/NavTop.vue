<template>
<el-row>
  <el-rol
  :span="4"
  class="logo">LSOJ</el-rol>
  <el-col
  :span="14"
  >
  <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    text-color="#699"
    active-text-color="#ffd04b"
  >
    <el-menu-item index="1"><router-link to="/">首页</router-link></el-menu-item>
    <el-menu-item index="2">问题</el-menu-item>
    <el-menu-item index="3">竞赛</el-menu-item>
    <el-menu-item index="4"><router-link to="/ceshi">闯关</router-link></el-menu-item>
    <el-menu-item index="5"><router-link to="/login">登录</router-link></el-menu-item>
  </el-menu>
  </el-col>
  <el-col
  :span="2"
  class="icon"
  >

  </el-col>
</el-row>
  
</template>

<script>
export default {
  data() {
    return {
      activeIndex: "1",
      activeIndex2: "1",
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<style>
</style>
