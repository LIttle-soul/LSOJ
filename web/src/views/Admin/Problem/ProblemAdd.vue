<template>
  <div class="problem-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="problem_form">
        <el-form-item label="题目编号">
          <el-input-number
            v-model="problem_form.problem_id"
            controls-position="right"
            :disabled="change_problem_id"
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
      <el-button type="primary" style="float: right; margin-bottom: 15px" @click="submit"
        >提交</el-button
      >
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">题目内容</span>
          <el-button class="button" type="text" @click="changeProblem = !changeProblem"
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
    <el-dialog title="内容编辑" v-model="changeProblem" width="90%" top="60px" center>
      <ProblemChild
        height="800px"
        :content="problem_form.problem_content"
        @getContent="getContent"
      />
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import ProblemChild from "@/components/Editor/MarkdownEditor.vue";
import { submitProblemData, changeProblemData, getProblemDataList } from "@/api/problem";
import { useStore, mapState } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { ElLoading, ElMessage } from "element-plus";
import problem_mode from "@/assets/markdown/ProblemTemplet.md?raw";

let store = useStore();
let route = useRoute();
let router = useRouter();

let problem_tag_list = computed(
  mapState("problem", ["problem_tag_list"]).problem_tag_list.bind({
    $store: store,
  })
);

let changeProblem = ref(false);
let change_problem_id = ref(false);
let problem_form = ref({
  problem_id: 9999,
  problem_title: "",
  problem_content: problem_mode,
  problem_spj: false,
  problem_course: "",
  time_limit: 1000,
  memory_limit: 128,
  problem_tag: [],
  problem_difficult: 0,
  problem_status: true,
});
let getContent = (text: string) => {
  problem_form.value.problem_content = text;
};
let submit = async () => {
  let back_data =
    route.params.problem_id == ""
      ? await submitProblemData({
          problem_id: problem_form.value.problem_id,
          problem_title: problem_form.value.problem_title,
          problem_description: problem_form.value.problem_content,
          problem_spj: problem_form.value.problem_spj,
          problem_course: problem_form.value.problem_course,
          time_limit: problem_form.value.time_limit,
          memory_limit: problem_form.value.memory_limit,
          problem_tag: problem_form.value.problem_tag,
          problem_difficult: problem_form.value.problem_difficult,
          problem_status: problem_form.value.problem_status,
        })
      : await changeProblemData({
          problem_id: problem_form.value.problem_id,
          problem_title: problem_form.value.problem_title,
          problem_description: problem_form.value.problem_content,
          problem_spj: problem_form.value.problem_spj,
          problem_course: problem_form.value.problem_course,
          time_limit: problem_form.value.time_limit,
          memory_limit: problem_form.value.memory_limit,
          problem_tag: problem_form.value.problem_tag.join(","),
          problem_difficult: problem_form.value.problem_difficult,
          problem_status: problem_form.value.problem_status,
        });
  // console.log(back_data);
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    setTimeout(() => {
      router.push("/admin/problemlist");
    }, 2000);
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let formatData = (val: any) => {
  return {
    problem_id: val.problem_id,
    problem_title: val.problem_title,
    problem_content: val.problem_description,
    problem_spj: val.problem_spj,
    problem_course: val.problem_course || "",
    time_limit: val.time_limit,
    memory_limit: val.memory_limit,
    problem_tag: val.problem_tag.split(","),
    problem_difficult: val.problem_difficult,
    problem_status: val.problem_status,
  };
};
let getProblemData = async (val: string) => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getProblemDataList({
    page: 1,
    total: 50,
    key: "id",
    text: val,
  });
  if (back_data.status) {
    problem_form.value = formatData(back_data.message[0]);
    loading.close();
  } else {
    loading.close();
  }
};
onMounted(() => {
  if (route.params.problem_id) {
    change_problem_id.value = true;
    getProblemData(<string>route.params.problem_id[0]);
  }
});
</script>

<style scoped lang="scss">
.problem-add {
  width: 95%;
  margin: 40px auto;
  .card {
    margin: 30px 0;
    border-radius: 20px;
    .el-input {
      max-width: 400px;
    }
    .problem-span {
      font-size: 18px;
      font-weight: 800;
      margin-left: 20px;
    }
    .el-rate {
      height: 40px;
      line-height: 40px;
      transform: translateY(5px);
      // background-color: #555666;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      .title {
        width: 100px;
        height: 20px;
        line-height: 20px;
        font-size: 20px;
        font-weight: 800;
        font-family: "宋体";
      }
      .button {
        width: 60px;
        height: 20px;
      }
    }
  }
}
</style>
