<template>
  <div class="class-list">
    <div class="echart">
      <!-- 此处用于添加图表信息 -->
    </div>
    <div class="list">
      <ClassList />
    </div>
  </div>
</template>

<script>
import ClassList from '@/components/School/ClassList.vue'

export default {
  components: {
    ClassList: ClassList
  },
  beforeCreate () {
    this.$store.dispatch('school/getClassList');
  },
}
</script>

<style scoped>
.class-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .class-list {
    width: 100%;
  }
}
</style>