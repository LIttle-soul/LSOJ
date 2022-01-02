<template>
  <el-card class="ranking-card">
    <template #header>
      <div class="header">
        <span class="card-title">统计信息</span>
      </div>
    </template>
    <div class="card-info">
      <span>总提交量</span>
      <span>{{ Data.solution_total }}</span>
    </div>
    <div class="card-info">
      <span>今日提交</span>
      <span>{{ Data.solution_today }}</span>
    </div>
    <div class="card-info">
      <span>题目总数</span>
      <span>{{ Data.problem_total }}</span>
    </div>
    <div class="card-info">
      <span>注册用户</span>
      <span>{{ Data.user_total }}</span>
    </div>
  </el-card>
</template>
<script lang="ts" setup>
let props = defineProps({
  Data: {
    type: undefined,
    default: {
      problem_total: 0,
      solution_today: 0,
      solution_total: 0,
      user_total: 0,
    },
  },
});
</script>
<style scoped lang="scss">
.ranking-card {
  width: 99%;
  min-height: 200px;
  margin-bottom: 40px;
  border-radius: 20px;
  .header {
    height: 40px;
    line-height: 40px;
    padding: 0 10px;
    font-size: 16px;
  }
  .card-info {
    line-height: 16px;
    font-size: 14px;
    line-height: 28px;
    span:last-child {
      float: right;
    }
  }
}
</style>
