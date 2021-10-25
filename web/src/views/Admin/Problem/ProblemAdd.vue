<template>
  <div class="problem-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="problem_form">
        <el-form-item label="题目编号">
          <el-input-number
            v-model="problem_form.problem_id"
            controls-position="right"
          ></el-input-number>
        </el-form-item>
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
          <el-select
            v-model="problem_form.problem_tag"
            :multiple="true"
            placeholder="请选择"
            :filterable="true"
            :allow-create="true"
          >
            <el-option
              v-for="item in problem_tag_list"
              :key="item"
              :label="item"
              :value="item"
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
        <el-form-item label="题目状态">
          <el-switch
            v-model="problem_form.problem_status"
            active-color="#13ce66"
            inactive-color="#00000033"
          ></el-switch>
        </el-form-item>
      </el-form>
      <el-button
        type="primary"
        style="float: right; margin-bottom: 15px;"
        @click="submit"
        >提交</el-button
      >
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">题目内容</span>
          <el-button
            class="button"
            type="text"
            @click="changeProblem = !changeProblem"
            >修改内容</el-button
          >
        </div>
      </template>
      <ProblemChild
        mode="preview"
        :content="problem_form.problem_content"
        :key="new Date().getTime()"
      />
    </el-card>
    <el-dialog
      title="内容编辑"
      v-model="changeProblem"
      width="90%"
      top="60px"
      center
    >
      <ProblemChild
        height="800px"
        :content="problem_form.problem_content"
        @getContent="getContent"
      />
    </el-dialog>
  </div>
</template>

<script lang="js">
import ProblemChild from "@/components/Editor/MarkdownEditor.vue";
import { submitProblemData, changeProblemData } from "@/api/problem";
import { mapState, mapGetters } from "vuex";

export default {
  components: {
    ProblemChild,
  },
  created() {
    this.setData(this.$route.params.problem_id);
  },
  computed: {
    ...mapState("problem", {
      problem_tag_list: state => state.problem_tag_list,
    }),
    ...mapGetters("problem", {
      getProblemData: "getProblemData",
    }),
  },
  data() {
    return {
      changeProblem: false,
      iconClasses: ["icon-rate-face-1", "icon-rate-face-2", "icon-rate-face-3"],
      problem_form: {
        problem_id: 9999,
        problem_title: "",
        problem_content: require("@/assets/markdown/问题模板.md"),
        problem_spj: false,
        problem_course: "",
        time_limit: 1000,
        memory_limit: 128,
        problem_tag: [],
        problem_difficult: 1,
        problem_status: true
      },
    };
  },
  methods: {
    getContent(text) {
      this.problem_form.problem_content = text;
    },
    async submit() {
      let back_data =
        this.$route.params.problem_id == ""
          ? await submitProblemData(this.problem_form)
          : await changeProblemData(this.problem_form);
        // console.log(back_data);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("problem/getProblemDataList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    setData(data) {
      // console.log(data)
      if (data != "") {
        let val = this.getProblemData(data);
        // console.log(val.problem_tag)
        this.problem_form = {
          problem_id: val.problem_id,
          problem_title: val.problem_title,
          problem_content: val.problem_description,
          problem_spj: val.problem_spj,
          problem_course: val.problem_course.join(' '),
          time_limit: val.time_limit,
          memory_limit: val.memory_limit,
          problem_tag: val.problem_tag,
          problem_difficult: val.problem_difficult,
          problem_status: val.problem_status
        };
      }
    },
  },
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
