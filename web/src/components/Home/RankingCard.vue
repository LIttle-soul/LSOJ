<template>
    <el-card class="ranking-card">
        <template #header>
            <span class="ranking-ranking1">排名</span>
            <span class="ranking-ranking2">
              <el-button @click="changeMonth" type="text">每月</el-button>
              <el-button @click="changeWeek" type="text">每周</el-button>
              <el-button @click="changeDay" type="text">每日</el-button>
            </span>
        </template>
        <div v-for="item in conInfo" :key="item.key" class="card-info">
          <span>{{item.title}}</span>
          <span>{{item.text}}</span>
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
        {'title': '总提交量1', 'text': 12456, 'key': 1},
        {'title': '昨日提交', 'text': 250, 'key': 2},
        {'title': '题目总数', 'text': 3215, 'key': 3},
        {'title': '注册用户', 'text': 6343, 'key': 4},
      ]
    }
  },
  components: {
  },
  methods: {
    changeMonth() {
      this.conInfo = [
        {'title': '总提交量2', 'text': 12456, 'key': 1},
        {'title': '昨日提交', 'text': 250, 'key': 2},
        {'title': '题目总数', 'text': 3215, 'key': 3},
        {'title': '注册用户', 'text': 6343, 'key': 4},
      ]
    },
    changeWeek() {
      this.conInfo = [
        {'title': '总提交量3', 'text': 12456, 'key': 1},
        {'title': '昨日提交', 'text': 250, 'key': 2},
        {'title': '题目总数', 'text': 3215, 'key': 3},
        {'title': '注册用户', 'text': 6343, 'key': 4},
      ]
    },
    changeDay() {
      this.conInfo = [
        {'title': '总提交量4', 'text': 12456, 'key': 1},
        {'title': '昨日提交', 'text': 250, 'key': 2},
        {'title': '题目总数', 'text': 3215, 'key': 3},
        {'title': '注册用户', 'text': 6343, 'key': 4},
      ]
    }
  }
};
</script>

<style scoped>
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
.ranking-card .card-info {
  line-height: 20px;
  font-size: 14px;
}
.ranking-card .card-info span:last-child {
  float: right;
}
.ranking-card .bottom-button {
    float: right;
}
</style>
