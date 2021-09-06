<template>
    <el-card class="ranking-card">
        <template #header>
            <span class="ranking-ranking1">新闻</span>
            
        </template>
        <div v-for="item in conInfo" :key="item.key">
          <el-link :href="item.index">{{item.text}}</el-link>
        </div>
        <el-button class="bottom-button" type="text">more</el-button>
      </el-card>
</template>
<script>
// import { defineAsyncComponent } from '@vue/runtime-core'

export default {
  name: "Home",
  setup() {},
   data() {
    return {
      conInfo: [
        {'text': 'Hello_1', 'key': 1, 'index': 'index1'},
        {'text': 'Hello_2', 'key': 2, 'index': 'index2'},
        {'text': 'Hello_3', 'key': 3, 'index': 'index3'},
        {'text': 'Hello_4', 'key': 4, 'index': 'index4'},
      ]
    }
  },
}
</script>
<style>
.ranking-card {
    width: 95%;
}
.ranking-card .el-card__header {
    font-size: 16px;
    height: 40px;
    line-height: 40px;
    padding: 0 10px;
}
.ranking-ranking1{
    width: 50%;
    float: left;
    height: 40px;
    /* background-color: aqua; */
}
.ranking-ranking2{
    width: 50%;
    height: 40px;
    float: left;
    /* background-color: beige; */
}
.ranking-ranking2 .el-button {
  color: #000;
  width: 25%;
  margin: 0;
  font-size: 10px;
  float: right;
}
.ranking-card .bottom-button {
    float: right;
}
</style>
