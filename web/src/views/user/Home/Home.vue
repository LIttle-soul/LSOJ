<template>
  <div class="home">
    <div style="width: 80%; max-width: 1000px; margin: 30px auto;">
      <el-carousel :interval="4000" type="card" height="200px">
        <el-carousel-item v-for="item in 6" :key="item">
          <h3 class="medium">{{ item }}</h3>
        </el-carousel-item>
      </el-carousel>
    </div>
    <el-container>
      <el-aside style="width: 25%; min-width: 250px; max-width: 700px;">
        <RankingCard />
        <JournalismCard />
        <StatisticsCard />
      </el-aside>

      <el-main>
        <ContestCard />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";

export default {
  name: "Home",
  setup() {},
  components: {
    RankingCard: defineAsyncComponent(() =>
      import("@/components/Home/RankingCard.vue")
    ),
    JournalismCard: defineAsyncComponent(() =>
      import("@/components/Home/JournalismCard.vue")
    ),
    StatisticsCard: defineAsyncComponent(() =>
      import("@/components/Home/StatisticsCard.vue")
    ),
    ContestCard: defineAsyncComponent(() =>
      import("@/components/Home/ContestCard.vue")
    ),
  },
};
</script>

<style scoped>
.home {
  width: 80%;
  max-width: 1800px;
  margin: 0px auto;
}
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

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.el-skelenton {
  margin: 50px auto;
}
.el-card {
  margin: 40px 0;
  border-radius: 10px;
}
.el-card div {
  width: 100%;
  height: 40px;
  line-height: 40px;
}
@media screen and (max-width: 1000px) {
  .home {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .el-aside {
    display: none;
  }
}
</style>
