<template>
  <div class="level-add">
    <el-card >
      <el-form label-position="left" label-width="80px" >
        <el-form-item label="关卡标题">
          <el-input v-model="Data.level_title"></el-input>
        </el-form-item>
        <el-form-item label="关卡描述">
          <el-input v-model="Data.level_describe"></el-input>
        </el-form-item>
        <el-form-item label="关卡状态">
          <el-switch
            v-model="Data.status"
            active-color="#13ce66"
            inactive-color="#00000033"
            @click="handleStatusChange(status)"
          ></el-switch>
        </el-form-item>
      </el-form>
      <el-button type="danger"   style=" float: right; margin-bottom: 15px; " @click="handleBackLevellist()" >取消</el-button>
      <el-button
        type="primary"
        style="float: right; margin-bottom: 15px; margin-right: 10px;"
        @click="submit({defunct: Data.status,type: Data.type,title: Data.level_title,description: Data.level_describe})"
        >提交</el-button
      >
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { addLevel } from "@/api/level";
import { ElMessage } from "element-plus";
import { useRouter, useRoute } from "vue-router";
let router = useRouter();
let route = useRoute();
let Data = ref({
  level_title: "",
  level_describe: "",
  status: false,
  type: 2,
});
let handleStatusChange = (val: any) =>{
    console.log(val);
};
let handleBackLevellist = () =>{
  router.push('/admin/levellist');
};
let setData = (val: number) =>{
  Data.value.type = val.type;
};
let submit = async (val: any) =>{
  console.log(val);
  let back_data = await addLevel(val);
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
</script>

<style lang="scss">
.level-add {
  width: 50%;
  margin: 40px auto;
  .el-card {
    margin: 20px 0;
    .el-input {
      max-width: 650px;
    }
  }
}
</style>
