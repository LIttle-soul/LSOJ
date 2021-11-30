<template>
  <div class="class-add">
    <el-card class="card">
      <el-form
        label-position="left"
        label-width="80px"
        v-model="class_form"
        ref="form_ref"
        :rules="form_rule"
      >
        <el-form-item label="班级名称">
          <el-input v-model="class_form.class_name"></el-input>
        </el-form-item>
        <el-form-item label="班级老师">
          <el-input v-model="class_form.class_teacher"></el-input>
        </el-form-item>
        <el-form-item label="班级学生">
          <el-input v-model="class_form.class_student"></el-input>
        </el-form-item>
        <el-form-item label="所属学校">
          <el-cascader
            placeholder="请选择学校"
            v-model="class_form.class_school"
            :props="school_list"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="所属学院">
          <el-cascader
            placeholder="请选择学院"
            v-model="class_form.class_college"
            :props="college_list"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="所属专业">
          <el-input v-model="class_form.class_major" placeholder="请输入你的专业">
          </el-input>
        </el-form-item>
        <el-form-item label="所属课程">
          <el-cascader
            placeholder="请选择所属课程"
            v-model="class_form.class_course"
            :props="course_list"
            :clearable="true"
          >
          </el-cascader>
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
import { getAddressList } from "@/api/address";
import { getSchoolList, addCollegeData } from "@/api/school";

let router = useRouter();

let class_form = ref({
  class_id: 0,
  class_name: "",
  class_teacher: "",
  class_student: "",
  class_school: [],
  class_college: [],
  class_major: [],
  class_course: [],
  class_description: "",
  class_remarks: "",
});

// 数据验证
let form_ref = ref();
let form_rule = ref({
  college_name: [{ required: true, message: "学院名称不可为空", trigger: "blur" }],
  college_school: [{ required: true, message: "学校不可为空", trigger: "blur" }],
});

// 懒加载数据请求
let school_list = ref({
  lazy: true,
  lazyLoad(node: any, resolve: any) {
    const { level, value } = node;
    switch (level) {
      case 0:
        getAddress("", 0, "province", resolve);
        break;
      case 1:
        getAddress("province", value, "municipality", resolve);
        break;
      case 2:
        getSchool(value, resolve);
        break;
      default:
        resolve([]);
    }
  },
});
let college_list = ref({
  lazy: true,
  lazyLoad(node: any, resolve: any) {
    resolve([]);
  },
});
let course_list = ref({
  lazy: true,
  lazyLoad(node: any, resolve: any) {
    resolve([]);
  },
});

// 相关数据获取
let getAddress = async (
  father: string,
  father_id: number,
  child: string,
  resolve: any
) => {
  let back_data = await getAddressList(<any>{
    father: father,
    father_id: father_id,
    child: child,
    page: 1,
    total: 100,
  });
  // console.log(back_data);
  if (back_data.status) {
    resolve(formatAddress(back_data.message));
  }
};

let getSchool = async (municipality_id: number, resolve: any) => {
  let back_data = await getSchoolList(<any>{
    page: 1,
    total: 500,
    text: "",
    municipality_id: municipality_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    resolve(formatSchool(back_data.message));
  }
};

// 相关数格式化
let formatAddress = (val: any) => {
  return val.map((item: any) => ({
    value: item.id,
    label: item.name,
    leaf: item.deep >= 3,
  }));
};
let formatSchool = (val: any) => {
  return val.map((item: any) => ({
    value: item.school_id,
    label: item.school_name,
    leaf: true,
  }));
};

let submit = async () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let back_data = await addCollegeData({});
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
