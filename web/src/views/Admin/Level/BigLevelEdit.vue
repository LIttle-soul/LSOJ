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
      </el-form>
      <el-button type="danger"   style=" float: right; margin-bottom: 15px; " @click="handleBackLevellist()" >取消</el-button>
      <el-button
        type="primary"
        style=" margin-bottom: 15px; float: right; margin-right: 10px;"
        @click="editbiglevel({level_id: Data.level_id,type: Data.type,title: Data.level_title,description: Data.level_describe})"
        >修改关卡</el-button
      >
    
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { editLevel } from "@/api/level";
import { ElMessage } from "element-plus";
import { useRouter, useRoute } from "vue-router";
let route = useRoute();
let router = useRouter();
let Data = ref({
  level_title: "cpdsg",
  level_describe: "cpdsg123",
  type: "2",
  level_id: "1",
});
let handleBackLevellist = () =>{
  router.push('/admin/levellist');
};
let setData = (val: any) =>{
  Data.value.level_title = val.level_title;
  Data.value.level_describe = val.level_describe;
  Data.value.type = val.type;
  Data.value.level_id = val.level_id;
};
let editbiglevel = async (val: any) =>{
  console.log(val);
  let back_data = await editLevel(val);
  if  (back_data.status){
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
onMounted(()=>{
  setData(route.query);
});
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
