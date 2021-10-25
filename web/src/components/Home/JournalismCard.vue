<template>
  <el-card class="ranking-card">
    <template #header>
      <span class="card-title">统计信息</span>
    </template>
    <div v-for="item in conInfo" :key="item.key" class="card-info">
      <span>{{ item.title }}</span>
      <span>{{ item.text }}</span>
    </div>
  </el-card>
</template>
<script>
import { mapGetters, mapState } from "vuex";

export default {
  name: "Home",
  computed: {
    ...mapState("solution", {
      solution_list: (state) => state.solution_list,
    }),
    ...mapState("problem", {
      problem_list: (state) => state.problem_list,
    }),
    ...mapState("user", {
      user_list: (state) => state.user_list,
    }),
    ...mapGetters("solution", {
      getSolutionList: "filterDaySolution",
    }),
  },
  mounted() {
    this.setData();
  },
  data() {
    return {
      conInfo: [
        { title: "总提交量", text: 0, key: 1 },
        { title: "今日提交", text: 0, key: 2 },
        { title: "题目总数", text: 0, key: 3 },
        { title: "注册用户", text: 0, key: 4 },
      ],
    };
  },
  methods: {
    setData() {
      this.conInfo[0].text = this.solution_list.length;
      this.conInfo[1].text = this.getSolutionList().length;
      this.conInfo[2].text = this.problem_list.length;
      this.conInfo[3].text = this.user_list.length;
    },
  },
};
</script>
<style scoped>
.ranking-card {
  width: 95%;
  min-height: 200px;
}
.ranking-card .card-title {
  width: 50%;
  float: left;
  height: 40px;
  /* background-color: aqua; */
}
.ranking-card .card-info {
  line-height: 16px;
  font-size: 14px;
  line-height: 28px;
}
.ranking-card .card-info span:last-child {
  float: right;
}
</style>
