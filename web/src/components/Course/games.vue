<template>
  <div>
    <div class="page">
      <div
        class="item"
        v-for="(item, index) in game_data"
        :key="index"
        @click="to(index)"
      >
        {{ item || "" }}
      </div>
    </div>
    <el-button @click="game_data.sort(randomsort)">开始</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElMessageBox } from "element-plus";
import { ref } from "vue";

let game_data = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]);
function randomsort(a: number, b: number) {
  return Math.random() > 0.5 ? -1 : 1;
}
function swap(a: number, b: number) {
  let c = game_data.value[b];
  game_data.value[b] = game_data.value[a];
  game_data.value[a] = c;
}
function check(x: number, y: number) {
  let temp = game_data.value.indexOf(0);
  // console.log(`(${x},${y}), ${temp}`);
  if (
    (x - 1 >= 0 && y * 4 + (x - 1) === temp) ||
    (x + 1 < 4 && y * 4 + (x + 1) === temp) ||
    (y - 1 >= 0 && (y - 1) * 4 + x === temp) ||
    (y + 1 < 4 && (y + 1) * 4 + x === temp)
  ) {
    return true;
  } else {
    return false;
  }
}
function to(b: number) {
  let temp = game_data.value.indexOf(0);
  let x = b % 4;
  let y = Math.floor(b / 4);
  if (check(x, y)) {
    swap(b, temp);
    let pd = true;
    if (game_data.value.indexOf(0) === 15) {
      // console.log(true);
      for (let i = 0; i < 15; i++) {
        if (game_data.value[i] !== i + 1) {
          pd = false;
          break;
        }
      }
      if (pd) {
        ElMessageBox.alert("通关成功", "提示");
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  width: 400px;
  height: 400px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr 1fr;
  grid-gap: 1px;
  .item {
    width: 100%;
    background-color: aquamarine;
    font-size: 60px;
    line-height: 100px;
    text-align: center;
  }
}
</style>
