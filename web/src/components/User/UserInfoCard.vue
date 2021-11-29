<template>
  <div class="user-info-card">
    <el-card class="user-info">
      <el-descriptions :column="1">
        <template #title>
          <el-icon size="1.6rem"><user /></el-icon>
          用户信息
        </template>
        <template #extra>
          <el-button type="text" size="mini" @click="changeUserInfo">修改信息</el-button>
        </template>
        <el-descriptions-item label="我的账号:">{{
          user_data.user_id
        }}</el-descriptions-item>
        <el-descriptions-item label="我的昵称:">{{
          user_data.user_nick
        }}</el-descriptions-item>
        <el-descriptions-item label="我的姓名:">{{
          user_data.user_name
        }}</el-descriptions-item>
        <el-descriptions-item label="我的身份:">{{
          user_power_list[user_data.user_power]
        }}</el-descriptions-item>
        <el-descriptions-item label="我的积分:">{{
          user_data.user_score
        }}</el-descriptions-item>
        <el-descriptions-item label="我的电话:">{{
          user_data.user_telephone || "未绑定"
        }}</el-descriptions-item>
        <el-descriptions-item label="我的邮箱:"
          >{{ user_data.user_email || "未绑定" }}
          <el-button size="mini" type="success" @click="dialogBingEmail = true"
            >绑定邮箱</el-button
          >
        </el-descriptions-item>
        <el-descriptions-item label="我的性别:">{{
          user_data.user_sex == 0 ? "男" : "女"
        }}</el-descriptions-item>
        <el-descriptions-item label="我的生日:">{{
          dayJS(user_data.user_birthday).format("YYYY年MM月DD日")
        }}</el-descriptions-item>
        <el-descriptions-item label="我的注册时间:">{{
          dayJS(user_data.registration_time).format("YYYY年MM月DD日 HH:mm:ss")
        }}</el-descriptions-item>
        <el-descriptions-item label="我的地址:">{{
          user_data.user_address?.address_name || ""
        }}</el-descriptions-item>
        <el-descriptions-item label="我的学校:">{{
          user_data.user_school?.school_name || ""
        }}</el-descriptions-item>
        <el-descriptions-item label="我的学号:">{{
          user_data.student_id
        }}</el-descriptions-item>
        <el-descriptions-item label="我的团队:"
          >{{ user_data.user_team }}
          <el-button size="mini" type="success" @click="dialogBingTeam = true"
            >团队管理</el-button
          >
        </el-descriptions-item>
        <el-descriptions-item label="我的介绍:">{{
          user_data.user_introduce
        }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-dialog title="绑定邮箱" v-model="dialogBingEmail" width="400px">
      <el-form label-width="80px" :model="email_form" :rules="email_rules">
        <el-form-item label="邮箱" prop="new_email"
          ><el-input v-model="email_form.new_email"></el-input
        ></el-form-item>
        <el-form-item label="验证码"
          ><el-input v-model="email_form.email_code">
            <template #append>
              <el-button
                type="info"
                @click="sendEmail(email_form)"
                :disabled="send_email_button.status"
                style="width: 120px; padding: 0; font-size: 10px"
                >{{ send_email_button.text }}</el-button
              >
            </template>
          </el-input></el-form-item
        >
      </el-form>
      <template #footer>
        <el-button @click="dialogBingEmail = false">取消</el-button>
        <el-button type="primary" @click="bindEmail(email_form)">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog title="团队管理" v-model="dialogBingTeam" width="95%">
      <el-tabs type="border-card" class="team-admin">
        <el-tab-pane label="我创建的团队">
          <TeamList
            :is_delete_power="true"
            :Data="my_create_team_list"
            @reload="getMyTeamList('create')"
          />
        </el-tab-pane>
        <el-tab-pane label="我加入的团队">
          <TeamList :Data="my_join_team_list" @reload="getMyTeamList('join')" />
        </el-tab-pane>
      </el-tabs>
      <el-button type="primary" @click="team_reg = true">创建队伍</el-button>
      <el-button type="primary" @click="joinTeamBox">加入队伍</el-button>
    </el-dialog>
    <el-dialog v-model="team_reg" title="团队注册">
      <teamReg
        @reloadTeamData="
          () => {
            getMyTeamList('create');
            getMyTeamList('join');
            team_reg = false;
          }
        "
      />
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watchEffect, reactive, onMounted } from "vue";
import { useStore, mapGetters, mapState } from "vuex";
import { useRouter } from "vue-router";
import { sendEmailCode, bindUserEmail } from "@/api/user";
import { ElMessage, ElMessageBox } from "element-plus";
import { User } from "@element-plus/icons";
import dayJS from "dayjs";

