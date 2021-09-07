<template>
  <div class="problem-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="problem_form">
        <el-form-item label="题目标题">
          <el-input v-model="problem_form.problem_title"></el-input>
        </el-form-item>
        <el-form-item label="时间限制">
          <el-input-number v-model="problem_form.time_limit"></el-input-number
          ><span class="problem-span">MS</span>
        </el-form-item>
        <el-form-item label="内存限制">
          <el-input-number v-model="problem_form.memory_limit"></el-input-number
          ><span class="problem-span">MB</span>
        </el-form-item>
        <el-form-item label="题目来源">
          <el-input v-model="problem_form.problem_course"></el-input>
        </el-form-item>
        <el-form-item label="题目标签">
          <el-select v-model="problem_form.problem_tag" multiple placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.value"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="题目难度">
          <el-rate
            v-model="problem_form.problem_difficult"
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            :show-score="false"
          >
          </el-rate>
        </el-form-item>
        <el-form-item label="题目特判">
          <el-switch
            v-model="problem_form.problem_spj"
            active-color="#13ce66"
            inactive-color="#00000033"
          ></el-switch>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">题目内容</span>
          <el-button class="button" type="text" @click="changeProblem=!changeProblem">修改内容</el-button>
        </div>
      </template>
      <ProblemChild mode="preview" :content="problem_form.problem_content" :key="new Date().getTime()" />
    </el-card>
    <el-dialog
    title="内容编辑"
    v-model="changeProblem"
    width="90%"
    top="60px"
    center>
        <ProblemChild height="800px" :content="problem_form.problem_content" @getContent="getContent"/>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import ProblemChild from '@/components/Editor/MarkdownEditor.vue';
import ProblemModel from '@/assets/markdown/问题模板.md';

export default {
  components: {
    ProblemChild
  },
  setup() {},
  data() {
    return {
        changeProblem: false,
      iconClasses: ["icon-rate-face-1", "icon-rate-face-2", "icon-rate-face-3"],
      options: [
          {value: '线性结构'},
          {value: '树性结构'},
          {value: '堆'},
          {value: '图'},
          {value: '排序算法'},
          {value: '动态规划'},
          {value: '贪心算法'},
          {value: '搜索'},
          {value: '字符串'},
          {value: '基础联系'},
          {value: '数论'},
      ],
      problem_form: {
        problem_title: "",
        problem_content: ProblemModel,
        problem_spj: false,
        problem_course: "",
        time_limit: 1000,
        memory_limit: 128,
        problem_tag: [],
        problem_difficult: null,
      },
    };
  },
  methods: {
      getContent(text){
        this.problem_form.problem_content = text;
      }
  }
};
</script>

<style>
.problem-add {
  width: 90%;
  margin: 40px auto;
}
.problem-add .el-input {
  max-width: 500px;
}
.problem-add .el-card {
  margin: 20px 0;
}
.problem-add .el-card .el-form-item:nth-child(2) .el-input-number__decrease,
.problem-add .el-card .el-form-item:nth-child(2) .el-input-number__increase {
  transform: translateY(1px);
}
.problem-add .el-card .el-form-item:nth-child(3) .el-input-number__decrease,
.problem-add .el-card .el-form-item:nth-child(3) .el-input-number__increase {
  transform: translateY(1px);
}
.problem-span {
  font-size: 18px;
  font-weight: 800;
  margin-left: 20px;
}
.problem-add .el-card__header {
  height: 60px;
  padding: 0 40px;
}
.problem-add .el-rate {
  height: 100%;
  line-height: 100%;
}
.problem-add .el-rate i {
  margin-top: 11px;
}
.problem-add .card-header {
  justify-content: space-between;
  align-items: center;
}
.problem-add .title {
  float: left;
  /* background-color: rgba(15, 105, 214, 0.2); */
  width: 100px;
  height: 60px;
  line-height: 60px;
  font-size: 20px;
  font-weight: 800;
  font-family: "宋体";
}
.problem-add .button {
  float: right;
  width: 60px;
  height: 60px;
}
</style>
