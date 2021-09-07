<template>
  <div class="contest-show">
    <div class="card">
      <el-card class="left">
        <el-descriptions :column="1">
            <el-descriptions-item label="竞赛标题">{{contest_form.contest_title}}</el-descriptions-item>
            <el-descriptions-item label="开始时间">{{contest_form.begin_time}}</el-descriptions-item>
            <el-descriptions-item label="比赛时长">{{contest_form.duration}}</el-descriptions-item>
            <el-descriptions-item label="比赛状态">{{contest_form.contest_status}}</el-descriptions-item>
            <el-descriptions-item label="比赛类型">{{contest_form.contest_type}}</el-descriptions-item>
            <el-descriptions-item label="报名人数">{{contest_form.join_people}}</el-descriptions-item>
            <el-descriptions-item label="创建者">{{contest_form.contest_creator}}</el-descriptions-item>
        </el-descriptions>
        </el-card>
        <div class="right">
            <Times :endTime="contest_form.begin_time" class="right-child" />
            <el-button type="primary" size="medium" v-if="contest_form.contest_power">点击进入</el-button>
            <el-button type="primary" size="medium" v-else>点击报名</el-button>
        </div>
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
import Times from "@/components/Other/CountDown.vue";

export default {
  components: {
    ContestChild,
    Times,
  },
  data() {
    return {
      contest_form: {
        contest_id: 1,
        contest_title: "竞赛一",
        contest_content: "### Hello the first Contest",
        begin_time: "2022-01-01 12:00:00",
        contest_status: "未开始",
        contest_type: "竞赛",
        duration: "5小时",
        join_people: 120,
        contest_creator: "LiSoul",
        contest_power: false
      },
    };
  },
};
</script>

<style>
.contest-show .left .el-descriptions__body {
    height: 100%;
    font-family: "楷体";
    background-color:unset;
    color: black;
}
.contest-show .left .el-descriptions__body td{
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
      margin: 60px 0;
    }
    .card {
        margin: 5px 0;
    }
  }
</style>
