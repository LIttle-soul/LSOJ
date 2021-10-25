<template>
  <div class="user-status">
    <div class="header">
      <el-card class="lefter" :body-style="{ 'border-radius': '5px' }">
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
      <a
        v-for="item in solved_data"
        :key="item.problem_id"
        href="#"
        class="text"
      >
        {{ item.problem_id }}({{ item.count }})
      </a>
    </el-card>
  </div>
</template>

<script>
import { getUserStatus } from "@/api/user";
import { ElLoading } from "element-plus";

export default {
  setup() {},
  mounted() {
    this.setData(this.$route.params.user_id);
    this.echartsInit();
  },
  watch: {
    user_info() {
      this.echartsInit();
    },
  },
  data() {
    return {
      user_info: {
        user_id: { name: "账号", value: "" },
        user_nick: { name: "昵称", value: "" },
        user_solved: { name: "解决", value: 0 },
        user_submit: { name: "提交", value: 0 },
        user_accurate: { name: "正确", value: 0 },
        format_error: { name: "格式错误", value: 0 },
        wrong_answer: { name: "答案错误", value: 0 },
        time_over: { name: "时间超限", value: 0 },
        memory_over: { name: "内存超限", value: 0 },
        output_over: { name: "输出超限", value: 0 },
        runtime_error: { name: "运行错误", value: 0 },
        compile_error: { name: "编译错误", value: 0 },
        user_school: { name: "学校", value: "" },
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
    async setData(user_id) {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      let val = null;
      if (user_id) {
        val = await getUserStatus({
          user_id: user_id[0],
        });
      } else {
        val = await getUserStatus();
      }
      // console.log(val);
      if (val.status) {
        let temp = val.message;
        this.user_info = {
          user_id: { name: "账号", value: temp.user_id },
          user_nick: { name: "昵称", value: temp.user_nick },
          user_solved: { name: "解决", value: temp.user_solved },
          user_submit: { name: "提交", value: temp.user_submit },
          user_accurate: { name: "正确", value: temp.user_accurate },
          format_error: { name: "格式错误", value: temp.format_error },
          wrong_answer: { name: "答案错误", value: temp.wrong_answer },
          time_over: { name: "时间超限", value: temp.time_over },
          memory_over: { name: "内存超限", value: temp.memory_over },
          output_over: { name: "输出超限", value: temp.output_over },
          runtime_error: { name: "运行错误", value: temp.runtime_error },
          compile_error: { name: "编译错误", value: temp.compile_error },
          user_school: { name: "学校", value: temp.user_school },
        };
        this.solved_data = [];
        for (var item in temp.solved_data) {
          this.solved_data.push({
            problem_id: item,
            count: temp.solved_data[item],
          });
        }
        loading.close();
      }
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
            show: true,
          },
          tooltip: {
            trigger: "item",
            show: true,
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
                this.user_info.compile_error,
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
  margin-bottom: 80px;
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
