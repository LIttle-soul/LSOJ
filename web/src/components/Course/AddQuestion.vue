<template>
  <div class="homework-main">
    <div class="header">
      <div class="left">
        <div class="title">标题</div>
        <div class="input"><el-input v-model="form_data.title"></el-input></div>
        <div class="setting">
          <el-button type="text" @click="page.setting = true">设置</el-button>
        </div>
      </div>
      <div class="right">
        <el-button type="info" @click="showTaskData">预览</el-button>
        <el-button type="primary" @click="addTask">保存并返回</el-button>
      </div>
    </div>
    <div class="main">
      <div class="left-nav">
        <div class="nav-header">
          <div class="total">
            题量: <span>{{ form_data.problem_content.length }}</span>
          </div>
          <div class="score">
            总分: <span>{{ form_data.aggregate_score }}</span>
          </div>
        </div>
        <div class="nav-content">
          <div
            class="problem-list"
            v-for="(item, index) in form_data.problem_content"
            :key="index"
          >
            <div class="left" @click="switchToProblem(index)">
              {{ problem_type[item.type] }}-{{ index + 1 }}
            </div>
            <div class="right">
              <el-button
                type="text"
                @click="handleUpSwitch(index)"
                v-show="index !== 0"
                ><el-icon><i class="bi bi-arrow-up-short"></i></el-icon
              ></el-button>
              <el-button
                type="text"
                @click="handleDownSwitch(index)"
                v-show="index !== form_data.problem_content.length - 1"
                ><el-icon><i class="bi bi-arrow-down-short"></i></el-icon
              ></el-button>
              <el-button type="text" @click="handleDelete(index)"
                ><el-icon><i class="bi bi-trash"></i></el-icon
              ></el-button>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <div class="content-header">
          <div class="left">
            <el-button type="info" @click="addProblem(0)">单选题</el-button>
            <el-button type="info" @click="addProblem(1)">多选题</el-button>
            <el-button type="info" @click="addProblem(2)">填空题</el-button>
            <el-button type="info" @click="addProblem(3)">判断题</el-button>
            <el-button type="info" @click="addProblem(4)">简答题</el-button>
          </div>
          <div class="right">
            <el-button type="info" @click="autoAddProblem">智能导入</el-button>
            <el-button type="info" @click="choiceByProblemList"
              >题库选题</el-button
            >
          </div>
        </div>
        <div class="content-main">
          <div class="problem-score">
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="分值">
                <el-input-number
                  v-model="page.cur_problem.value.score"
                ></el-input-number>
                <span>{{ page.cur_problem.id }}</span>
              </el-form-item>
            </el-form>
          </div>
          <div class="problem-title">
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="题干">
                <el-input
                  type="textarea"
                  v-model="page.cur_problem.value.title"
                  :rows="5"
                ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div
            class="problem-choice"
            v-if="[0, 1].includes(page.cur_problem.value.type)"
          >
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="选项"
                ><span style="color: red">在此勾选的为正确答案</span
                ><el-button
                  type="text"
                  style="margin-left: 20px"
                  @click="addChoice(true)"
                  >增加选项</el-button
                ><el-button
                  type="text"
                  style="margin-left: 20px"
                  @click="addChoice(false)"
                  >删除选项</el-button
                ></el-form-item
              >
              <el-form-item
                label=""
                v-for="(item, index) in page.cur_problem.value.answer"
                :key="index"
              >
                <template #label>
                  <div>
                    <el-radio
                      v-if="page.cur_problem.value.type === 0"
                      v-model="page.cur_problem.value.choice_answer"
                      :label="index"
                      >{{ String.fromCharCode(index + 65) }}</el-radio
                    >
                    <el-checkbox
                      v-else-if="page.cur_problem.value.type === 1"
                      v-model="item.true_answer"
                      >{{ String.fromCharCode(index + 65) }}</el-checkbox
                    >
                  </div>
                </template>
                <el-input
                  type="textarea"
                  v-model="item.content"
                  :rows="2"
                ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div
            class="problem-answer"
            v-else-if="[2, 4].includes(page.cur_problem.value.type)"
          >
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="答案">
                <el-input
                  type="textarea"
                  v-model="page.cur_problem.value.answer"
                  :rows="3"
                ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div
            class="problem-judger"
            v-else-if="[3].includes(page.cur_problem.value.type)"
          >
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="答案">
                <el-switch
                  v-model="page.cur_problem.value.answer"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                />
              </el-form-item>
            </el-form>
          </div>
          <div class="problem-analyze">
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="答案解析">
                <el-input
                  type="textarea"
                  v-model="page.cur_problem.value.answer_analyze"
                  :rows="3"
                ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="problem-dgree">
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="难度">
                <el-slider
                  v-model="page.cur_problem.value.degree"
                  :min="0"
                  :max="10"
                  style="max-width: 200px"
                ></el-slider>
              </el-form-item>
            </el-form>
          </div>
          <div class="problem-point">
            <el-form
              label-width="80px"
              style="margin-right: 20px; margin-top: 20px"
            >
              <el-form-item label="知识点">
                <el-select
                  v-model="page.cur_problem.value.knowledge_point"
                  multiple
                  filterable
                  allow-create
                  default-first-option
                  placeholder="请选择知识点"
                >
                  <el-option
                    v-for="(item, index) in page.point_list"
                    :key="index"
                    :label="item"
                    :value="item"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
          <div class="bottom-button">
            <el-button type="success" @click="saveProblem">保存该题</el-button>
            <el-button type="danger" @click="resetProblem">重置</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ElLoading, ElMessage } from "element-plus";
