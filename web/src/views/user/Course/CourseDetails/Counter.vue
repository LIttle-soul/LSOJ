<template>
  <div class="page">
    <div style="height: 40px">
      <div style="float: left">
        <el-select size="large" v-model="page.class" placeholder="Select">
          <el-option
            v-for="(item, index) in page.class_data"
            :key="index"
            :label="item.class_options"
            :value="item.class_id"
            @click="handleChange(item.class_id)"
          >
          </el-option>
        </el-select>
      </div>
      <div style="float: right">
        <el-button
          type="success"
          @click="getAllClass"
          style="margin-right: 20px"
          v-show="page.user_identity"
          >添加学生</el-button
        >
        <el-dialog v-model="form_user.addUser" title="添加学生">
          <el-form :model="form_user">
            <el-form-item label="学号添加学生(英文,分隔)">
              <el-input
                v-model="form_user.user_id"
                autocomplete="off"
                style="width: 200px"
              ></el-input>
            </el-form-item>
            <el-form-item label="班级添加学生">
              <el-select
                size="large"
                v-model="form_user.add_class_name"
                placeholder="Select"
              >
                <el-option
                  v-for="(item, index) in form_user.class_data"
                  :key="index"
                  :label="item.class_options"
                  :value="item.class_id"
                  @click="addClassId(item.class_id)"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="form_user.addUser = false">取消</el-button>
              <el-button
                type="primary"
                v-model="form_user.addUser"
                @click="addCourseUser()"
                >确定</el-button
              >
            </span>
          </template>
        </el-dialog>
        <el-button type="success" @click="form_class.addClass = true" v-show="page.user_identity">添加班级</el-button>
        <el-dialog v-model="form_class.addClass" title="添加班级">
          <el-form :model="form_class">
            <el-form-item label="班级名称">
              <el-input
                v-model="form_class.class_name"
                autocomplete="off"
                style="width: 200px"
              ></el-input>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="form_class.addClass = false">取消</el-button>
              <el-button type="primary" @click="addCourseClass()"
                >确定</el-button
              >
            </span>
          </template>
        </el-dialog>
      </div>
    </div>
    <div class="header">学生总人数({{ all_user.total }}人)</div>
    <el-table :data="userCourseStatistics" border class="content">
      <el-table-column prop="rank" label="排名" />
      <el-table-column prop="user_name" label="学生姓名" />
      <el-table-column prop="user_id" label="学生学号" />
      <el-table-column prop="task_finish" label="任务完成数" />
      <el-table-column prop="discuss" label="讨论数" />
      <el-table-column prop="score" label="分数" />
      <el-table-column prop="score" label="操作">
        <template #default="scope">
          <el-button
            size="medium"
            type="danger"
            circle
            @click="handleDeleteClick(scope.row)"
            style="margin-left: 20px"
            v-show="page.user_identity"
          >
            <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import {
  getCourseStatistics,
  getClassList,
  addStudent,
  deleteStudent,
  addClss,
  allClass,
  getUserPower
} from "@/api/course";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { useRouter, useRoute } from "vue-router";

let router = useRouter();
let route = useRoute();

let page = ref({
  course_id: route.params.course_id,
  add_course_class_name: "",
  add_course_class: 1,
  class: "",
  course_class: 1,
  class_data: [
    {
      class_id: 1,
      class_options: "",
    },
  ],
  user_identity: 1,
});

let form_user = ref({
  addUser: false,    //添加学生弹出框
  user_name: "",     //用户名称
  user_id: "",       //用户id
  add_class_id: 1,   //班级id
  add_class_name: "",    //班级名称
  class_data : [
    {
      class: 1,
      class_options: "默认班级",
    }
  ]
})
let form_class = ref({
  addClass: false,   //添加班级弹出框
  class_name: "",    //班级名称
});

let all_user = ref({
  total: 42,
});

// 页面数据
let userCourseStatistics = ref([
  {
    rank: 1, //排名
    user_name: "烟雨",
    user_id: "200910101600076",
    task_finish: "submit/all", //任务完成数
    discuss: 0, //讨论次数
  },
]);

