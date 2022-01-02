<template>
  <div class="contest-add">
    <el-card >
      <el-form label-position="left" label-width="80px" >
        
        <el-form-item label="前置关卡">
          <el-select  v-model="Data.front_id" placeholder="请选择" >
            <el-option
              v-for="item in level_form"
              :key="item.level_id"
              :label="item.level_title"
              :value="item.level_id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="关卡标题">
          <el-input v-model="Data.level_title"></el-input>
        </el-form-item>
        <el-form-item label="关卡描述">
          <el-input v-model="Data.level_describe"></el-input>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card >
      <el-form label-position="left" label-width="80px" >
        <el-form-item label="关卡题目">
          <el-select
            v-model="problem_list.problem_id"
            multiple
            filterable
            clearable
            placeholder="请选择"
          >
            <el-option
              v-for="item in problem_list"
              :key="item.problem_id"
              :label="item.problem_title"
              :value="item.problem_id"
            >
            </el-option>
          </el-select>
        </el-form-item>
       <div class="twobutton">
        <el-button type="danger"   style=" float: right; margin-bottom: 15px; " @click="handleBackLevellist()">取消</el-button>
        <el-button
          type="primary"
          style="float: right; margin-bottom: 15px; margin-right: 10px;"
          @click="editsmalllevel({level_id: Data.level_id,type: Data.type,title: Data.level_title,description: Data.level_describe,front_id: Data.front_id,problems: JSON.stringify(problem_list.problem_id)})"
        >修改关卡
        </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { smallLevelMove,editLevel,searchProblem } from "@/api/level";
import { ElMessage } from "element-plus";
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
let router = useRouter();
let route = useRoute();
let Data = ref({
  front_id: "1",
  level_title: "cpdsg",
  level_describe: "cpdsg123",
  type: "2",
  level_id: "1",
  problem_id: "1234",
});
let problem_list = ref([{
  problem_id: 1001,
  problem_title: "cpdsg",
}]);
let level_form = ref([{
  level_id: "",
  level_title: "",
}]);
let formatProblemlist = (val: any) =>{
  console.log(val);
  return  val.map((item: any) =>({
      problem_id: item.problem_id,
      problem_title: item.problem_title,   
  }));
};
let handleSelectClick = async () =>{
  let back_data = await searchProblem();
  console.log(back_data)
  if (back_data.status){
    problem_list.value = formatProblemlist(back_data.message);
  }
};
let handleBackLevellist = () =>{
  router.push('/admin/levellist');
};
let setData = (val:any) =>{
  // Data.value.front_id = val.front_id;
  Data.value.level_title = val.level_title;
  Data.value.level_describe = val.level_describe;
  Data.value.type = val.type;
  Data.value.level_id = val.level_id;
};
let editsmalllevel = async (val: any) =>{
  console.log(val);
  let back_data = await editLevel(val);
  if (back_data.status){
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  }
  else{
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleLevelForm = async () =>{
  let level = await smallLevelMove();
  if (level.status) {
    level_form.value = formatData(level.message);
  }
};
let formatData = (val: any) =>{
  console.log(val)
  return  val.map((item: any) =>({
    level_id: item.level_id,
    level_title: item.title,   
  }));
};
onMounted(() =>{
  setData(route.query);
  handleLevelForm();
  handleSelectClick();
});
</script>
<style lang="scss">
.contest-add {
  width: 50%;
  margin: 40px auto;
  .el-card {
    margin: 20px 0;
    .el-input {
      max-width: 500px;
    }
  }
  .twobutton{
    margin-top: 8px;
  }
}

</style>