import { ref } from "vue";
import { addTaskData } from "@/api/course";
import { useRoute, useRouter } from "vue-router";

let route = useRoute();
let router = useRouter();

let problem_type = ["单选题", "多选题", "填空题", "判断题", "简答题"];

let form_data = ref({
  title: <string>"",
  aggregate_score: <number>100,
  problem_content: <any>[
    {
      title: <string>"",
      type: <number>0,
      score: <number>5,
      answer: <any>[
        {
          content: <string>"",
        },
        {
          content: <string>"",
        },
        {
          content: <string>"",
        },
        {
          content: <string>"",
        },
      ],
      choice_answer: <number>0,
      answer_analyze: <string>"",
      degree: <number>0,
      knowledge_point: [],
    },
  ],
});
let page = ref({
  setting: false,
  cur_problem: {
    id: 0,
    value: <any>{
      title: <string>"",
      type: <number>0,
      score: <number>5,
      answer: <any>[
        {
          content: <string>"",
          true_answer: <boolean>false,
        },
        {
          content: <string>"",
          true_answer: <boolean>false,
        },
        {
          content: <string>"",
          true_answer: <boolean>false,
        },
        {
          content: <string>"",
          true_answer: <boolean>false,
        },
      ],
      choice_answer: <number>0,
      answer_analyze: <string>"",
      degree: <number>0,
      knowledge_point: [],
    },
  },
  point_list: [],
});

let probelm_temp = ref({
  choice: {
    title: <string>"",
    type: <number>0,
    score: <number>5,
    answer: <any>[
      {
        content: <string>"",
        true_answer: <boolean>false,
      },
      {
        content: <string>"",
        true_answer: <boolean>false,
      },
      {
        content: <string>"",
        true_answer: <boolean>false,
      },
      {
        content: <string>"",
        true_answer: <boolean>false,
      },
    ],
    choice_answer: <number>0,
    answer_analyze: <string>"",
    degree: <number>0,
    knowledge_point: [],
  },
  judger: {
    title: <string>"",
    type: <number>3,
    score: <number>5,
    answer: <boolean>false,
    choice_answer: <number>0,
    answer_analyze: <string>"",
    degree: <number>0,
    knowledge_point: [],
  },
  answer: {
    title: <string>"",
    type: <number>2,
    score: <number>5,
    answer: <string>"",
    choice_answer: <number>0,
    answer_analyze: <string>"",
    degree: <number>0,
    knowledge_point: [],
  },
});

// 计算总分
let getAggregateScore = () => {
  let score = 0;
  form_data.value.problem_content.forEach((item: any) => {
    score += item.score;
  });
  return score;
};

// 跳转到题目
let switchToProblem = (val: number) => {
  page.value.cur_problem.id = val;
  page.value.cur_problem.value = form_data.value.problem_content[val];
};

// 添加题目
let addProblem = (val: number) => {
  let temp = <any>{};
  console.log(probelm_temp.value);
  if ([0, 1].includes(val)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.choice));
  } else if ([2, 4].includes(val)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.answer));
  } else if ([3].includes(val)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.judger));
  }
  temp.type = val;
  page.value.cur_problem.id = form_data.value.problem_content.length;
  page.value.cur_problem.value = temp;
  form_data.value.problem_content.push(temp);
};
let autoAddProblem = () => {
  console.log("智能导入");
};
let choiceByProblemList = () => {
  console.log("题库选题");
};

