<template>
  <div class="judger-box">
    <el-form label-width="80px">
      <el-form-item label="提交编号">
        <el-input v-model="judger_form.solution_id"></el-input>
      </el-form-item>
      <el-form-item label="问题编号">
        <el-input v-model="judger_form.problem_id"></el-input>
      </el-form-item>
      <el-form-item label="竞赛编号">
        <el-input v-model="judger_form.contest_id"></el-input>
      </el-form-item>
      <el-form-item label="用户账号">
        <el-input v-model="judger_form.user_id"></el-input>
      </el-form-item>
    </el-form>
    <div class="bottom">
      <el-button type="primary" class="bottom_button" @click="submit">提交</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { afreshJudgerSolution } from "@/api/solution";
import { ElMessage } from "element-plus";

let judger_form = ref({
  solution_id: "",
  problem_id: "",
  contest_id: "",
  user_id: "",
});

let submit = async () => {
  let back_data = await afreshJudgerSolution({
    solution_id: judger_form.value.solution_id || "",
    problem_id: judger_form.value.problem_id || "",
    contest_id: judger_form.value.contest_id || "",
    user_id: judger_form.value.user_id || "",
  });
  //   console.log(back_data);
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
</script>

<style scoped lang="scss">
.judger-box {
  width: 80%;
  max-width: 400px;
  min-width: 200px;
  margin: 0 auto;
  margin-top: 100px;
  background: #ffffff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 0 10px #dddddddd;
  .bottom {
    height: 40px;
    width: 100%;
    display: flex;
    justify-content: end;
  }
}
</style>
