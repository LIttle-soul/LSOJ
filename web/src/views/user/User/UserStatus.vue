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
        id="main_mychart"
        :style="{ width: '400px', height: '400px' }"
      ></div>
    </div>
    <el-card class="context">
      <a v-for="item in solved_data" :key="item.problem_id" href="#" class="text">
        {{ item.problem_id }}({{ item.count }})
      </a>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import { getUserStatus } from "@/api/user";
import { ElLoading, ElMessage } from "element-plus";
import * as ECharts from "echarts";
import { useRoute } from "vue-router";

let route = useRoute();

let user_info = ref({
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
});
let solved_data = ref([
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
]);

let setData = async (user_id: string) => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading....",
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
    user_info.value = {
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
    solved_data.value = [];
    for (var item in temp.solved_data) {
      solved_data.value.push({
        problem_id: Number(item),
        count: temp.solved_data[Number(item)],
      });
    }
    echartsInit();
    loading.close();
  } else {
    loading.close();
    ElMessage({
      type: "error",
      message: val.message,
    });
  }
};

// 图表事件处理
type EChartsOption = ECharts.EChartsOption;
var chartDom: HTMLElement;
var myChart: ECharts.ECharts;
var option: EChartsOption;
let echartsInit = () => {
  //柱形图
  //因为初始化echarts 的时候，需要指定的容器 id='main'
  option = {
    title: {
      text: "我的状态",
      subtext: user_info.value.user_id.value,
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
          user_info.value.user_accurate,
          user_info.value.format_error,
          user_info.value.wrong_answer,
          user_info.value.time_over,
          user_info.value.memory_over,
          user_info.value.output_over,
          user_info.value.runtime_error,
          user_info.value.compile_error,
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
  };
  myChart.setOption(option);
};

onMounted(() => {
  chartDom = <HTMLElement>document.getElementById("main_mychart");
  myChart = ECharts.init(chartDom);
  setData(<string>route.params.user_id);
});
</script>

<style scoped lang="scss">
.user-status {
  width: 80%;
  margin: 80px auto;
  .el-card {
    border-radius: 25px;
  }
  .header {
    margin-bottom: 80px;
    display: flex;
    justify-content: space-around;
    .lefter {
      width: 40%;
      min-width: 360px;
      height: 400px;
      p {
        font-size: 22px;
        line-height: 25px;
        font-family: "楷体";
      }
    }
    .righter {
      width: 40%;
      min-width: 360px;
      height: 400px;
      padding-top: 40px;
      /* background-color: aqua; */
    }
  }
  .context {
    width: 100%;
    a {
      margin: 0 5px;
    }
  }
}
</style>
