<template>
    <div class="contest-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <ContestList :admin="true" />
        </div>
    </div>
</template>

<script>
import ContestList from '@/components/Contest/ContestList.vue'

export default {
  components: {
      ContestList: ContestList
  },
    
}
</script>

<style scoped>
.contest-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .contest-list {
        width: 100%;
    }
}
</style>