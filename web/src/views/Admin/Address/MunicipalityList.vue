<template>
    <div class="municipality-list">
        <div class="echart">
            <!-- 此处用于添加图表信息 -->
        </div>
        <div class="list">
            <MunicipalityList />
        </div>
    </div>
</template>

<script>
import MunicipalityList from '@/components/Address/MunicipalityList.vue'

export default {
  components: {
      MunicipalityList: MunicipalityList
  },
    
}
</script>

<style scoped>
.municipality-list {
    width: 95%;
    max-width: 1200px;
    margin: 70px auto;
}
@media screen and (max-width: 1000px){
    .municipality-list {
        width: 100%;
    }
}
</style>