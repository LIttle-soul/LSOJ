<template>
    <div class="team-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <TeamList />
        </div>
    </div>
</template>

<script>
import TeamList from '@/components/User/TeamList.vue'

export default {
  components: {
      TeamList: TeamList
  },
    
}
</script>

<style scoped>
.team-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .solution-list {
        width: 100%;
    }
}
</style>