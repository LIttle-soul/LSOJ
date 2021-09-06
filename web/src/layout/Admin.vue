<template>
  <el-container class="admin-layout">
    <el-aside class="left-nav" style="width: auto;">
      <LeftNav :isCollapse="isCollapse" @hasSelect="hasSelect" />
    </el-aside>
    <div class="main">
      <div class="header">
        <el-button
          size="mini"
          class="button-icon"
          icon="el-icon-suitcase"
          @click="isCollapse = !isCollapse"
        ></el-button>
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item v-for="item in header" :key="item">{{item}}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-button type="primary" size="mini" class="back-button" @click="to">返回前台</el-button>
      </div>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </el-container>
</template>

<script>
import LeftNav from "@/components/Header/LeftNav.vue";

export default {
  components: {
    LeftNav,
  },
  setup() {},
  data() {
    return {
      isCollapse: true,
      header: ["首页"]
    };
  },
  methods: {
    hasSelect(val) {
      // console.log(val);
      this.header = val;
    },
    to() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.admin-layout {
  width: 100%;
  height: 100%;
}
.left-nav {
  height: 100vh;
  background-color: rgba(0, 5, 5, 0.1);
}
.main {
  width: 100%;
  height: 100vh;
  overflow: auto;
  background-color: antiquewhite;
}
.button-icon {
  background: none;
  border: none;
  font-size: 25px;
  float: left;
}
.header {
  width: 100%;
  height: 40px;
  line-height: 40px;
  background: #66456645;
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
</style>
