<template>
  <div class="home">
    <div style="width: 80%; max-width: 1000px; margin: 30px auto;">
      <el-carousel
        :interval="4000"
        type="card"
        height="240px"
        :loop="true"
        indicator-position="none"
      >
        <el-carousel-item v-for="(item, index) in image_list" :key="index">
          <img :src="item.url" :alt="item.title" class="image" />
          <p class="medium">{{ item.title }}</p>
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
  data() {
    return {
      image_list: [
        {
          title: "欢迎使用ACM系统",
          url: "http://www.52ac.net/upload/20191223/20191223081743_51152.jpg",
        },
        {
          title: "我要发飙了",
          url: "http://www.52ac.net/upload/20210301/20210301111526_40537.jpg",
        },
        {
          title: "扶我起来，我还能码",
          url: "http://www.jhcoj.cn/upload/20201104/20201104084136_31254.jpg",
        },
        {
          title: "加入我们吧",
          url: "http://www.52ac.net/upload/20191223/20191223095021_18269.jpeg",
        },
      ],
    };
  },
};
</script>

<style scoped>
.home {
  width: 80%;
  max-width: 1800px;
  margin: 0px auto;
}
.medium {
  text-align: center;
  width: 100%;
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
  font-size: 1.6rem;
  font-weight: bolder;
  color: #cfcfcf;
  text-shadow: 3px 3px 3px black, -1px -1px 3px black;
  z-index: 1;
  position: absolute;
  bottom: 20px;
  left: 0;
  overflow: hidden;
}

.image {
  width: calc(100% - 10px);
  height: calc(100% - 10px);
  z-index: -1;
  position: absolute;
  border: 5px solid #b7bdc5;
  background: #d3dce6;
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
