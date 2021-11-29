<template>
  <el-card class="ranking-card">
    <template #header>
      <div class="header">
        <span class="ranking-ranking1">排名</span>
        <span class="ranking-ranking2">
          <el-button @click="sort_by('month')" type="text">每月</el-button>
          <el-button @click="sort_by('week')" type="text">每周</el-button>
          <el-button @click="sort_by('day')" type="text">每日</el-button>
        </span>
      </div>
    </template>
    <div v-for="(item, index) in prop.Data" :key="index" class="card-info">
      <span>{{ item.user_nick }}</span>
      <span>{{ item.true_submit }}</span>
    </div>
    <el-button class="bottom-button" type="text" @click="to('ranklist')">more</el-button>
  </el-card>
</template>
<script lang="ts" setup>
import { useRouter } from "vue-router";

let router = useRouter();

let prop = defineProps({
  Data: {
    type: undefined,
    default: <any>[],
  },
});
let emit = defineEmits(["sortBy"]);
let sort_by = (val: String) => {
  emit("sortBy", val);
};
let to = (val: string) => {
  router.push({ path: val });
};
</script>

<style lang="scss">
.ranking-card {
  .el-card__header {
    padding: 0;
  }
}
</style>

<style scoped lang="scss">
.ranking-card {
  width: 99%;
  min-height: 200px;
  position: relative;
  margin-bottom: 40px;
  .header {
    font-size: 16px;
    height: 40px;
    // background-color: #d3d3d3;
    line-height: 40px;
    padding: 0 10px;
    display: flex;
    .ranking-ranking1 {
      width: 50%;
      height: 40px;
      // background-color: aqua;
    }
    .ranking-ranking2 {
      width: 50%;
      height: 40px;
      // background-color: beige;
      .el-button {
        color: #000;
        width: 25%;
        margin: 0;
        font-size: 10px;
        float: right;
      }
    }
  }
  .card-info {
    line-height: 16px;
    font-size: 14px;
    span:last-child {
      float: right;
    }
  }
  .bottom-button {
    position: absolute;
    bottom: 0;
    right: 20px;
  }
}
</style>
