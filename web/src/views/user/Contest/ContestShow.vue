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
          :text="count_down.text"
          :endTime="count_down.end_time"
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
        <ContestJoin
          :contest_id="contest_form.contest_id"
          @reload="setContestData(Number(route.params.contest_id))"
        />
      </el-dialog>
    </div>
    <el-card class="content">
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

<script lang="ts" setup>
import ContestChild from "@/components/Editor/MarkdownEditor.vue";
import ContestJoin from "@/components/Contest/ContestJoin.vue";
import Times from "@/components/Other/CountDown.vue";
import { useStore, mapGetters, mapState } from "vuex";
import { useRouter, useRoute } from "vue-router";
import { computed, onMounted, ref } from "vue";
import dayJS from "dayjs";
import { ElLoading, ElMessage } from "element-plus";
import { getContestList } from "@/api/contest";

let store = useStore();
let router = useRouter();
let route = useRoute();

let user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);
let contest_data = computed(
  mapState("contest", ["contest_list"]).contest_list.bind({ $store: store })
);
let count_down = ref({
  text: "距离比赛开始还有",
  end_time: "2022-01-01 12:00:00",
});
let contest_power = ref(false);
let button_status = ref(true);
let contest_join = ref(false);
let filter_status_data = [
  { text: "公开", value: 0 },
  { text: "私有", value: 1 },
  { text: "作业", value: 2 },
  { text: "竞赛", value: 3 },
];
let contest_form = ref({
  contest_id: 1,
  contest_title: "竞赛一",
  contest_content: "### Hello the first Contest",
  begin_time: "2022-01-01 12:00:00",
  end_time: "2022-01-01 14:00:00",
  contest_status: "未开始",
  contest_type: 0,
  join_people: 0,
  contest_creator: "LiSoul",
});
let showContestData = (contest_id: any) => {
  router.push("/contestdata/" + contest_id);
};
let joinContest = () => {
  contest_join.value = true;
};
let setContestData = async (val: number) => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getContestList({
    contest_id: val,
  });
  // console.log(back_data);
  if (back_data.status) {
    let temp = back_data.message;
    contest_form.value = {
      contest_id: temp.contest_id,
      contest_title: temp.contest_title,
      contest_content: temp.contest_introduce,
      begin_time: dayJS(temp.start_time).format("YYYY-MM-DD HH:mm:ss"),
      end_time: dayJS(temp.end_time).format("YYYY-MM-DD HH:mm:ss"),
      contest_status: getContestStatus(temp.start_time, temp.end_time),
      contest_type: temp.contest_province,
      join_people: temp.user_list.length,
      contest_creator: temp.contest_creator,
    };
    getContestPower(temp.contest_province, temp.user_list);
    loading.close();
  } else {
    loading.close();
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let getContestStatus = (begin_time: any, end_time: any) => {
  if (dayJS().isBefore(dayJS(begin_time))) {
    button_status.value = false;
    count_down.value.end_time = dayJS(begin_time).format("YYYY-MM-DD HH:mm:ss");
    count_down.value.text = "距离比赛开始还有";
    return "未开始";
  } else if (dayJS().isBefore(dayJS(end_time))) {
    button_status.value = true;
    count_down.value.end_time = dayJS(end_time).format("YYYY-MM-DD HH:mm:ss");
    count_down.value.text = "距离比赛结束还有";
    return "比赛中";
  } else {
    button_status.value = true;
    count_down.value.end_time = dayJS(end_time).format("YYYY-MM-DD HH:mm:ss");
    count_down.value.text = "比赛已结束";
    return "已结束";
  }
};
let getContestPower = (contest_type: any, contest_user: any) => {
  contest_user = contest_user.map((item: any) => {
    return item.user_id;
  });
  if (user_info.value === null || user_info.value === undefined) {
    ElMessage({
      type: "error",
      message: "用户未登录，请先登录",
    });
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } else if (+contest_type === 0) {
    contest_power.value = true;
  } else if (contest_user.includes(user_info.value.user_id)) {
    contest_power.value = true;
  } else {
    contest_power.value = false;
  }
};
let timeEnd = () => {
  if (button_status.value) {
    count_down.value.text = "比赛已结束";
  } else if (!button_status && contest_power.value) {
    count_down.value.text = "距离比赛结束还有";
    count_down.value.end_time = dayJS(contest_form.value.end_time).format(
      "YYYY-MM-DD HH:mm:ss"
    );
  }
};

onMounted(() => {
  setContestData(Number(route.params.contest_id));
});
</script>

<style lang="scss">
.contest-show {
  .left {
    .el-descriptions__body {
      height: 100%;
      font-family: "楷体";
      background-color: unset;
      color: black;
      td {
        margin: 0;
        padding: 0;
        line-height: 29px;
        .el-descriptions__label {
          font-size: 1.2em;
          font-weight: bold;
        }
      }
    }
  }
}
</style>

<style scoped lang="scss">
.contest-show {
  width: 80%;
  margin: 0 auto;
  .card {
    width: 100%;
    margin: 60px 0;
    display: flex;
    justify-content: space-evenly;
    .left {
      width: 40%;
      height: 100%;
      background-color: #eeeeee;
      border-radius: 25px;
      box-shadow: -2px -2px 10px #999999;
    }
    .right {
      width: 40%;
      height: 100%;
      text-align: center;
      line-height: 75px;
      // background-color: aquamarine;
    }
    @media screen and (max-width: 650px) {
      .left {
        display: none;
      }
      .right {
        width: 100%;
      }
    }
  }
  .card:first-child {
    height: 250px;
  }
}

@media screen and (max-width: 1000px) {
  .contest-show {
    width: 100%;
  }
}
</style>
