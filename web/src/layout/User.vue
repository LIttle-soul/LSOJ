<template>
  <div class="page">
    <div class="header">
      <Header />
    </div>
    <el-container class="main">
      <router-view />
      <el-backtop></el-backtop>
    </el-container>

    <div class="footer">
      <Footer />
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "@/components/Header/Header.vue";
import Footer from "@/components/Footer/Footer.vue";
</script>

<style scoped lang="scss">
.page {
  min-height: 100%;
  .header {
    width: 100%;
    min-width: 360px;
    height: 60px;
    z-index: 100;
    position: sticky;
    top: 0;
  }
  .main {
    width: 100%;
    min-width: 360px;
    min-height: calc(100vh - 187px);
    position: relative;
  }
  .footer {
    width: 100%;
    min-width: 360px;
  }
}
</style>
