<template>
  <el-card class="ranking-card">
    <template #header>
      <span class="ranking-ranking1">排名</span>
      <span class="ranking-ranking2">
        <el-button @click="sort_by('month')" type="text">每月</el-button>
        <el-button @click="sort_by('week')" type="text">每周</el-button>
        <el-button @click="sort_by('day')" type="text">每日</el-button>
      </span>
    </template>
    <div v-for="(item, index) in Data" :key="index" class="card-info">
      <span>{{ item.user_nick }}</span>
      <span>{{ item.true_submit }}</span>
    </div>
    <el-button class="bottom-button" type="text" @click="to('ranklist')"
      >more</el-button
    >
  </el-card>
</template>
<script>
import { mapState } from "vuex";
import { getRankList } from "@/api/rank";

export default {
  name: "Home",
  computed: {
    ...mapState("rank", {
      temp_data: (state) => state.rank_list,
    }),
  },
  watch: {
    temp_data() {
      this.Data = this.formatData(this.temp_data);
    },
  },
  created() {
    this.Data = this.formatData(this.temp_data);
  },
  data() {
    return {
      Data: [],
    };
  },
  methods: {
    formatData(val) {
      let len = Math.min(val.length, 10);
      return val
        .map((item) => ({
          user_nick: item.user_nick,
          true_submit: item.solved,
        }))
        .splice(-len);
    },
    async sort_by(val) {
      let temp = await getRankList(val);
      this.Data = this.formatData(temp.message);
    },
    to(val) {
      this.$router.push({ path: val });
    },
  },
};
</script>

<style lang="css">
.ranking-card .el-card__header {
  font-size: 16px;
  height: 40px;
  line-height: 40px;
  padding: 0 10px;
}
</style>

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
  /* background-color: aqua; */
}
.ranking-ranking2 {
  width: 50%;
  height: 40px;
  float: left;
  /* background-color: beige; */
}
.ranking-ranking2 .el-button {
  color: #000;
  width: 25%;
  margin: 0;
  font-size: 10px;
  float: right;
}
.ranking-card .card-info {
  line-height: 16px;
  font-size: 14px;
}
.ranking-card .card-info span:last-child {
  float: right;
}
.ranking-card .bottom-button {
  position: absolute;
  bottom: 0;
  right: 20px;
}
</style>
