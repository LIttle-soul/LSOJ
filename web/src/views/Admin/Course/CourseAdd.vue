<template>
  <div class="course-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="course_form">
        <el-form-item label="课程编号">
          <el-input-number v-model="course_form.course_id" disabled controls-position="right"></el-input-number>
        </el-form-item>
        <el-form-item label="课程名称">
          <el-input v-model="course_form.course_name"></el-input>
        </el-form-item>
        <!-- <el-form-item label="课程学校">
          <el-input v-model="course_form.course_school">
          </el-input>
        </el-form-item> -->
        <el-form-item label="课程学分">
          <el-select v-model="course_form.course_credits" placeholder="请选择">
            <el-option v-for="item in credits_options" :key="item.value" :label="item.title" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="课程价格">
          <el-input style="width:150px" v-model="course_form.course_cost"></el-input>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker v-model="course_form.start_time" type="datetime" format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss" placeholder="选择日期时间"></el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker v-model="course_form.end_time" type="datetime" format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss" placeholder="选择日期时间"></el-date-picker>
        </el-form-item>
        <el-form-item label="封面上传" ref="uploadElement" prop="course_cover">
          <el-input v-model="course_form.course_cover" v-if="fasle"></el-input>
          <el-upload action="/api/course/getcoursedetails/" ref="upload" :show-file-list="fasle" :limit=1
            :before-upload="beforeUpload" :on-change="handleChange" :auto-upload="false" :data="course_data">
            <img v-show="course_form.course_cover" :src="course_form.course_cover" class="avatar">
            <el-button size="mini" type="primary">添加课程封面</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="float: right; margin-bottom: 15px" @click="submitCourse">提交</el-button>
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">课程介绍</span>
          <el-button class="button" type="text" @click="change = !change">修改内容</el-button>
        </div>
      </template>
      <CourseChild mode="preview" :content="course_form.course_introduce" />
    </el-card>
    <el-dialog title="内容编辑" v-model="change" width="90%" top="60px" center>
      <CourseChild height="800px" :content="course_form.course_introduce" @getCourse="getCourse" />
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import CourseChild from "@/components/Editor/MarkdownEditor.vue";
import {
  submitCourseData,
  changeCourseData,
  getCourseList,
  submitCourseImg,
  getcoursemessage,
} from "@/api/course";
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted, watchEffect } from "vue";
import { ElMessage } from "element-plus";
import dayJS from "dayjs";
import course_mode from "@/assets/markdown/CourseTemplet.md?raw";
import { rejects } from "assert";

let route = useRoute();
let router = useRouter();

let change = ref(false);

let credits_options = [
  { value: 0, title: "20" },
  { value: 1, title: "30" },
];
let course_form = ref({
  course_id: 0,
  course_name: "",
  course_school: "",
  course_introduce: course_mode,
  course_credits: 0,
  course_cost: 0,
  start_time: "2020-01-01 08:00:00",
  end_time: "2020-01-01 16:00:00",
  course_cover: "",
});

// 数据处理
let getCourse = (text: string) => {
  course_form.value.course_introduce = text;
};
//提交数据
let submitCourse = async () => {
  console.log(route.query.course_id);
  let back_data =
    route.query.course_id == ""
      ? await submitCourseData({
          course_id: "",
          course_name: course_form.value.course_name,
          course_school: course_form.value.course_school,
          course_credits: course_form.value.course_credits,
          course_cost: course_form.value.course_cost,
          start_time: course_form.value.start_time,
          end_time: course_form.value.end_time,
          course_introduce: course_form.value.course_introduce,
        })
      : await changeCourseData({
          course_id: course_form.value.course_id,
          course_name: course_form.value.course_name,
          course_school: course_form.value.course_school,
          course_credits: course_form.value.course_credits,
          course_cost: course_form.value.course_cost,
          start_time: course_form.value.start_time,
          end_time: course_form.value.end_time,
          course_introduce: course_form.value.course_introduce,
        });
  console.log(back_data);
  if (back_data.status) {
    subminImg(back_data.course_id);
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    setTimeout(() => {
      router.push("/admin/CourseList");
    }, 2000);
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
//添加图片
let subminImg = async (res: any) => {
  let back_data = await submitCourseImg({
    course_cover: course_form.value.course_cover,
    course_id: res,
  });
  console.log(back_data);
};
//格式化课程数据
let formatData = (val: any) => {
  console.log(val);
  return {
    course_id: val.course_id,
    course_name: val.course_title,
    course_school: "金职院",
    course_introduce: val.course_introduce,
    course_credits: val.course_credits,
    course_cost: val.course_cost,
    start_time: dayJS(val.start_time).format("YYYY-MM-DD HH:mm:ss"),
    end_time: dayJS(val.end_time).format("YYYY-MM-DD HH:mm:ss"),
    course_cover: val.course_cover,
  };
};
//更改图片为base64
let handleChange = (file: any) => {
  getBase64(file.raw).then((res) => {
    let params = res;
    course_form.value.course_cover = String(params);
  });
};

let getBase64 = (file: any) => {
  return new Promise(function (resolve, reject) {
    const reader = new FileReader();
    let imgResult = "";
    reader.readAsDataURL(file);
    reader.onload = function () {
      imgResult = String(reader.result);
    };
    reader.onerror = function (error) {
      reject(error);
    };
    reader.onloadend = function () {
      resolve(imgResult);
    };
  });
};
//获取图片数据
let getcourseIdData = async () => {
  let back_data = await getcoursemessage({
    course_id: route.query.course_id,
  });
  console.log(back_data);
  if (back_data.status) {
    course_form.value = formatData(back_data.message);
  }
};
//挂载
onMounted(() => {
  console.log(route.query.course_id);
  if (route.query.course_id) {
    getcourseIdData();
  }
  // console.log(route.params);
  // if (route.params.course_id) {
  //   getCourseData(Number(route.params.course_id[0]));
  // }
});
</script>

<style lang="scss" scoped>
.course-add {
  width: 95%;
  margin: 40px auto;
  .card {
    margin: 30px 0;
    border-radius: 20px;
    .el-input {
      max-width: 400px;
    }
    .course-span {
      font-size: 18px;
      font-weight: 800;
      margin-left: 20px;
    }
    .avatar {
      width: 180px;
      height: 150px;
      display: block;
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
