<template>
  <div>
    <div class="home-header">
      <Header />
    </div>
    <div class="top-margin"></div>
    <el-container class="home-main">
      <router-view />
      <el-backtop></el-backtop>
    </el-container>
    <div class="home-footer">
      <Footer />
    </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";

export default {
  name: "User",
  components: {
    Header: defineAsyncComponent(() =>
      import("@/components/Header/Header.vue")
    ),
    Footer: defineAsyncComponent(() =>
      import("@/components/Footer/Footer.vue")
    ),
  },
};
</script>

<style scoped>
.home-header {
  width: 100%;
  min-width: 360px;
  position: fixed;
  /* top: 10px; */
  z-index: 100;
}
.top-margin {
  width: 100%;
  height: 70px;
  /* 代替头部空间 */
}
.home-main {
  width: 100%;
  min-width: 360px;
  position: relative;
}
.home-footer {
  width: 100%;
  min-width: 360;
  position: relative;
}
.router-link-active {
  text-decoration: none;
}
@media screen and (max-height: 400px) {
  .top-margin {
    height: 0;
  }
}
</style>
