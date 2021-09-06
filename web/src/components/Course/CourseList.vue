<template>
  <div class="courses">
  <el-container >
    <el-header class="header">
      
    </el-header>
    <el-main>
      <el-row class="course-list" :gutter="20">
        <el-col class="course" :span="6"  :xs="12" :sm="8" :md="6" v-for="a in [1,2,3,4,5,6,7,8,9,10]" :key="a">
          <course-card></course-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
  </div>
</template>

<script>

import CourseCard  from "./CourseCard.vue"

export default {
  components: {
    "course-card": CourseCard
  },
  data() {
    return {
    };
    
  }
}
</script>

<style scoped>
  .courses {
    width: 80%;
    margin: 0 auto;
  }
  .courses .header {
    background-color: cornsilk;
  }
  .courses .course {
    /* margin: 0 auto; */
    margin-bottom: 2rem;
  }

  @media screen and (max-width: 800px) {
    .courses {
    width: 100%;
  }
    
  }
</style>