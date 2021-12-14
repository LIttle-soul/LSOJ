<template>
  <div class="class-add">
    <el-card class="card">
      <el-form
        label-position="left"
        label-width="80px"
        :model="class_form"
        ref="form_ref"
        :rules="form_rule"
      >
        <el-form-item label="班级名称" prop="class_name">
          <el-input v-model="class_form.class_name"></el-input>
        </el-form-item>
        <el-form-item label="班级老师" prop="class_teacher">
          <el-select
            v-model="class_form.class_teacher"
            :multiple="true"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的班级教师"
            :remote-method="remotePeople"
          >
            <el-option
              v-for="item in people_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="班级学生" prop="class_student">
          <el-select
            v-model="class_form.class_student"
            :multiple="true"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的学生"
            :remote-method="remotePeople"
          >
            <el-option
              v-for="item in people_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属学校" prop="class_school">
          <el-select
            v-model="class_form.class_school"
            :multiple="false"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的学校"
            :remote-method="remoteSchool"
          >
            <el-option
              v-for="item in school_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属学院" prop="class_college">
          <el-select
            v-model="class_form.class_college"
            :multiple="false"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的学院"
            :remote-method="remoteCollege"
          >
            <el-option
              v-for="item in college_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属课程" prop="class_course">
          <el-select
            v-model="class_form.class_course"
            :multiple="false"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的课程"
            :remote-method="remoteCourse"
          >
            <el-option
              v-for="item in course_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="班级描述">
          <el-input
            v-model="class_form.class_description"
            :autosize="{ minRows: 6, maxRows: 10 }"
            type="textarea"
            class="description"
          ></el-input>
        </el-form-item>
        <el-form-item label="班级备注">
          <el-input
            v-model="class_form.class_remarks"
            :autosize="{ minRows: 4, maxRows: 10 }"
            type="textarea"
            class="description"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="float: right; margin-bottom: 15px" @click="submit"
        >提交</el-button
      >
    </el-card>
  </div>
</template>
<script lang="ts" setup>
import { ref, reactive, unref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { getUserList } from "@/api/user";
import { getAddressList } from "@/api/address";
import { getSchoolList, getCollegeList, addClassData } from "@/api/school";
import { getCourseList } from "@/api/course";

let router = useRouter();

let class_form = ref({
  class_id: 0,
  class_name: "",
  class_teacher: [],
  class_student: [],
  class_school: "",
  class_college: "",
  class_course: 0,
  class_description: "",
  class_remarks: "",
});

// 数据验证
let form_ref = ref();
let form_rule = ref({
  class_name: [{ required: true, message: "班级名称不可为空", trigger: "blur" }],
  class_teacher: [{ required: false, message: "班级教师不可为空", trigger: "blur" }],
  class_school: [{ required: true, message: "学校不可为空", trigger: "blur" }],
  class_college: [{ required: true, message: "学院不可为空", trigger: "blur" }],
});

// 可搜索数据请求
let people_list = ref({
  options: <any>[],
  loading: false,
});
let school_list = ref({
  options: <any>[],
  loading: false,
});
let college_list = ref({
  options: <any>[],
  loading: false,
});
let course_list = ref({
  options: <any>[],
  loading: false,
});

let remotePeople = async (val: string) => {
  if (val !== "") {
    people_list.value.loading = true;
    let back_data = await getUserList({
      page: 1,
      total: 10,
      text: val || "",
      user_id: "",
    });
    if (back_data.status) {
      people_list.value.options = back_data.message.map((item: any) => ({
        label: item.user_name || item.user_nick || item.user_id,
        value: item.user_id,
      }));
    } else {
      people_list.value.options = [];
    }
  } else {
    people_list.value.options = [];
  }
};
let remoteSchool = async (val: string) => {
  if (val !== "") {
    school_list.value.loading = true;
    let back_data = await getSchoolList({
      page: 1,
      total: 10,
      text: val || "",
      municipality_id: "",
      school_id: "",
    });
    if (back_data.status) {
      school_list.value.options = back_data.message.map((item: any) => ({
        label: item.school_name,
        value: item.school_id,
      }));
    } else {
      school_list.value.options = [];
    }
  } else {
    school_list.value.options = [];
  }
};
let remoteCollege = async (val: string) => {
  if (val !== "") {
    college_list.value.loading = true;
    let back_data = await getCollegeList({
      page: 1,
      total: 10,
      text: val,
      college_id: "",
      school_id: class_form.value.class_school,
    });
    if (back_data.status) {
      college_list.value.options = back_data.message.map((item: any) => ({
        label: item.college_name,
        value: item.college_id,
      }));
    } else {
      college_list.value.options = [];
    }
  } else {
    college_list.value.options = [];
  }
};
let remoteCourse = async (val: string) => {
  if (val !== "") {
    course_list.value.loading = true;
    let back_data = await getCourseList({
      page: 1,
      total: 10,
      text: val,
    });
    if (back_data.status) {
      course_list.value.options = back_data.message.map((item: any) => ({
        label: item.course_name,
        value: item.course_id,
      }));
    } else {
      course_list.value.options = [];
    }
  } else {
    course_list.value.options = [];
  }
};

// 提交数据
let submit = async () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let back_data = await addClassData({
        class_name: class_form.value.class_name || "",
        class_creator: class_form.value.class_teacher || "",
        class_note: class_form.value.class_remarks || "",
        class_introduce: class_form.value.class_description || "",
        course_id: class_form.value.class_course || 0,
        class_school: class_form.value.class_school || "",
        class_college: class_form.value.class_college || "",
        class_teacher: class_form.value.class_teacher || "",
        class_student: class_form.value.class_student || "",
      });
      console.log(back_data);
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        setTimeout(() => {
          router.push({ path: "/admin/collegelist" });
        }, 1000);
      } else {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      }
    } else {
      ElMessage({
        type: "error",
        message: "请正确填写表单信息！！！",
      });
      return false;
    }
  });
};
</script>

<style scoped lang="scss">
.class-add {
  width: 80%;
  margin: 40px auto;
  .card {
    border-radius: 20px;
    .el-input {
      max-width: 300px;
    }
    .description {
      max-width: 90%;
    }
    .bottom-button {
      float: right;
      margin-bottom: 20px;
      margin-right: 30px;
    }
  }
}
</style>
