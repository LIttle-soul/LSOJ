<template>
  <el-card class="ranking-card">
    <template #header>
      <span class="ranking-ranking1">新闻</span>
    </template>
    <div v-for="item in conInfo" :key="item.key">
      <el-link @click="toNews(item.key)">{{ item.text }}</el-link>
    </div>
    <el-button class="bottom-button" type="text" @click="moreNews()"
      >more</el-button
    >
  </el-card>
</template>
<script>
import { mapState } from "vuex";
export default {
  name: "Home",
  computed: {
    ...mapState("news", {
      temp_data: (state) => state.news_list,
    }),
  },
  created() {
    this.conInfo = this.formatData(this.temp_data);
  },
  data() {
    return {
      conInfo: [],
    };
  },
  methods: {
    moreNews() {
      this.$router.push({ path: "/newslist" });
    },
    toNews(val) {
      this.$router.push({ path: "/shownews/" + val });
    },
    formatData(val) {
      let len = Math.min(val.length, 10);
      return val
        .map((item) => ({
          text: item.news_title,
          key: item.news_id,
        }))
        .splice(-len)
        .reverse();
    },
  },
};
</script>

<style scoped>
.ranking-card {
  width: 95%;
  min-height: 200px;
  position: relative;
}
.ranking-ranking1 {
  width: 50%;
  float: left;
  height: 40px;
}
.ranking-card .card-info {
  line-height: 16px;
  font-size: 14px;
}
.ranking-card .bottom-button {
  position: absolute;
  bottom: 0;
  right: 20px;
}
</style>
