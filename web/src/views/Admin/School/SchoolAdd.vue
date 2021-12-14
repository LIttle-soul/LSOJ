<template>
  <div class="school-add">
    <el-card class="card">
      <el-form
        label-position="left"
        label-width="80px"
        :model="school_form"
        ref="form_ref"
        :rules="form_rule"
      >
        <el-form-item label="学校编号" prop="school_id">
          <el-input v-model="school_form.school_id"></el-input>
        </el-form-item>
        <el-form-item label="学校名称" prop="school_name">
          <el-input v-model="school_form.school_name"></el-input>
        </el-form-item>
        <el-form-item label="主管部门">
          <el-input v-model="school_form.school_department"></el-input>
        </el-form-item>
        <el-form-item label="办学层次">
          <el-input v-model="school_form.school_rank"></el-input>
        </el-form-item>
        <el-form-item label="所在城市" prop="school_municipality">
          <el-cascader
            placeholder="请选择城市"
            v-model="school_form.school_municipality"
            :props="address_list"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="学校描述">
          <el-input
            v-model="school_form.school_describe"
            :autosize="{ minRows: 6, maxRows: 10 }"
            type="textarea"
            class="description"
          ></el-input>
        </el-form-item>
        <el-form-item label="学校备注">
          <el-input
            v-model="school_form.school_remark"
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
import { getSchoolList, addSchoolData } from "@/api/school";

let router = useRouter();

let school_form = ref({
  school_id: "",
  school_name: "",
  school_describe: "",
  school_department: "",
  school_rank: "",
  school_remark: "",
  school_municipality: "",
});

// 数据验证
let form_ref = ref();
let form_rule = ref({
  school_id: [{ required: true, message: "学校编号不可为空", trigger: "blur" }],
  school_name: [{ required: true, message: "学校名称不可为空", trigger: "blur" }],
  school_municipality: [
    { required: true, message: "学校所在地不可为空", trigger: "blur" },
  ],
});

// 懒加载数据请求
let address_list = ref({
  lazy: true,
  lazyLoad(node: any, resolve: any) {
    const { level, value } = node;
    // console.log(level, value);
    switch (level) {
      case 0:
        getAddress("", 0, "province", resolve);
        break;
      case 1:
        getAddress("province", value, "municipality", resolve);
        break;
      case 2:
        getAddress("municipality", value, "district", resolve);
        break;
      case 3:
        getAddress("district", value, "township", resolve);
        break;
      case 4:
        getAddress("township", value, "village", resolve);
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

// 相关数格式化
let formatAddress = (val: any) => {
  return val.map((item: any) => ({
    value: item.id,
    label: item.name,
    leaf: item.deep >= 2,
  }));
};

// 数据提交
let submit = async () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let back_data = await addSchoolData({
        school_id: school_form.value.school_id,
        school_name: school_form.value.school_name,
        school_describe: school_form.value.school_describe,
        school_municipality: school_form.value.school_municipality,
        school_department: school_form.value.school_department,
        school_rank: school_form.value.school_rank,
        school_remark: school_form.value.school_remark,
      });
      console.log(back_data);
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        setTimeout(() => {
          router.push({ path: "/admin/schoollist" });
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
.school-add {
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
