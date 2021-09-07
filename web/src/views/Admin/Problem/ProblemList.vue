<template>
    <div class="problem-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <ProblemList :admin="true"/>
        </div>
    </div>
</template>

<script>
import ProblemList from '@/components/Problem/ProblemList.vue'

export default {
  components: {
      ProblemList: ProblemList
  },
    
}
</script>

<style scoped>
.problem-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .problem-list {
        width: 100%;
    }
}
</style>