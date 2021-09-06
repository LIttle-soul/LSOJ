<template>
  <div class="count-down">
    <p class="itemss">
      <span>距离比赛开始还有</span>
    </p>
    <p class="itemss">
      <span>{{ day }}天</span>
      <span>{{ hour }}时</span>
      <span>{{ minute }}分</span>
      <span>{{ second }}秒</span>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      day: "",
      hour: "",
      minute: "",
      second: "",
      flag: false,
    };
  },
  mounted() {
    let time = setInterval(() => {
      if (this.flag == true) {
        clearInterval(time);
      }
      this.timeDown();
    }, 500);
  },
  props: {
    endTime: {
      type: String,
    },
  },
  methods: {
    timeDown() {
      const endTime = new Date(this.endTime);
      const nowTime = new Date();
      let leftTime = parseInt((endTime.getTime() - nowTime.getTime()) / 1000);
      let d = parseInt(leftTime / (24 * 60 * 60));
      let h = this.formate(parseInt((leftTime / (60 * 60)) % 24));
      let m = this.formate(parseInt((leftTime / 60) % 60));
      let s = this.formate(parseInt(leftTime % 60));
      if (leftTime <= 0) {
        this.flag = true;
        this.$emit("time-end");
      }
      this.day = d; //天
      this.hour = h; //时
      this.minute = m; //分
      this.second = s; //秒
    },
    formate(time) {
      if (time >= 10) {
        return time;
      } else {
        return `0${time}`;
      }
    },
  },
};
</script>

<style scoped>
.count-down {
  width: 100%;
}
.itemss {
  width: 100%;
  text-align: center;
}
.count-down .itemss span {
  line-height: 70px;
  font-size: 2.4em;
  font-family: "楷体";
  font-weight: bold;
  color: tomato;
}
</style>
