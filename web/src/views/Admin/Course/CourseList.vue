<template>
    <div class="course-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <CourseList />
        </div>
    </div>
</template>

<script>
import CourseList from '@/components/Course/CourseList.vue'

export default {
  components: {
      CourseList: CourseList
  },
    
}
</script>

<style scoped>
.course-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .course-list {
        width: 100%;
    }
}
</style>