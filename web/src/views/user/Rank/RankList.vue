<template>
    <div class="rank-list">
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
      RankList: defineAsyncComponent(() => import('@/components/Rank/RankList.vue'))
  },
    
}
</script>

<style scoped>
.rank-list {
    width: 80%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .rank-list {
        width: 100%;
    }
}
</style>