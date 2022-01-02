<template>
  <div class="work">
    <div class="nav">
      <div
        class="nav-item"
        v-for="(item, index) in task_data.problem_content"
        :key="index"
        :class="{
          activate: index === cur_problem.id,
          answered: !task_data.real_judger && item.has_done,
          trueanswer:
            task_data.real_judger && item.has_done && item.judger_result,
          erroranswer:
            task_data.real_judger && item.has_done && !item.judger_result,
        }"
        @click="problem_change(index)"
      >
        {{ index }}
      </div>
      <div class="bottom-button">
        <el-button type="success" @click="submit()">提交</el-button>
      </div>
    </div>
    <div class="main">
      <div class="header">
        <div class="title">{{ task_data.title }}</div>
        <div class="subhead">
          <p>
            题量: <span>{{ task_data.problem_content.length }}</span>
          </p>
          <p>
            满分: <span>{{ task_data.aggregate_score }}</span>
          </p>
          <p>
            创建者: <span>{{ task_data.creater }}</span>
          </p>
          <p>
            作答时间:
            <span>{{ task_data.begin_time }}-{{ task_data.end_time }}</span>
          </p>
        </div>
      </div>
      <div class="content">
        <div class="problem-title">
          {{ cur_problem.value.title
          }}<span>({{ cur_problem.value.score }}分)</span>
        </div>
        <div class="choice" v-if="[0, 1].includes(cur_problem.value.type)">
          <div
            class="choice-item"
            v-for="(item, index) in cur_problem.value.answer"
            :key="index"
          >
            <el-radio
              v-if="cur_problem.value.type === 0"
              v-model="cur_problem.value.user_answer"
              :label="index"
              >{{ String.fromCharCode(index + 65) }}</el-radio
            >
            <el-checkbox
              v-else-if="cur_problem.value.type === 1"
              v-model="item.user_answer"
              >{{ String.fromCharCode(index + 65) }}</el-checkbox
            >、
            <span>{{ item.content }}</span>
          </div>
        </div>
        <div class="answer" v-else-if="[2, 4].includes(cur_problem.value.type)">
          <el-input
            type="textarea"
            label="答案"
            v-model="cur_problem.value.user_answer"
          ></el-input>
        </div>
        <div class="judger" v-else-if="[3].includes(cur_problem.value.type)">
          <el-radio :label="true" v-model="cur_problem.value.user_answer"
            >对</el-radio
          >
          <el-radio :label="false" v-model="cur_problem.value.user_answer"
            >错</el-radio
          >
        </div>
        <div v-show="task_data.real_judger && cur_problem.value.has_done">
          <div class="point">
            知识点: <span>{{ cur_problem.value.knowledge_point }}</span>
          </div>
          <div class="degree">
            难度系数: <span>{{ cur_problem.value.degree }}</span>
          </div>
          <div class="analyze">
            答案解析: <span>{{ cur_problem.value.answer_analyze }}</span>
          </div>
        </div>
        <div
          class="other"
          v-show="task_data.real_judger && cur_problem.value.has_done"
        >
          得分:
          <el-input-number
            v-model="cur_problem.value.user_score"
            v-if="task_data.judger_problem"
          ></el-input-number
          ><span v-else>{{ cur_problem.value.user_score }}分</span>
        </div>
      </div>
      <div class="bottom-button">
        <el-button
          type="primary"
          @click="problem_change(cur_problem.id - 1)"
          v-show="cur_problem.id !== 0"
          >上一题</el-button
        >
        <el-button
          type="primary"
          @click="problem_change(cur_problem.id + 1)"
          v-show="cur_problem.id !== task_data.problem_content.length - 1"
          >下一题</el-button
        >
        <el-button type="primary" @click="saveOneProblem()">保存</el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ElLoading, ElMessage } from "element-plus";
import { onMounted, ref } from "vue";
import { submitAnswerData } from "@/api/course";
import { getOneTask } from "@/api/course";
import { useRoute, useRouter } from "vue-router";
import dayJS from "dayjs";

let route = useRoute();
let router = useRouter();

// 显示在窗格中的问题
let cur_problem = ref({
  id: 0,
  value: <any>{},
});

// 总数据
let task_data = ref({
  task_id: 0,
  title: <string>"金华职业技术学院第一次期末考试",
  aggregate_score: <number>100,
  user_score: 0,
  judger_problem: false,
  real_judger: false,
  creater: "梅老师",
  begin_time: "2020-01-01 12:00",
  end_time: "2021-01-01 12:00",
  answer_time: 60,
  problem_content: <any>[
    {
      title: <string>"下列选项中正确的是()?",
      type: <number>0,
      score: <number>5,
      answer: <any>[
        {
          content: <string>"此选项为选项一",
          true_answer: <boolean>false,
          user_answer: false,
        },
        {
          content: <string>"此选项为选项二",
          true_answer: <boolean>false,
          user_answer: false,
        },
        {
          content: <string>"此选项为选项三",
          true_answer: <boolean>false,
          user_answer: false,
        },
        {
          content: <string>"此选项为选项四",
          true_answer: <boolean>false,
          user_answer: false,
        },
      ],
      choice_answer: <number>0,
      user_answer: <number | string | boolean>"",
      answer_analyze: <string>"",
      degree: <number>0,
      knowledge_point: [],
      has_done: false,
      judger_result: "",
      user_score: 0,
    },
  ],
});

let problem_change = (val: number) => {
  // console.log(val);
  cur_problem.value.id = val;
  cur_problem.value.value = task_data.value.problem_content[val];
};

