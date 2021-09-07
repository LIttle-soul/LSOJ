<template>
    <div class="forum-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <ForumList :admin="true" />
        </div>
    </div>
</template>

<script>
import ForumList from '@/components/Forum/ForumList.vue'

export default {
  components: {
      ForumList: ForumList
  },
    
}
</script>

<style scoped>
.forum-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .forum-list {
        width: 100%;
    }
}
</style>