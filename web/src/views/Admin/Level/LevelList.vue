<template>
    <div class="level-list">
         <div class="level-list-child">
            <el-card>
                <div class="table-header">
                    关卡列表
                  <div class="current-time">当前时间:{{ current_time }}</div>
                </div>
                <el-input 
                    placeholder="请输入内容" 
                    size="mini" 
                    v-model="find.search_data" 
                    class="input-with-select"
                > 
                <template #prefix>
                  <el-icon
                    color="#AAAAAA"
                    style="font-size: 1.1rem; transform: translateY(7px)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 1024 1024"
                      data-v-394d1fd8=""
                    >
                      <path
                        fill="currentColor"
                        d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704z"
                      ></path>
                    </svg>
                  </el-icon>
                </template>
                <template #append>
                    <el-button
                    icon="el-icon-search"
                    @click="search_all_data(find.search_data)"
                    >搜索</el-button> 
                </template>
                </el-input>
            <div>
                <el-table :data="Data" size="mini" :stripe="false" :fit="true" row-key="level_id" style="width: 100%;"
                :default-sort="{ prop: 'num', order: 'ascending' }"
                :tree-props="{children: 'level_list', hasChildren: 'problem_list'}"
                :default-expand-all="false"
                :lazy:="true"
                >
                <el-table-column prop="level_id" label="关卡编号"> </el-table-column>
                <el-table-column prop="level_title" label="关卡标题"> </el-table-column>
                <el-table-column prop="level_describe" label="关卡描述"></el-table-column>
                <!-- <el-table-column prop="type"  label="类型"> </el-table-column>
                <el-table-column prop="front_id"   label="前置关卡"> </el-table-column> -->
                <el-table-column prop="creator" label="创建者"></el-table-column>
                <el-table-column prop="status"  fixed="right" width="50px" label="状态">
                    <template #default="scope">
                    <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949" @click="handleStatusChange({
                      level_id: scope.row.level_id,
                      status: scope.row.status,
                      })"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column fixed="right" width="125px" label="操作">
                    <template #default="scope">
                    <div>
                    <el-button size="mini" type="primary" circle  @click="handleEditClick({  
                        level_id: scope.row.level_id,
                        level_title: scope.row.level_title,
                        level_describe: scope.row.level_describe,
                        type: scope.row.type,
                    })">
                      <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
                    </el-button>
                    <el-button size="mini" type="success" circle  @click="handleAddlevelClick({
                      type: scope.row.type,
                    })">
                      <el-icon :size="16"><i class="bi bi-plus-lg"></i></el-icon>
                    </el-button>
                    <el-button size="mini" type="danger" circle  @click="confirmDelete({
                      level_id: scope.row.level_id,
                    })">
                      <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
                    </el-button>
                    </div>
                    <el-button size="mini" type="info" circle  @click="handleUpClick({
                        level_id: scope.row.level_id,
                        type: scope.row.type,
                        move: 1,
                        front_id: scope.row.front_id,
                    })">
                      <el-icon :size="16"><i class="bi bi-arrow-up"></i></el-icon>
                    </el-button>
                    <el-button class="downbutton" size="mini" type="info" circle @click="handleDownClick({
                        level_id: scope.row.level_id,
                        type: scope.row.type,
                        move: 2,
                        front_id: scope.row.front_id,
                    })">
                      <el-icon :size="16"><i class="bi bi-arrow-down"></i></el-icon>
                    </el-button>

                    </template>
                </el-table-column>
                </el-table>
            </div>
            </el-card>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ElLoading,ElMessageBox,ElMessage } from "element-plus";
import { edithideLevel,levelMove,searchLevel } from "@/api/level";
import { getLevelList,deleteLevel } from "@/api/level";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import dayJS from "dayjs";
let router = useRouter();
let find = ref({
  search_data: "",
})
let Data = ref([{
    creator:"admin",
    level_describe:"青铜玩家往往是最不受控制的爱好者，他们不熟悉规则，不明白什么时候该去提交，什么时候该去改代码，他们的特点就是“犟”。↵无论你在干什么，他们因为写不出这道代码，所以就会在简单的题目上找找快感，所以在周赛的时候，他总会一个人默默地写简单的题目，没有任何战绩可言。",
    front_id:"0",
    level_id:"1",
    status: true,
    level_title: "倔强青铜",
    type: 2,
    level_list: [
    {
        creator:"admin",
        level_describe:"解决输入输出的问题",
        front_id: "1",
        level_id: "10",
        status: true,
        level_title: "计算机开口说话",
        type: 1,
    }
    ]
}]);
let current_time = ref(dayJS().format("YYYY-MM-DD HH:mm:ss"));

