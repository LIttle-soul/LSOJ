<template>
  <div class="rank-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-guide"></i>
          排名列表
          <span class="sort-button">
            <el-button size="mini" @click="sort_by('year')">按年排序</el-button>
            <el-button size="mini" @click="sort_by('month')"
              >按月排序</el-button
            >
            <el-button size="mini" @click="sort_by('week')">按周排序</el-button>
            <el-button size="mini" @click="sort_by('day')">按日排序</el-button>
          </span>
        </div>
      </template>
      <div>
        <RankList :Data="Data" />
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { getRankList } from "@/api/rank";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    RankList: defineAsyncComponent(() =>
      import("@/components/Rank/RankList.vue")
    ),
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("rank", {
      temp_data: (state) => state.rank_list,
    }),
    ...mapGetters("rank", {
      filterRankList: "filterRankList",
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data(this.search_data);
    },
    temp_data() {
      this.Data = this.formatData(this.temp_data);
    },
  },
  created() {
    this.Data = this.formatData(this.temp_data);
  },
  data() {
    return {
      search_data: "",
      Data: [
        {
          user_rank: 1,
          user_id: "user_1",
          user_nick: "nick_1",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
        {
          user_rank: 2,
          user_id: "user_2",
          user_nick: "nick_2",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
        {
          user_rank: 3,
          user_id: "user_3",
          user_nick: "nick_3",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      this.Data = this.formatData(this.filterRankList(val));
    },
    formatData(val) {
      return val.map((item, index) => ({
        user_rank: index + 1,
        user_id: item.user_id,
        user_nick: item.user_nick,
        true_submit: item.solved,
        all_submit: item.submit,
        percentage:
          ((item.success / item.submit) * 100).toFixed(2).toString() + "%",
      }));
    },
    async sort_by(val) {
      let temp = await getRankList(val);
      this.Data = this.formatData(temp.message);
    },
  },
};
</script>

<style scoped>
.rank-list {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
}
.table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.sort-button {
  width: 400px;
  float: right;
  transform: translateY(-1px);
}
.sort-button button {
  margin: 0 5px;
}
@media screen and (max-width: 1000px) {
  .rank-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .sort-button {
    display: none;
  }
}
</style>
