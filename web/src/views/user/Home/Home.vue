<template>
  <div style="width: 80%; margin: 50px auto;">
    <el-carousel :interval="4000" type="card" height="200px">
      <el-carousel-item v-for="item in 6" :key="item">
        <h3 class="medium">{{item}}</h3>
      </el-carousel-item>
    </el-carousel>
    <el-skeleton :row="5" animated v-for="item in 10" :key="item" style="margin: 50px auto;"></el-skeleton>
  </div>
</template>

<script>
  
</script>

<style scoped>
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }

  .el-skelenton {
    margin: 50px auto;
  }
</style>

