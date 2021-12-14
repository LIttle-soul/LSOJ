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
        <el-select
          v-model="teamData.team_teacher"
          :multiple="true"
          :filterable="true"
          :remote="true"
          :reserve-keyword="true"
          placeholder="请输入你的指导老师"
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
      <el-form-item label="学校" prop="team_school">
        <el-select
          v-model="teamData.team_school"
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

// 数据获取懒加载
let school_list = ref({
  options: <any>[],
  loading: false,
});
let people_list = ref({
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
