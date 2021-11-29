<template>
  <div class="count-down">
    <p class="itemss">
      <span>{{ text }}</span>
    </p>
    <p class="itemss">
      <span>{{ timer.day }}天</span>
      <span>{{ timer.hour }}时</span>
      <span>{{ timer.minute }}分</span>
      <span>{{ timer.second }}秒</span>
    </p>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";

let props = defineProps({
  text: {
    type: String,
    default: "距离比赛开始还有",
  },
  endTime: {
    type: String,
  },
});

let emit = defineEmits(["time-end"]);

let timer = reactive({
  day: 0,
  hour: 0,
  minute: 0,
  second: 0,
  flag: false,
});

onMounted(() => {
  let time = setInterval(() => {
    if (timer.flag == true) {
      clearInterval(time);
    }
    timeDown();
  }, 1000);
});

let timeDown = () => {
  let endTime = new Date(<string>props.endTime);
  let nowTime = new Date();
  let leftTime = parseInt(
    ((endTime.getTime() - nowTime.getTime()) / 1000).toString()
  );
  let d = parseInt((leftTime / (24 * 60 * 60)).toString());
  let h = parseInt(((leftTime / (60 * 60)) % 24).toString());
  let m = parseInt(((leftTime / 60) % 60).toString());
  let s = parseInt((leftTime % 60).toString());
  if (leftTime <= 0) {
    timer.day = 0; //天
    timer.hour = 0; //时
    timer.minute = 0; //分
    timer.second = 0; //秒
    timer.flag = true;
    emit("time-end");
  } else {
    timer.day = d; //天
    timer.hour = h; //时
    timer.minute = m; //分
    timer.second = s; //秒
  }
};
let formate = (time: number) => {
  if (time >= 10) {
    return time;
  } else {
    return `0${time}`;
  }
};
</script>

<style scoped lang="scss">
.count-down {
  width: 100%;
  .itemss {
    width: 100%;
    text-align: center;
    span {
      line-height: 70px;
      font-size: 2.4em;
      font-family: "楷体";
      font-weight: bold;
      color: tomato;
    }
  }
}
</style>