let interval = setInterval(() => {
  current_time.value = dayJS().format("YYYY-MM-DD HH:mm:ss");
}, 1000);


let getlevellist = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中...",
    background: "rgba(0,0,0,0.7)",
  });
  let level = await getLevelList();
  if (level.status) {
    Data.value = formatData(level.message);
    loading.close();
  }
  console.log(level.message);
};
let formatData = (val: any) => {
  return val.map((item: any) => ({
      creator:item.creator,
      level_describe: item.description,
      front_id: item.front_id,
      level_id: item.level_id,
      status: item.status,
      level_title: item.title,
      type: item.type, 
      level_list: item.level_list.map((it: any) => ({
          creator:it.creator,
          level_describe: it.description,
          front_id: it.front_id,
          level_id: it.level_id,
          status: it.status,
          level_title: it.title,
          type: it.type,
      }))
  }))
};
let handleUpClick = async (val: any) => {
  let back_data = await levelMove(val);
  if (back_data.status === false){
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleDownClick = async (val: any) => {
  let back_data = await levelMove(val);
  if (back_data.status === false){
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleAddlevelClick = (val: any) =>{
  if (val.type === 1){
    router.push({
      path:"/admin/SmallLevelAdd",
    })
  }
  else{
    router.push({
      path:"/admin/LevelAdd",
    })
  }
};
let handleEditClick = (val: any) =>{
  if (val.type === 1){
    router.push({
      path:"/admin/SmallLevelEdit",
      query: {
        type: val.type,
        level_title: val.level_title,
        level_describe: val.level_describe,
        // front_id: val.front_id,
        level_id: val.level_id,
      },
    })
  }
  else{
    router.push({
      path:"/admin/BigLevelEdit",
      query: {
        type: val.type,
        level_title: val.level_title,
        level_describe: val.level_describe,
        level_id: val.level_id,
      },
    })
  }
};
let handleStatusChange = (val: any) =>{
  console.log(val.level_id,val.status);
  Data.value.status =!Data.value.status
  handleStatuschange({ level_id: val.level_id,defunct: val.status })
};
let handleStatuschange = async (val: any) =>{
  let back_data = await edithideLevel(val);
  if (back_data.status === false){
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleDeleteClick = async (val: number) => {
  // let data = {
  //   level_id: Data.value.level_id,
  // };
  console.log(val);
  let back_data = await deleteLevel(val);
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
let confirmDelete = (val: number) =>{
  ElMessageBox.confirm(
    "你确定要删除此关卡吗？",
    "确认信息",
    {
      confirmButtonText: "确认",
      cancelButtonText: "取消",
      // type: "warning",
      distinguishCancelAndClose: true,
    }
  )
    .then(() => {
      handleDeleteClick(val);
    })
    .catch(() => {});
};
let search_All_Data = async (val: string) => {
  let back_data = await searchLevel(val);
  if (back_data.status) {
    Data.value = formatLevel(back_data.message);
  }
  else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });   
  } 
};
let formatLevel = (val: any) =>{
  return  val.map((item: any) =>({
      creator: item.creator,  
      level_describe: item.description,
      level_id: item.level_id,
      front_id: item.front_id,
      level_title: item.title,
      type: item.type,
      status: item.status,
      level_list: item.level_list.map((it: any) =>({
        creator: it.creator,
        level_describe: it.description,
        level_id: it.level_id,
        status: it.status,
        level_title: it.title,
        type: it.type,
        front_id: it.front_id,
      }))
  }))
};
let search_all_data = (val: string) =>{
  console.log(val);
  find.value.search_data = val;
  if (val === undefined){
    val = "";
  }
  search_All_Data({ text: val });
};

onMounted(() => {
    getlevellist();
});
</script>

<style scoped lang="scss">
.level-list{
  width: 95%;   
  max-width: 1200px;
  margin: 70px auto;
  .table-header {
    font: 1.2em "楷体";
    letter-spacing: 3px;
    height: 30px;
    width: 50%;
    min-width: 210px;
    float: left;
    margin-bottom: 5px;
    .current-time {
      font-size: 10px;
      color: darkturquoise;
      letter-spacing: 1px;
    }
  }
  .input-with-select {
    width: 205px;
    float: right;
    margin-right: 10px;
    transform: translateY(-1px);
  }
  .downbutton{
    margin-top: 10px;
    margin-left: 10px;
  }

}

  
</style>