import teamReg from "@/components/User/TeamRegistration.vue";
import teamList from "@/components/User/TeamList.vue";
import { getTeamList, joinTeamByCode } from "@/api/user";

let store = useStore();
let router = useRouter();

// 数据绑定
let send_email_button = ref({
  status: false,
  text: "获取验证码",
});

let team_reg = ref(false);
let dialogBingEmail = ref(false);
let dialogBingTeam = ref(false);

let user_power_list = ["超级管理员", "管理员", "教师", "志愿者", "普通用户"];
let my_join_team_list = ref([]);
let my_create_team_list = ref([]);

let email_form = ref({
  new_email: "",
  email_code: "",
});

let email_rules = reactive({
  new_email: [
    { required: true, message: "邮箱不能为空", trigger: "blur" },
    { type: "email", message: "邮箱格式错误", trigger: ["blur", "change"] },
  ],
});

// Vuex数据获取
let user_data: any = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);

// console.log(user_data);
let team_list = ref("");

// 事件绑定
let changeUserInfo = () => {
  router.push({ path: "/perfectuserinfo" });
};

let sendEmail = async (form: any) => {
  if (!send_email_button.value.status) {
    send_email_button.value.status = true;
    let back_data = await sendEmailCode({
      email: form.new_email,
    });
    if (back_data.status) {
      ElMessage({
        type: "success",
        message: back_data.message,
      });
      let time_out = 60;
      let inter = setInterval(() => {
        if (time_out > 0) {
          send_email_button.value.text = "请在" + time_out + "秒后再试";
          time_out--;
        } else {
          send_email_button.value.status = false;
          send_email_button.value.text = "获取验证码";
          clearInterval(inter);
        }
      }, 1000);
    } else {
      ElMessage({
        type: "error",
        message: back_data.message,
      });
    }
  }
};

let bindEmail = async (form: any) => {
  // console.log(form);
  let back_data = await bindUserEmail({
    email: form.new_email,
    code: form.email_code,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    store.dispatch("user/getUserInfo");
    dialogBingEmail.value = false;
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};

let joinTeamBox = () => {
  ElMessageBox.prompt("请输入你要加入的团队邀请码", "邀请码加入", {
    confirmButtonText: "提交",
    cancelButtonText: "取消",
  })
    .then(({ value }: any) => {
      joinTeam(value);
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消加入",
      });
    });
};

let formatTeamData = (val: any) => {
  return val.map((item: any) => ({
    team_id: item.team_id,
    team_nick: item.team_nick,
    team_creator: item.team_creator,
    team_user_list: item.user_list,
    team_teacher: item.team_teacher,
    team_school: item.school_name,
    registration_time: dayJS(item.registration_time).format("YYYY-MM-DD HH:mm:ss"),
    team_introduce: item.team_introduce,
    invitation_code: item.invitation_code,
  }));
};

let getMyTeamList = async (val: string) => {
  let back_data = await getTeamList({
    page: 1,
    total: 500,
    text: "",
    mode: val,
  });
  // console.log(back_data);
  if (back_data.status) {
    if (val === "join") {
      my_join_team_list.value = formatTeamData(back_data.message);
    } else if (val === "create") {
      my_create_team_list.value = formatTeamData(back_data.message);
    }
  }
};

let joinTeam = async (val: string) => {
  let back_data = await joinTeamByCode({
    code: val,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    getMyTeamList("join");
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
onMounted(() => {
  getMyTeamList("join");
  getMyTeamList("create");
});
</script>

<style scoped lang="scss">
.user-info {
  border-radius: 20px;
  text-align: left;
  font-family: "楷体";
  font-size: 20px;
}
.team-admin {
  margin-bottom: 30px;
}
</style>