// 格式化数据
let formatStatisticsData = (val: any) => {
  return val.map((item: any) => ({
    rank: 1,
    user_name: item.user_name,
    user_id: item.user_id,
    task_finish: item.doneChapter,
    discuss: item.discuss,
    alluser: item.total,
  }));
};
//获取班级列表
let getClasslist = async () => {
  let back_Data = await getClassList({
    course_id: Number(page.value.course_id),
  });
  console.log(back_Data);
  if (back_Data.status) {
    page.value.class_data = back_Data.message.map((res: any) => ({
      class_id: res.class_id,
      class_options: res.class_name,
    }));
    page.value.class = page.value.class_data[0].class_options;
    page.value.course_class = page.value.class_data[0].class_id;
    getUserStatisticsData();
  }
};
//获取用户统计页面数据
let getUserStatisticsData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getCourseStatistics({
    course_id: Number(page.value.course_id),
    class_id: Number(page.value.course_class),
  });
  console.log(back_data);
  if (back_data.status) {
    userCourseStatistics.value = formatStatisticsData(back_data.message);
    all_user.value.total = back_data.total;
    loading.close();
  } else {
    loading.close();
  }
};

let handleChange = (val: any) => {
  page.value.course_class = val;
  getUserStatisticsData();
};
let addClassId = (val: any) => {
  form_user.value.add_class_id = val;
};
//添加学生
let addCourseUser = async () => {
  form_user.value.addUser = false;
  let back_data = await addStudent({
    course_id: Number(page.value.course_id),
    add_class_id: Number(form_user.value.add_class_id),
    class_id: page.value.course_class,
    user_list: String(form_user.value.user_id),
  });
  if (back_data.status) {
    getUserStatisticsData();
    ElMessage({ message: back_data.message, type: "success" });
  } else {
    ElMessage({ message: back_data.message, type: "error" });
  }
};
//删除学生
let handleDeleteClick = async (val: any) => {
  ElMessageBox.confirm("确定要删除这个学生吗？", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      let back_data = await deleteStudent({
        course_id: Number(page.value.course_id),
        class_id: Number(page.value.course_class),
        user_id: val.user_id,
      });
      if (back_data.status) {
        getUserStatisticsData();
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      } else {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消删除",
      });
    });
};
//获取所有的班级
let getAllClass = async () => {
  console.log(page.value.course_class);
  form_user.value.addUser = true;
  let back_data = await allClass();
  console.log(back_data);
  if (back_data.status) {
    form_user.value.class_data = back_data.message.map((res: any) => ({
      class_id: res.class_id,
      class_options: res.class_name,
    }));
  }
};

let handleAddChange = (val: any, res: any) => {
  page.value.add_course_class = val;
  page.value.add_course_class_name = res;
};

//添加班级
let addCourseClass = async () => {
  form_class.value.addClass = false;
  console.log(form_class.value.class_name);
  let back_data = await addClss({
    course_id: Number(page.value.course_id),
    class_name: form_class.value.class_name,
  });
  if (back_data.status) {
    ElMessage({ message: back_data.message, type: "success" });
    getClasslist();
  } else {
    ElMessage({ message: back_data.message, type: "error" });
  }
};
let getPower=async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中",
    background: "rgba(0,0,0,7)"
  });
  let back_data = await getUserPower({
    course_id: Number(route.query.course_id)
  });
  console.log(back_data);
  if (back_data.status){
    page.value.user_identity = back_data.message;
    loading.close();
  }else{
    loading.close();
  }
}
//挂载
onMounted(() => {
  getClasslist();
  getPower();
});
</script>

<style lang="scss" scoped>
.page {
  max-width: 1150px;
  width: 1200px;
  margin: 5px auto;
  .header {
    font-size: 20px;
    margin-bottom: 10px;
    margin-top: 20px;
  }
  .content {
    margin-top: 20px;
    width: 100%;
  }
}
</style>