// 题目排序
let handleUpSwitch = (val: number) => {
  //   console.log("上移");
  [
    form_data.value.problem_content[val],
    form_data.value.problem_content[val - 1],
  ] = [
    form_data.value.problem_content[val - 1],
    form_data.value.problem_content[val],
  ];
};
let handleDownSwitch = (val: number) => {
  //   console.log("下移");
  [
    form_data.value.problem_content[val],
    form_data.value.problem_content[val + 1],
  ] = [
    form_data.value.problem_content[val + 1],
    form_data.value.problem_content[val],
  ];
};
let handleDelete = (val: number) => {
  //   console.log("删除");
  form_data.value.problem_content.splice(val, 1);
};

// 选项添加
let addChoice = (val: boolean) => {
  if (val) {
    page.value.cur_problem.value.answer.push({
      content: <string>"",
      true_answer: <boolean>false,
    });
  } else {
    page.value.cur_problem.value.answer.pop();
  }
};

// 保存题目
let saveProblem = () => {
  form_data.value.problem_content[page.value.cur_problem.id] =
    page.value.cur_problem.value;
  form_data.value.aggregate_score = getAggregateScore();
  ElMessage({
    type: "success",
    message: "保存成功",
  });
};
// 重置题目
let resetProblem = () => {
  let temp = <any>{};
  if ([0, 1].includes(page.value.cur_problem.value.type)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.choice));
  } else if ([2, 4].includes(page.value.cur_problem.value.type)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.answer));
  } else if ([3].includes(page.value.cur_problem.value.type)) {
    temp = JSON.parse(JSON.stringify(probelm_temp.value.judger));
  }
  temp.type = page.value.cur_problem.value.type;
  page.value.cur_problem.value = temp;
};
// 预览题单
let showTaskData = () => {
  console.log("题单展示");
};
// 提交题单
let addTask = async () => {
  let back_data = await addTaskData({
    course_id: 1,
    task_title: form_data.value.title,
    task_type: 0,
    total_score: form_data.value.aggregate_score,
    problem_content: JSON.stringify(form_data.value.problem_content),
  });
  console.log(back_data);
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    router.push({
      path: "/joblibrary",
      query: {
        course_id: route.query.course_id,
      },
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
</script>
<style lang="scss" scoped>
.homework-main {
  width: 100%;
  max-width: 1600px;
  margin: 20px auto;
  //   background: rgba(120, 120, 120, 0.6);
  .header {
    width: 100%;
    height: 60px;
    border-bottom: 5px solid #555555;
    margin-bottom: 10px;
    .left {
      height: 60px;
      line-height: 60px;
      display: flex;
      float: left;
      margin-left: 30px;
      .title {
        font-size: 30px;
        margin-right: 10px;
      }
      .setting {
        margin-left: 20px;
        font-size: 20px;
      }
    }
    .right {
      height: 60px;
      line-height: 60px;
      float: right;
      margin-right: 30px;
    }
  }
  .main {
    width: 100%;
    min-height: 600px;

    .left-nav {
      width: 300px;
      min-height: 600px;
      max-height: 800px;
      float: left;
      border: 1px solid #000000;
      border-radius: 10px;
      overflow: hidden;
      .nav-header {
        height: 40px;
        line-height: 40px;
        display: flex;
        justify-content: space-around;
        font-size: 20px;
        border-bottom: 1px solid #000000;
        span {
          color: #ff0000;
          margin-left: 5px;
        }
      }
      .nav-content {
        min-height: 560px;
        max-height: 760px;
        overflow-y: auto;
        .problem-list {
          height: 40px;
          line-height: 40px;
          background-color: #dddddd;
          display: flex;
          justify-content: space-between;
          .left {
            margin-left: 20px;
            cursor: pointer;
          }
          .right {
            margin-right: 20px;
            i {
              font-size: 20px;
            }
          }
        }
      }
    }
    .content {
      width: calc(100% - 350px);
      float: right;
      min-height: 600px;
      border: 1px solid #000000;
      border-radius: 20px;
      .content-header {
        width: 100%;
        height: 60px;
        line-height: 60px;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #000000;
        .left {
          margin-left: 20px;
        }
        .right {
          margin-right: 20px;
        }
      }
      .content-main {
        width: 100%;
        min-height: 500px;
        .problem-score {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-title {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-choice {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-answer {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-judger {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-analyze {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-dgree {
          width: 100%;
          border-bottom: 1px dotted #555555;
        }
        .problem-point {
          width: 100%;
          // border-bottom: 1px dotted #555555;
        }
        .bottom-button {
          width: 100%;
          height: 80px;
          line-height: 80px;
          text-align: center;
        }
      }
    }
  }
}
</style>
