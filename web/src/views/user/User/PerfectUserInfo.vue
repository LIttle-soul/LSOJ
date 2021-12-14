<template>
  <div class="perfect">
    <!-- 基础信息修改完善 -->
    <el-card class="box-card">
      <h1 style="margin-bottom: 20px">
        <el-icon size="1.4em"><setting /></el-icon> {{ form_title }}
      </h1>
      <el-form
        ref="form_ref"
        :model="user_form"
        :rules="user_form_rules"
        label-width="80px"
        size="mini"
      >
        <el-form-item label="真实姓名" prop="user_name">
          <el-input
            placeholder="好汉，留名不杀"
            v-model="user_form.user_name"
            :disabled="activate"
          ></el-input>
        </el-form-item>
        <el-form-item label="个人昵称" prop="user_nick">
          <el-input
            placeholder="有趣的灵魂总能相遇"
            v-model="user_form.user_nick"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的性别">
          <el-radio-group v-model="user_form.user_sex" size="medium" :disabled="activate">
            <el-radio :label="0">男</el-radio>
            <el-radio :label="1">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="我的介绍">
          <el-input
            placeholder="此站是我开，此框是我管，要想我知你，留下自荐信"
            class="input-width"
            type="textarea"
            v-model="user_form.user_introduce"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的电话" prop="user_telephone">
          <el-input
            placeholder="怕我找你？切！懒得理你"
            v-model="user_form.user_telephone"
          ></el-input>
        </el-form-item>
        <el-form-item label="我的生日" prop="user_birthday">
          <el-date-picker
            v-model="user_form.user_birthday"
            type="date"
            size="small"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            placeholder="成功完善生日信息有惊喜哦"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="我的地址">
          <el-cascader
            placeholder="请输入你的地址"
            v-model="user_form.user_address"
            :props="address_list"
            :clearable="true"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="我的学校">
          <el-select
            v-model="user_form.user_school"
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
        <el-form-item label="我的班级">
          <el-select
            v-model="user_form.user_class"
            :multiple="false"
            :filterable="true"
            :remote="true"
            :reserve-keyword="true"
            placeholder="请输入你的班级"
            :remote-method="remoteClass"
            :disabled="user_form.user_school === null || user_form.user_school === ''"
          >
            <el-option
              v-for="item in class_list.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, reactive, ref, unref } from "vue";
import { useStore, mapState } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Setting } from "@element-plus/icons";
import { submitUserInfoForm } from "@/api/user";
import dayJS from "dayjs";
import { getAddressList } from "@/api/address";
import { getSchoolList, getClassList } from "@/api/school";

let store = useStore();
let router = useRouter();

// Vuex 数据获取
let store_user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);

// 相关信息填充
let form_title = "基础信息完善";
let activate = ref(false);
let school_status = ref(false);

// console.log(store_user_info.value);

let user_form = ref({
  user_name: store_user_info.value?.user_name || "",
  user_nick: store_user_info.value?.user_nick || "",
  user_introduce: store_user_info.value?.user_introduce || "",
  user_telephone: store_user_info.value?.user_telephone || "",
  user_birthday: dayJS(store_user_info.value?.user_birthday || "2000-01-01").format(
    "YYYY-MM-DD"
  ),
  user_school: store_user_info.value?.user_school.school_id.split(",") || "",
  user_class: store_user_info.value?.user_class?.class_id.split(",") || "",
  user_address: store_user_info.value?.user_address?.address_id.split(",") || "",
  user_sex: store_user_info.value?.user_sex || 0,
});

// 数据验证
let form_ref = ref();
let user_form_rules = reactive({
  user_name: [
    { required: true, message: "姓名不能为空", trigger: "blur" },
    { min: 1, max: 20, message: "姓名必须在2-20个字符之间", trigger: "blur" },
  ],
  user_nick: [{ required: true, message: "用户昵称不能为空", trigger: "blur" }],
  user_telephone: [
    {
      type: "string",
      required: false,
      pattern: /^[1]([3-9])[0-9]{9}$/,
      message: "请输入正确的电话号码",
      trigger: "blur",
    },
  ],
  user_birthday: [{ required: true, message: "生日不允许为空", trigger: "blur" }],
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
let school_list = ref({
  options: <any>[],
  loading: false,
});
let class_list = ref({
  options: <any>[],
  loading: false,
});
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
let remoteClass = async (val: string) => {
  if (val !== "") {
    school_list.value.loading = true;
    let back_data = await getClassList({
      page: 1,
      total: 10,
      text: val || "",
      school_id: user_form.value.user_school,
      college_id: "",
      class_id: "",
      course_id: "",
    });
    if (back_data.status) {
      class_list.value.options = back_data.message.map((item: any) => ({
        label: item.class_name,
        value: item.class_id,
      }));
    } else {
      class_list.value.options = [];
    }
  } else {
    class_list.value.options = [];
  }
};
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
    leaf: item.deep >= 3,
  }));
};

// 数据提交
let onSubmit = async () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let back_data = await submitUserInfoForm({
        user_name: user_form.value.user_name || "",
        user_nick: user_form.value.user_nick || "",
        user_introduce: user_form.value.user_introduce || "",
        user_telephone: user_form.value.user_telephone || "",
        user_birthday: user_form.value.user_birthday || "",
        user_school: user_form.value.user_school || "",
        user_class: user_form.value.user_class || "",
        user_address: user_form.value.user_address || "",
        user_sex: user_form.value.user_sex || 0,
      });
      // console.log(back_data);
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        store.dispatch("user/getUserInfo");
        setTimeout(() => {
          router.push({ path: "/showuserinfo" });
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
.perfect {
  max-width: 500px;
  min-width: 350px;
  margin: 0 auto;
  .box-card {
    margin: 40px auto;
    .el-input {
      max-width: 300px;
    }
    .input-width {
      width: 300px;
    }
  }
}
</style>
