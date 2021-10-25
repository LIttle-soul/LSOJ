<template>
  <div class="contest-show">
    <div class="card">
      <el-card class="left">
        <el-descriptions :column="1">
          <el-descriptions-item label="竞赛标题">{{
            contest_form.contest_title
          }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{
            contest_form.begin_time
          }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{
            contest_form.end_time
          }}</el-descriptions-item>
          <el-descriptions-item label="比赛状态">{{
            contest_form.contest_status
          }}</el-descriptions-item>
          <el-descriptions-item label="比赛类型">{{
            filter_status_data[contest_form.contest_type].text
          }}</el-descriptions-item>
          <el-descriptions-item label="报名人数">{{
            contest_form.join_people + "人"
          }}</el-descriptions-item>
          <el-descriptions-item label="创建者">{{
            contest_form.contest_creator
          }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      <div class="right">
        <Times
          :text="text"
          :endTime="end_time"
          @time-end="timeEnd"
          class="right-child"
          :key="new Date().getTime()"
        />
        <el-button
          type="primary"
          size="medium"
          v-if="contest_power"
          :disabled="!button_status"
          @click="showContestData(contest_form.contest_id)"
          >点击进入</el-button
        >
        <el-button type="primary" size="medium" @click="joinContest" v-else
          >点击报名</el-button
        >
      </div>
      <el-dialog v-model="contest_join" title="竞赛报名" width="500px">
        <ContestJoin :contest_id="contest_form.contest_id" />
      </el-dialog>
    </div>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">竞赛介绍</span>
        </div>
      </template>
      <ContestChild
        mode="preview"
        :content="contest_form.contest_content"
        :key="new Date().getTime()"
      />
    </el-card>
  </div>
</template>

<script>
import ContestChild from "@/components/Editor/MarkdownEditor.vue";
import ContestJoin from "@/components/Contest/ContestJoin.vue";
import Times from "@/components/Other/CountDown.vue";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    ContestChild,
    ContestJoin,
    Times,
  },
  computed: {
    ...mapState("user", {
      self_user: (state) => state.user_info,
    }),
    ...mapState("contest", {
      contest_data: (state) => state.contest_list,
    }),
    ...mapGetters("contest", {
      getContestData: "getContestData",
    }),
  },
  watch: {
    contest_data() {
      this.setContestData(this.$route.params.contest_id);
    },
  },
  created() {
    this.setContestData(this.$route.params.contest_id);
  },
  data() {
    return {
      text: "距离比赛开始还有",
      end_time: "2022-01-01 12:00:00",
      contest_power: false,
      button_status: true,
      contest_join: false,
      filter_status_data: [
        { text: "公开", value: 0 },
        { text: "私有", value: 1 },
        { text: "作业", value: 2 },
        { text: "竞赛", value: 3 },
      ],
      contest_form: {
        contest_id: 1,
        contest_title: "竞赛一",
        contest_content: "### Hello the first Contest",
        begin_time: "2022-01-01 12:00:00",
        end_time: "2022-01-01 14:00:00",
        contest_status: "未开始",
        contest_type: 0,
        join_people: 0,
        contest_creator: "LiSoul",
      },
    };
  },
  methods: {
    showContestData(contest_id) {
      this.$router.push("/contestdata/" + contest_id);
    },
    joinContest() {
      this.contest_join = true;
    },
    setContestData(val) {
      let data = this.getContestData(val);
      // console.log(data);
      this.contest_form = {
        contest_id: data.contest_id,
        contest_title: data.contest_title,
        contest_content: data.contest_introduce,
        begin_time: this.$dayJS(data.start_time).format("YYYY-MM-DD HH:mm:ss"),
        end_time: this.$dayJS(data.end_time).format("YYYY-MM-DD HH:mm:ss"),
        contest_status: this.getContestStatus(data.start_time, data.end_time),
        contest_type: data.contest_province,
        join_people: data.user_list.length,
        contest_creator: data.contest_creator,
      };
      this.getContestPower(data.contest_province, data.user_list);
    },
    getContestStatus(begin_time, end_time) {
      if (this.$dayJS().isBefore(this.$dayJS(begin_time))) {
        this.button_status = false;
        this.end_time = this.$dayJS(begin_time).format("YYYY-MM-DD HH:mm:ss");
        this.text = "距离比赛开始还有";
        return "未开始";
      } else if (this.$dayJS().isBefore(this.$dayJS(end_time))) {
        this.button_status = true;
        this.end_time = this.$dayJS(end_time).format("YYYY-MM-DD HH:mm:ss");
        this.text = "距离比赛结束还有";
        return "比赛中";
      } else {
        this.button_status = true;
        this.end_time = this.$dayJS(end_time).format("YYYY-MM-DD HH:mm:ss");
        this.text = "比赛已结束";
        return "已结束";
      }
    },
    getContestPower(contest_type, contest_user) {
      contest_user = contest_user.map((item) => {
        return item.user_id;
      });
      if (this.self_user === null || this.self_user === undefined) {
        this.$message({
          type: "error",
          message: "用户未登录，请先登录",
        });
        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);
      } else if (+contest_type === 0) {
        this.contest_power = true;
      } else if (contest_user.includes(this.self_user.user_id)) {
        this.contest_power = true;
      } else {
        this.contest_power = false;
      }
    },
    timeEnd() {
      if (this.button_status) {
        this.text = "比赛已结束";
      } else if (!this.button_status && this.contest_power) {
        this.text = "距离比赛结束还有";
        this.end_time = this.$dayJS(this.contest_form.end_time).format(
          "YYYY-MM-DD HH:mm:ss"
        );
      }
    },
  },
};
</script>

<style>
.contest-show .left .el-descriptions__body {
  height: 100%;
  font-family: "楷体";
  background-color: unset;
  color: black;
}
.contest-show .left .el-descriptions__body td {
  margin: 0;
  padding: 0;
  line-height: 29px;
}
.contest-show .left .el-descriptions__body td .el-descriptions__label {
  font-size: 1.2em;
  font-weight: bold;
}
</style>

<style scoped>
.contest-show {
  width: 80%;
  margin: 0 auto;
}
.card {
  width: 100%;
  margin: 60px 0;
}
.contest-show .card:first-child {
  height: 250px;
}
.left {
  width: 40%;
  height: 100%;
  float: left;
  background-color: rgba(182, 110, 20, 0.4);
}
.right {
  width: 50%;
  height: 100%;
  float: right;
  text-align: center;
  line-height: 75px;
}

@media screen and (max-width: 1000px) {
  .contest-show {
    width: 100%;
  }
}
@media screen and (max-width: 650px) {
  .left {
    display: none;
  }
  .right {
    width: 100%;
  }
}
</style>
