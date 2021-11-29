<template>
  <div class="team-registration">
    <el-form label-width="80px" ref="form_ref" :rules="team_data_rules" :model="teamData">
      <el-form-item label="团队名称" prop="team_title">
        <el-input v-model="teamData.team_title" input-style="width: 208px"></el-input>
      </el-form-item>
      <el-form-item label="团队介绍">
        <el-input
          type="textarea"
          v-model="teamData.team_introduce"
          input-style="width: 208px"
        ></el-input>
      </el-form-item>
      <el-form-item label="指导老师" prop="team_teacher">
        <el-input
          v-model="teamData.team_teacher"
          placeholder="请输入老师账号"
          input-style="width: 208px"
        >
        </el-input>
      </el-form-item>
      <el-form-item label="学校" prop="team_school">
        <el-cascader
          placeholder="请选择团队所在学校"
          v-model="teamData.team_school"
          :props="school_list"
          :clearable="true"
        >
        </el-cascader>
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="submitTeamData">提交</el-button>
  </div>
</template>

<script lang="ts" setup>
import { teamRegistration } from "@/api/user";
import { useStore, mapState } from "vuex";
import { reactive, ref, unref } from "vue";
import { ElMessage } from "element-plus";
import { getAddressList } from "@/api/address";
import { getSchoolList } from "@/api/school";
import { getUserList } from "@/api/user";

let store = useStore();

// 团队表单数据
let teamData = reactive({
  team_title: "",
  team_introduce: "",
  team_school: "",
  team_teacher: "",
});

// 表单自定义效验
let form_ref = ref();
let check_teacher = async (rule: any, value: any, callback: any) => {
  if (value) {
    // console.log(value);
    let back_data = await getUserList({
      page: 1,
      total: 1,
      text: "",
      user_id: value,
    });
    if (back_data.status) {
      callback();
    } else {
      callback(back_data.message);
    }
  } else {
    callback();
  }
};

let team_data_rules = reactive({
  team_title: [
    { required: true, message: "团队名不可为空", trigger: "blur" },
    { min: 4, max: 20, message: "团队名必须在4-20个字符之间", trigger: "blur" },
  ],
  team_school: [{ required: true, message: "请选择团队所在学校", trigger: "blur" }],
  team_teacher: [{ validator: check_teacher, trigger: "blur" }],
});

// vuex数据获取懒加载
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

let emits = defineEmits(["reloadTeamData"]);

// 数据提交
let submitTeamData = () => {
  let form_temp = unref(form_ref);
  form_temp.validate(async (valid: any) => {
    if (valid) {
      let back_data = await teamRegistration({
        team_nick: teamData.team_title,
        team_introduce: teamData.team_introduce || "",
        team_school: teamData.team_school,
        team_teacher: teamData.team_teacher || "",
      });
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        emits("reloadTeamData");
      } else {
        ElMessage({
          type: "error",
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

<style lang="scss" scoped>
.team-registration {
  width: 300px;
}
</style>
