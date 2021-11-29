<template>
  <div class="home">
    <div style="width: 80%; max-width: 1000px; margin: 30px auto">
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
      <el-aside class="aside">
        <RankingCard :Data="rank_data" @sortBy="setRankData" />
        <JournalismCard :Data="count_data" />
        <StatisticsCard :con_info="news_data" />
      </el-aside>
      <el-main>
        <ContestCard :Data="contest_data" />
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import dayJS from "dayjs";

import { getRankList } from "@/api/rank";
import { getContestList } from "@/api/contest";
import { getNewsList } from "@/api/news";
import { getCountData } from "@/api/other";

import RankingCard from "@/components//Home/RankingCard.vue";
import JournalismCard from "@/components/Home/JournalismCard.vue";
import StatisticsCard from "@/components/Home/StatisticsCard.vue";
import ContestCard from "@/components/Home/ContestCard.vue";
import { onMounted } from "@vue/runtime-core";

let image_list = [
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
];

// 子组件数据
let rank_data = ref([]);
let news_data = ref([]);
let count_data = ref([]);
let contest_data = ref([]);

// 事件处理
let formatNewsData = (val: any) => {
  let len = Math.min(val.length, 10);
  return val.map((item: any) => ({
    text: item.news_title,
    key: item.news_id,
  }));
};

let formatCountData = (val: any) => {
  return {
    problem_total: val.problem_total,
    solution_today: val.solution_today,
    solution_total: val.solution_total,
    user_total: val.user_total,
  };
};
let formatRankData = (val: any) => {
  return val.map((item: any) => ({
    user_nick: item.user_nick,
    true_submit: item.solved,
  }));
};
let getContestStatus = (begin_time: string, end_time: string) => {
  if (dayJS().isBefore(dayJS(begin_time))) {
    return "未开始";
  } else if (dayJS().isBefore(dayJS(end_time))) {
    return "比赛中";
  } else {
    return "已结束";
  }
};
let formatContestData = (val: any) => {
  return val.map((item: any) => ({
    contest_id: item.contest_id,
    contest_title: item.contest_title,
    begin_time: dayJS(item.start_time).format("YYYY-MM-DD HH:mm:ss"),
    end_time: dayJS(item.end_time).format("YYYY-MM-DD HH:mm:ss"),
    contest_type: item.contest_province,
    contest_creator: item.contest_creator,
    contest_status: getContestStatus(item.start_time, item.end_time),
  }));
};

// 数据请求
let setCountData = async () => {
  let back_data = await getCountData();
  // console.log(back_data);
  if (back_data.status) {
    count_data.value = <any>formatCountData(back_data.message);
  }
};
let setNewsData = async () => {
  let back_data = await getNewsList({
    page: 1,
    total: 10,
    text: "",
    news_id: "",
  });
  if (back_data.status) {
    news_data.value = <any>formatNewsData(back_data.message);
    // console.log(news_data.value);
  }
};
let setRankData = async (val: string) => {
  let back_data = await getRankList({
    page: 1,
    total: 10,
    sort_by: val || "",
    text: "",
  });
  if (back_data.status) {
    rank_data.value = <any>formatRankData(back_data.message);
    // console.log(rank_data.value);
  }
};
let setContestData = async () => {
  let back_data = await getContestList({
    page: 1,
    total: 10,
    status: "",
    text: "",
    contest_id: "",
    me: "",
  });
  if (back_data.status) {
    contest_data.value = <any>formatContestData(back_data.message);
    // console.log(rank_data.value);
  }
};

// 挂载执行操作
onMounted(() => {
  setCountData();
  setNewsData();
  setRankData("");
  setContestData();
});
</script>

<style scoped lang="scss">
.home {
  width: 80%;
  max-width: 1800px;
  margin: 0px auto;
  .image {
    width: calc(100% - 10px);
    height: calc(100% - 10px);
    z-index: -1;
    position: absolute;
    border: 5px solid #b7bdc5;
    background: #d3dce6;
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
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  .aside {
    width: 25%;
    min-width: 250px;
    max-width: 700px;
    margin-right: 10px;
  }
  @media screen and (max-width: 600px) {
    .aside {
      display: none;
    }
  }
}

@media screen and (max-width: 1000px) {
  .home {
    width: 100%;
  }
}
</style>
