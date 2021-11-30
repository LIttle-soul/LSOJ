<template>
  <div class="college-add">
    <el-card class="card">
      <el-form
        label-position="left"
        label-width="80px"
        v-model="college_form"
        ref="form_ref"
        :rules="form_rule"
      >
        <el-form-item label="学院名称" prop="college_name">
          <el-input v-model="college_form.college_name"></el-input>
        </el-form-item>
        <el-form-item label="所属学校" prop="college_school">
          <el-cascader
            placeholder="请选择学校"
            v-model="college_form.college_school"
            :props="school_list"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="学院描述">
          <el-input
            v-model="college_form.college_description"
            :autosize="{ minRows: 6, maxRows: 10 }"
            type="textarea"
            class="description"
          ></el-input>
        </el-form-item>
        <el-form-item label="学院备注">
          <el-input
            v-model="college_form.college_remarks"
            :autosize="{ minRows: 4, maxRows: 10 }"
            type="textarea"
            class="description"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" class="bottom-button" @click="submit">提交</el-button>
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

let college_form = ref({
  college_id: 0,
  college_name: "",
  college_school: [],
  college_description: "",
  college_remarks: "",
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
      let back_data = await addCollegeData({
        college_id: college_form.value.college_id,
        college_name: college_form.value.college_name,
        college_school: college_form.value.college_school,
        college_description: college_form.value.college_description,
        college_remarks: college_form.value.college_remarks,
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
.college-add {
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
