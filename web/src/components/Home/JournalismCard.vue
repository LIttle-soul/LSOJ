<template>
    <el-card class="ranking-card">
        <template #header>
            <span class="card-title">统计信息</span> 
        </template>
        <div v-for="item in conInfo" :key="item.key" class="card-info">
          <span>{{item.title}}</span>
          <span>{{item.text}}</span>
        </div>
      </el-card>
</template>
<script>

export default {
  name: "Home",
  setup() {},
   data() {
    return {
      conInfo: [
        {'title': '总提交量', 'text': 12456, 'key': 1},
        {'title': '昨日提交', 'text': 250, 'key': 2},
        {'title': '题目总数', 'text': 3215, 'key': 3},
        {'title': '注册用户', 'text': 6343, 'key': 4},
      ]
    }
  },
}
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
.ranking-card .card-title{
    width: 50%;
    float: left;
    height: 40px;
    /* background-color: aqua; */
}
.ranking-card .card-info {
  line-height: 30px;
}
.ranking-card .card-info span:last-child {
  float: right;
}
</style>
