<template>
  <div class="contest-card">
    <el-card class="content">
      <template #header>
        <div class="header">
          <span>近期比赛</span>
          <el-button type="text" @click="more">more</el-button>
        </div>
      </template>
      <el-card
        shadow="hover"
        class="container"
        v-for="item in Data"
        :key="item.contest_id"
        @click="linkTo(item.contest_id.toString())"
      >
        <template #header>
          <div class="content-header">
            <span>{{ item.contest_title }}</span>
            <el-tag type="success" size="mini" class="content-tag">{{
              filter_status_data[item.contest_type].text
            }}</el-tag>
          </div>
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

<script lang="ts" setup>
import { useRouter } from "vue-router";

let router = useRouter();

let props = defineProps({
  Data: {
    type: undefined,
    default: [
      {
        contest_id: 1,
        contest_title: "Hello",
        begin_time: "2000-01-01 08:00:00",
        end_time: "2000-01-01 08:00:00",
        contest_type: 0,
        contest_creator: "LiSoul",
        contest_status: "比赛中",
      },
    ],
  },
});

let more = () => {
  router.push({
    path: "contestlist",
  });
};
let linkTo = (val: string) => {
  router.push({
    path: "/contestshow/",
    query: {
      contest_id: val,
    },
  });
};

let filter_status_data: any = [
  { text: "公开", value: 0 },
  { text: "私有", value: 1 },
  { text: "作业", value: 2 },
  { text: "竞赛", value: 3 },
];
</script>

<style lang="scss">
.contest-card {
  .el-card__body {
    padding: 0;
  }
  .el-card__header {
    padding: 0;
  }
}
</style>

<style scoped lang="scss">
.contest-card {
  width: 100%;
  .content {
    width: 100%;
    min-height: 400px;
    margin: 20px 0;
    position: relative;
    border-radius: 20px;
    .header {
      height: 50px;
      line-height: 50px;
      position: relative;
      font-weight: 800;
      padding: 0 20px;
      .el-button {
        position: absolute;
        right: 20px;
        top: 6px;
      }
    }
    .container {
      width: 45%;
      margin: 15px 0;
      min-height: 120px;
      position: relative;
      .content-header {
        height: 40px;
        line-height: 40px;
        font-size: 16px;
        padding: 0 20px;
        position: relative;
        // background-color: #606060;
        .content-tag {
          position: absolute;
          right: 20px;
          top: 10px;
        }
      }
      .container-text {
        font-size: 8px;
        height: 100%;
        width: 95%;
        margin: 0 auto;
        p {
          line-height: 40px;
          span:last-child {
            float: right;
          }
        }
      }
    }
    .container:nth-child(2n-1) {
      float: left;
      margin-left: 3%;
    }
    .container:nth-child(2n) {
      float: right;
      margin-right: 3%;
    }
  }
}
</style>
