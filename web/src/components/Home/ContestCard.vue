<template>
  <div class="contest-card">
    <el-card class="content">
      <template #header>
        <span class="header">近期比赛</span>
        <el-button type="text" @click="more">more</el-button>
      </template>
      <el-card
        shadow="hover"
        class="container"
        v-for="item in Data"
        :key="item.contest_id"
        @click="linkTo(item.contest_id)"
      >
        <template #header>
          <span class="content-header">{{ item.contest_title }}</span>
          <el-tag type="success" size="mini" class="content-tag">{{
            filter_status_data[item.contest_type].text
          }}</el-tag>
        </template>
        <div class="container-text">
          <p>
            <span>状态: {{ item.contest_status }}</span
            ><span>{{ item.begin_time }}</span>
          </p>
          <p>
            <span>命题: {{ item.contest_creator }}</span
            ><span>{{ item.end_time }}</span>
          </p>
        </div>
      </el-card>
    </el-card>
    <!-- <el-card class="content">
      <template #header>
        <span class="header">其他比赛</span>
      </template>
      <el-card shadow="hover" class="container" v-for="item in 6" :key="item">
        <template #header>
          <span class="content-header">竞赛{{ item }}</span>
          <el-tag type="success" size="mini" class="content-tag">公开</el-tag>
        </template>
        <div class="container-text">
          <p><span>状态: 比赛中</span><span>2020-01-02 12:12:00</span></p>
          <p><span>命题: LiSoul</span><span>2020-01-02 12:12:00</span></p>
        </div>
      </el-card>
    </el-card> -->
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
export default {
  computed: {
    ...mapState("contest", {
      temp_data: (state) => state.contest_list,
    }),
    ...mapGetters("contest", {
      getContestList: "filterContestByTime",
    }),
  },
  watch: {
    temp_data() {
      this.Data = this.formatData(this.getContestList());
    },
  },
  created() {
    this.Data = this.formatData(this.getContestList());
    // console.log(this.Data);
  },
  data() {
    return {
      Data: [],
      filter_status_data: [
        { text: "公开", value: 0 },
        { text: "私有", value: 1 },
        { text: "作业", value: 2 },
        { text: "竞赛", value: 3 },
      ],
    };
  },
  methods: {
    more() {
      this.$router.push({
        path: "contestlist",
      });
    },
    linkTo(val) {
      this.$router.push("/contestshow/" + val);
    },
    formatData(val) {
      return val.map((item) => ({
        contest_id: item.contest_id,
        contest_title: item.contest_title,
        begin_time: this.$dayJS(item.start_time).format("YYYY-MM-DD HH:mm:ss"),
        end_time: this.$dayJS(item.end_time).format("YYYY-MM-DD HH:mm:ss"),
        contest_type: item.contest_province,
        contest_creator: item.contest_creator,
        contest_status: this.getContestStatus(item.start_time, item.end_time),
      }));
    },
    getContestStatus(begin_time, end_time) {
      if (this.$dayJS().isBefore(this.$dayJS(begin_time))) {
        return "未开始";
      } else if (this.$dayJS().isBefore(this.$dayJS(end_time))) {
        return "比赛中";
      } else {
        return "已结束";
      }
    },
  },
};
</script>

<style>
.contest-card .el-card__body {
  padding: 0;
}
.contest-card .container .el-card__header {
  padding: 0;
  height: 35px;
  line-height: 30px;
}
</style>

<style scoped>
.contest-card {
  width: 100%;
}
.contest-card .content {
  width: 100%;
  min-height: 400px;
  margin: 20px 0;
  position: relative;
}
.contest-card .content .el-button {
  position: absolute;
  right: 20px;
  top: 6px;
}
.contest-card .header {
  font-weight: 800;
  max-width: 50%;
}

.contest-card .container {
  width: 45%;
  margin: 15px 0;
  min-height: 120px;
  position: relative;
}
.contest-card .container:nth-child(2n-1) {
  float: left;
  margin-left: 3%;
}
.contest-card .container:nth-child(2n) {
  float: right;
  margin-right: 3%;
}

.contest-card .content-header {
  font-size: 12px;
  margin-left: 12px;
}
.contest-card .content-tag {
  position: absolute;
  right: 10px;
  top: 6px;
}
.contest-card .container-text {
  font-size: 8px;
  height: 100%;
  width: 95%;
  margin: 0 auto;
}
.contest-card .container-text p {
  line-height: 40px;
}
.contest-card .container-text p span:last-child {
  float: right;
}
</style>
