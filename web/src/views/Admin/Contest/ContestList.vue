<template>
  <div class="contest-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          竞赛列表
          <div class="current-time">当前时间:{{ current_time }}</div>
        </div>
        <el-input
          placeholder="请输入内容"
          size="mini"
          v-model="search_data"
          class="input-with-select"
        >
          <template #append>
            <el-button
              icon="el-icon-search"
              @click="search_all_data"
            ></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <ContestList :Data="Data" :admin="true" />
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { mapState } from "vuex";

export default {
  components: {
    ContestList: defineAsyncComponent(() =>
      import("@/components/Contest/ContestList.vue")
    ),
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("contest", {
      temp_data: (state) => state.contest_list,
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
    this.current_time = setInterval(() => {
      this.current_time = this.$dayJS().format("YYYY-MM-DD HH:mm:ss");
    }, 1000);
    return {
      search_data: "",
      current_time: this.$dayJS().format("YYYY-MM-DD HH:mm:ss"),
      Data: [
        {
          contest_id: 1,
          contest_title: "竞赛一",
          contest_time: "@已结束 2020-02-03 12:00:00",
          contest_type: 2,
          contest_creator: "Admin",
          contest_status: true,
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      console.log(val);
    },
    formatData(val) {
      return val.map((item) => ({
        contest_id: item.contest_id,
        contest_title: item.contest_title,
        contest_time: this.$dayJS(item.start_time).format(
          "YYYY-MM-DD HH:mm:ss"
        ),
        contest_type: item.contest_province,
        contest_creator: item.contest_creator,
        contest_status: item.contest_defunct,
      }));
    },
  },
};
</script>

<style lang="css">
.contest-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.contest-list .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.contest-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
.contest-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.contest-list .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
@media screen and (max-width: 1000px) {
  .contest-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .contest-list .input-with-select {
    display: none;
  }
}
</style>
