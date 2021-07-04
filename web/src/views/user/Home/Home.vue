<template>
  <div style="width: 80%; margin: 50px auto; position: sticky;">
        <el-carousel :interval="4000" type="card" height="200px">
          <el-carousel-item v-for="item in 6" :key="item">
            <h3 class="medium">{{item}}</h3>
          </el-carousel-item>
        </el-carousel>
    </div>
  <el-container>
    <el-aside
    style="width: 25%;">
      <el-card
      >
        <div
        v-for="item in 4"
        :key="item"
        >
          {{'列表内容' + item}}
        </div>
      </el-card>
      <el-card
      >
        <div
        v-for="item in 4"
        :key="item"
        >
          {{'列表内容' + item}}
        </div>
      </el-card>
      <el-card
      >
        <div
        v-for="item in 4"
        :key="item"
        >
          {{'列表内容' + item}}
        </div>
      </el-card>
      <UpLoad />
    </el-aside>
    <el-main>
      <el-skeleton :row="5" animated v-for="item in 10" :key="item" style="margin: 50px auto;"></el-skeleton>
    </el-main>
  </el-container>
</template>

<script>
import { defineAsyncComponent } from '@vue/runtime-core'

export default {
  name: "Home",
  setup() {
    
  },
  components: {
    UpLoad: defineAsyncComponent(() => import('@/components/UpLoad.vue')),
  }
}
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
  .el-card {
    margin: 40px 0;
    border-radius: 20px;
  }
  .el-card div {
    width: 100%;
    height: 40px;
    line-height: 40px;
  }
  @media screen and (max-width: 600px) {
    .el-aside {
      display: none;
    }
  }
</style>