<template>
    <div class="province-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <ProvinceList />
        </div>
    </div>
</template>

<script>
import ProvinceList from '@/components/Address/ProvinceList.vue'

export default {
  components: {
      ProvinceList: ProvinceList
  },
    
}
</script>

<style scoped>
.province-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .province-list {
        width: 100%;
    }
}
</style>