<template>
  <div class="user-status">
    <div class="header">
      <el-card class="lefter" :body-style="{ 'border-radius':'5px'}">
        <p v-for="item in user_info" :key="item.name">
          {{ item.name }}: {{ item.value }}
        </p>
      </el-card>
      <div class="center"></div>
      <div
        class="righter"
        id="user_status_echart"
        :style="{ width: '400px', height: '400px' }"
      ></div>
      
    </div>
    <el-card class="context">
      <a v-for="item in solved_data" :key="item.problem_id" href="#" class="text">
        {{ item.problem_id }}({{ item.count}})
      </a>
    </el-card>
  </div>
</template>

<script>
export default {
  setup() {},
  mounted() {
    this.setData(this.$route.params.user_id);
    this.echartsInit();
  },
  data() {
    return {
      user_info: {
        user_id: { name: "账号", value: "201910101600040" },
        user_nick: { name: "昵称", value: "LiSoul" },
        // user_rank: { name: "排名", value: 1 },
        user_solved: { name: "解决", value: 520 },
        user_submit: { name: "提交", value: 1314 },
        user_accurate: { name: "正确", value: 256 },
        format_error: { name: "格式错误", value: 5 },
        wrong_answer: { name: "答案错误", value: 25 },
        time_over: { name: "时间超限", value: 18 },
        memory_over: { name: "内存超限", value: 16 },
        output_over: { name: "输出超限", value: 28 },
        runtime_error: { name: "运行错误", value: 8 },
        compile_error: { name: "编译错误", value: 1 },
        user_school: { name: "学校", value: "金华职业技术学院" },
      },
      solved_data: [
        {
          problem_id: 1000,
          count: 1,
        },
        {
          problem_id: 1001,
          count: 2,
        },
        {
          problem_id: 1003,
          count: 1,
        },
        {
          problem_id: 1004,
          count: 1,
        },
      ],
    };
  },
  methods: {
    setData(user_id) {
      let val = this.$store.getters.getUserDataByUserId(user_id);
      // console.log(val);
      this.user_info.user_id.value = val.user_id;
      this.user_info.user_nick.value = val.user_nick;
      // this.user_info.user_rank.value = val.user_solution_data.user_rank;
      this.user_info.user_solved.value = val.user_solution_data.user_solved.length;
      this.user_info.user_submit.value = val.user_solution_data.user_submit;
      this.user_info.user_accurate.value = val.user_solution_data.user_accurate;
      this.user_info.format_error.value = val.user_solution_data.format_error;
      this.user_info.wrong_answer.value = val.user_solution_data.wrong_answer;
      this.user_info.time_over.value = val.user_solution_data.time_over;
      this.user_info.memory_over.value = val.user_solution_data.memory_over;
      this.user_info.output_over.value = val.user_solution_data.output_over;
      this.user_info.runtime_error.value = val.user_solution_data.runtime_error;
      this.user_info.compile_error.value = val.user_solution_data.compile_error;
      this.user_info.user_school.value = val.user_school?val.user_school.school_name:null;
      this.solved_data = val.user_solution_data.user_solved.map(item => ({
        problem_id: item.problem_id,
        count: item.number
      }));
    },
    echartsInit() {
      //柱形图
      //因为初始化echarts 的时候，需要指定的容器 id='main'
      this.$ECharts
        .init(document.getElementById("user_status_echart"))
        .setOption({
          title: {
            text: "我的状态",
            subtext: this.user_info.user_id.value,
            left: "center",
            show: true
          },
          tooltip: {
            trigger: "item",
            show: true
          },
          legend: {
            orient: "vertical",
            left: "right",
          },
          series: [
            {
              name: "我的状态",
              type: "pie",
              radius: "50%",
              data: [
                this.user_info.user_accurate,
                this.user_info.format_error,
                this.user_info.wrong_answer,
                this.user_info.time_over,
                this.user_info.memory_over,
                this.user_info.output_over,
                this.user_info.runtime_error,
                this.user_info.compile_error
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)",
                },
              },
            },
          ],
        });
    },
  },
};
</script>

<style scoped>
.user-status {
  width: 80%;
  margin: 80px auto;
}
.lefter {
  width: 40%;
  min-width: 360px;
  height: 400px;
  float: left;
}
.header {
  margin-bottom: 80PX;
}
.header .el-card {
  border-radius: 25px;
}
.lefter p {
  font-size: 22px;
  line-height: 25px;
  font-family: "楷体";
}
.righter {
  width: 40%;
  min-width: 360px;
  height: 400px;
  float: right;
  padding-top: 40px;
  /* background-color: aqua; */
}
.context {
  width: 100%;
}
.context a {
  margin: 0 5px;
}
</style>
