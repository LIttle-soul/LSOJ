<template>
  <div class="app">
    <el-config-provider :locale="zhCn">
      <router-view />
    </el-config-provider>
  </div>
</template>
<script setup lang="ts">
import { ElConfigProvider } from "element-plus";
import zhCn from "element-plus/lib/locale/lang/zh-cn";
import { useStore } from "vuex";
let store = useStore();
store.dispatch("user/checkUserStatus");
</script>
<style lang="scss">
@import url("./assets/css/reset.css");
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.0/font/bootstrap-icons.css");
.app {
  position: relative;
  height: 100%;
}
</style>
