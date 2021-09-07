<template>
    <div class="judger-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <JudgerList />
        </div>
    </div>
</template>

<script>
import JudgerList from '@/components/Judger/JudgerList.vue'

export default {
  components: {
      JudgerList: JudgerList
  },
    
}
</script>

<style scoped>
.judger-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .judger-list {
        width: 100%;
    }
}
</style>