// 检查单条问题是否正确
let checkOneProblem = (val: any) => {
  console.log(val);
  if (val.type === 0) {
    console.log(val.user_answer, val.choice_answer);
    return val.user_answer === val.choice_answer;
  } else if (val.type === 1) {
    val.answer.forEach((res: any) => {
      if (res.user_answer !== res.true_answer) {
        return false;
      }
    });
    return true;
  } else if (val.type === 3) {
    return val.user_answer === val.answer;
  } else {
    return false;
  }
};

// 计算总分
let getAggregateScore = () => {
  let score = 0;
  task_data.value.problem_content.forEach((item: any) => {
    score += item.user_score;
  });
  return score;
};

// 单条数据保存
let saveOneProblem = () => {
  if (checkOneProblem(cur_problem.value.value)) {
    cur_problem.value.value.judger_result = true;
    cur_problem.value.value.user_score = cur_problem.value.value.score;
  } else {
    cur_problem.value.value.judger_result = false;
    cur_problem.value.value.user_score = 0;
  }
  cur_problem.value.value.has_done = true;
};

// 提交数据
let submit = async () => {
  task_data.value.user_score = getAggregateScore();
  let back_data = await submitAnswerData({
    task_id: task_data.value.task_id,
    user_score: task_data.value.user_score,
    problem_content: JSON.stringify(task_data.value.problem_content),
    task_type: route.query.task_type || 0,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};

// 格式化作业数据
let formatTaskData = (val: any) => {
  return {
    task_id: val.task_id,
    title: <string>val.task_title,
    aggregate_score: <number>val.total_score,
    user_score: 0,
    judger_problem: true, // 是否判题界面
    real_judger: val.task_type === 0, // 是否实时判题
    creater: val.creator_name,
    begin_time: dayJS(val.begin_time).format("YYYY-MM-DD HH:mm:ss"),
    end_time: dayJS(val.end_time).format("YYYY-MM-DD HH:mm:ss"),
    answer_time: 60,
    problem_content: val.question_list.map((res: any) => ({
      title: <string>res.question_description,
      type: <number>res.question_type,
      score: <number>5,
      answer: [0, 1].includes(res.question_type)
        ? res.question_option.map((res2: any) => ({
            content: <string>res2.content,
            true_answer: <boolean>res2.true_answer,
            user_answer: false,
          }))
        : res.question_option,
      choice_answer: <number>res.choice_answer,
      user_answer: <number | string | boolean>"",
      answer_analyze: <string>res.question_explanation,
      degree: <number>res.question_difficulty,
      knowledge_point: res.question_tag || [],
      has_done: false, // 题目是否已做
      judger_result: "",
      user_score: 0,
    })),
  };
};

// 获取作业数据
let getTaskData = async (val: number) => {
  console.log(val);
  let loading = ElLoading.service({
    lock: true,
    background: "rgba(0,0,0,0.6)",
    text: "加载中....",
  });
  let back_data = await getOneTask({ task_id: val, is_see: false });
  console.log(back_data);
  if (back_data.status) {
    task_data.value = formatTaskData(back_data.message);
    problem_change(0);
    loading.close();
  } else {
    loading.close();
  }
};

// 挂在数据
onMounted(() => {
  getTaskData(Number(route.query.task_id));
  problem_change(0);
});
</script>

<style scoped lang="scss">
.work {
  width: 80%;
  min-width: 800px;
  max-width: 1600px;
  display: flex;
  margin: 40px auto;
  .nav {
    width: 202px;
    min-height: 300px;
    overflow-y: auto;
    border: 1px solid #aaaaaa;
    border-radius: 10px;
    position: relative;
    // background: rgba(25, 200, 12, 0.4);
    .nav-item {
      width: 28px;
      height: 28px;
      text-align: center;
      line-height: 28px;
      margin: 5px;
      float: left;
      border-radius: 10px;
      border: 1px solid #dddddd;
      cursor: pointer;
    }
    .nav-item.answered {
      background: #81d4fa;
    }
    .nav-item.activate {
      border: 1px solid rgb(150, 0, 250);
    }
    .nav-item.trueanswer {
      background: rgb(0, 200, 20);
    }
    .nav-item.erroranswer {
      background-color: rgb(200, 0, 20);
    }
    .bottom-button {
      width: 100%;
      position: absolute;
      bottom: 20px;
      text-align: center;
    }
  }
  .main {
    width: calc(100% - 222px);
    margin-left: 20px;
    // background: rgba(128, 66, 30, 0.5);
    border: 1px solid #999999;
    border-radius: 20px;
    .header {
      text-align: center;
      padding: 20px;
      border-bottom: 1px dotted #999999;
      .title {
        font-size: 20px;
        font-weight: bold;
      }
      .subhead {
        font-size: 16px;
        color: #666666;
        display: flex;
        justify-content: center;
        margin-top: 15px;
        p {
          margin: 0 10px;
          span {
            margin: 3px;
          }
        }
      }
    }
    .content {
      padding: 20px;
      line-height: 20px;
      position: relative;
      .problem-title {
        font-size: 18px;
        span {
          color: #666666;
          margin-left: 5px;
        }
      }
      .choice {
        .choice-item {
          .el-radio {
            margin-right: 0;
          }
        }
      }
      .answer {
        margin-top: 20px;
      }
      .judger {
        margin-top: 20px;
      }
      .point {
        margin-top: 50px;
        border-top: 1px dotted #dddddd;
      }
      .degree {
        margin-top: 10px;
      }
      .analyze {
        margin-top: 10px;
      }
      .other {
        position: absolute;
        top: 10px;
        right: 10px;
      }
    }
    .bottom-button {
      height: 60px;
      line-height: 60px;
      text-align: center;
    }
  }
}
</style>
