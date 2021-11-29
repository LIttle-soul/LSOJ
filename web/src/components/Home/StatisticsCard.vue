<template>
  <el-card class="ranking-card">
    <template #header>
      <div class="header">
        <span>新闻</span>
      </div>
    </template>
    <div v-for="item in con_info" :key="item.key">
      <el-link @click="toNews(item.key)">{{ item.text }}</el-link>
    </div>
    <el-button class="bottom-button" type="text" @click="moreNews()">more</el-button>
  </el-card>
</template>
<script lang="ts" setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
let router = useRouter();
let conInfo = defineProps({
  con_info: {
    type: undefined,
    default: <any>[],
  },
});
let toNews = (val: String) => {
  router.push({ path: "/shownews/" + val });
};
let moreNews = () => {
  router.push({ path: "/newslist" });
};
</script>

<style scoped lang="scss">
.ranking-card {
  width: 99%;
  min-height: 200px;
  position: relative;
  margin-bottom: 40px;
  .header {
    font-size: 16px;
    height: 40px;
    line-height: 40px;
    padding: 0 10px;
  }
  .bottom-button {
    position: absolute;
    bottom: 0;
    right: 20px;
  }
}
</style>
