<template>
    <div class="news-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <NewsList :admin="true" />
        </div>
    </div>
</template>

<script>
import NewsList from '@/components/News/NewsList.vue'

export default {
  components: {
      NewsList: NewsList
  },
    
}
</script>

<style scoped>
.news-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .news-list {
        width: 100%;
    }
}
</style>