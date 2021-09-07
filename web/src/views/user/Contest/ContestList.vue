<template>
    <div class="contest-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <ContestList/>
        </div>
    </div>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core';

export default {
  components: {
      ContestList: defineAsyncComponent(() => import('@/components/Contest/ContestList.vue'))
  },
    
}
</script>

<style scoped>
.contest-list {
    width: 80%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .contest-list {
        width: 100%;
    }
}
</style>