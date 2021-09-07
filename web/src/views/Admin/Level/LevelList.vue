<template>
    <div class="level-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <LevelList />
        </div>
    </div>
</template>

<script>
import LevelList from '@/components/Level/LevelList.vue'

export default {
  components: {
      LevelList: LevelList
  },
    
}
</script>

<style scoped>
.level-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .level-list {
        width: 100%;
    }
}
</style>