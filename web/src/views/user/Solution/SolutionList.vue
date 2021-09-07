<template>
    <div class="solution-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <RankList />
        </div>
    </div>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core';

export default {
  components: {
      RankList: defineAsyncComponent(() => import('@/components/Solution/SolutionList.vue'))
  },
    
}
</script>

<style scoped>
.solution-list {
    width: 80%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .solution-list {
        width: 100%;
    }
}
</style>