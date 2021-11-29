<template>
  <div class="contest-join">
    <el-form label-width="80px">
      <el-form-item label="团队">
        <el-select
          v-model="team"
          :filterable="true"
          :remote="true"
          :remote-method="searchTeamList"
          :loading="loading"
          placeholder="请输入所要报名团队"
        >
          <el-option
            v-for="item in team_list"
            :key="item.team_id"
            :label="item.team_name"
            :value="item.team_id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          type="password"
          v-model="password"
          input-style="width: 208px;"
        ></el-input>
      </el-form-item>
    </el-form>
    <div class="bottom-button">
      <el-button type="primary" @click="JoinByUser">个人报名</el-button>
      <el-button type="primary" @click="JoinByTeam">团队报名</el-button>
      <el-button type="primary" @click="JoinByPassword">密码加入</el-button>
    </div>
  </div>
</template>
<script lang="ts" setup>
import {
  joinContestByUser,
  joinContestByTeam,
  joinContestByPassword,
} from "@/api/contest";
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import { getTeamList } from "@/api/user";

let store = useStore();

let prop = defineProps({
  contest_id: {
    type: Number,
    default: -1,
  },
});
let team = ref();
let password = ref("");
let loading = ref(false);
let team_list = ref<any>([]);
// 筛选团队列表
let searchTeamList = async (val: any) => {
  console.log(val);
  if (val !== "") {
    loading.value = true;
    let back_data = await getTeamList({
      page: 1,
      total: 20,
      text: val,
      mode: "join",
    });
    console.log(back_data);
    if (back_data.status) {
      team_list.value = formatTeamList(back_data.message);
      loading.value = false;
    } else {
      team_list.value = [];
      loading.value = false;
    }
  } else {
    team_list.value = [];
    loading.value = false;
  }
};

// 格式化团队列表
let formatTeamList = (val: any) => {
  return val.map((item: any) => ({
    team_id: item.team_id,
    team_name: item.team_nick,
  }));
};

// 事件处理
let emit = defineEmits(["reload"]);
let JoinByUser = async () => {
  let back_data = await joinContestByUser({
    contest_id: prop.contest_id,
  });
  if (back_data.status) {
    emit("reload");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let JoinByTeam = async () => {
  let back_data = await joinContestByTeam({
    contest_id: prop.contest_id,
    team_id: team.value,
  });
  if (back_data.status) {
    emit("reload");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let JoinByPassword = async () => {
  let back_data = await joinContestByPassword({
    contest_id: prop.contest_id,
    password: password.value,
  });
  if (back_data.status) {
    emit("reload");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
</script>
<style scoped lang="scss">
.contest-join {
  width: 100%;
  height: 100%;
}
.bottom-button {
  width: 100%;
  margin-top: 30px;
  display: flex;
}
</style>
