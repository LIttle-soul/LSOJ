<template>
  <div class="user-info-card">
    <el-card class="user-info">
      <el-descriptions :column="1">
        <template #title>
          <i class="el-icon-user-solid"></i>
          用户信息
        </template>
        <template #extra>
          <el-button type="text" size="mini" @click="ChangeUserInfo"
            >修改信息</el-button
          >
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
          user_data.user_telephone
        }}</el-descriptions-item>
        <el-descriptions-item label="我的邮箱:"
          >{{ user_data.user_email }}
          <el-button size="mini" type="success" @click="dialogBingEmail = true"
            >绑定邮箱</el-button
          >
        </el-descriptions-item>
        <el-descriptions-item label="我的性别:">{{
          user_data.user_sex == 0 ? "男" : "女"
        }}</el-descriptions-item>
        <el-descriptions-item label="我的生日:">{{
          this.$dayJS(user_data.user_birthday).format("YYYY年MM月DD日")
        }}</el-descriptions-item>
        <el-descriptions-item label="我的注册时间:">{{
          this.$dayJS(user_data.registration_time).format(
            "YYYY年MM月DD日 HH:mm:ss"
          )
        }}</el-descriptions-item>
        <el-descriptions-item label="我的地址:">{{
          user_data.user_address ? user_data.user_address.address_name : ""
        }}</el-descriptions-item>
        <el-descriptions-item label="我的学校:">{{
          user_data.user_school ? user_data.user_school.school_name : ""
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
      <el-form label-width="80px">
        <el-form-item label="邮箱"
          ><el-input v-model="user_data.user_email"></el-input
        ></el-form-item>
        <el-form-item label="验证码"
          ><el-input v-model="email_code">
            <template #append>
              <el-button
                type="info"
                @click="sendEmail(user_data.user_email)"
                :disabled="send_email_button.status"
                style="width: 120px; padding: 0; font-size: 10px;"
                >{{ send_email_button.text }}</el-button
              >
            </template>
          </el-input></el-form-item
        >
      </el-form>
      <template #footer>
        <el-button @click="dialogBingEmail = false">取消</el-button>
        <el-button type="primary" @click="bindUserEmail(user_data.user_email)"
          >确定</el-button
        >
      </template>
    </el-dialog>
    <el-dialog title="团队管理" v-model="dialogBingTeam" width="95%">
      <el-tabs type="border-card" class="team-admin">
        <el-tab-pane label="我创建的团队">
          <TeamList :is_delete_power="true" :Data="my_create_team_list" />
        </el-tab-pane>
        <el-tab-pane label="我加入的团队">
          <TeamList :Data="my_join_team_list" />
        </el-tab-pane>
      </el-tabs>
      <el-button type="primary" @click="team_reg = true">创建队伍</el-button>
      <el-button type="primary" @click="joinTeam">加入队伍</el-button>
      <el-dialog v-model="team_reg" title="团队注册" width="400px">
        <TeamReg />
      </el-dialog>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { defineAsyncComponent } from "@vue/runtime-core";
import { sendEmailCode, bindUserEmail } from "@/api/user";
export default {
  components: {
    TeamReg: defineAsyncComponent(() =>
      import("@/components/User/TeamRegistration")
    ),
    TeamList: defineAsyncComponent(() => import("@/components/User/TeamList")),
  },
  computed: {
    ...mapState("user", {
      user_data: (state) => state.user_info,
      team_list: (state) => state.team_list,
    }),
    ...mapGetters("user", {
      getMyCreateTeamList: "getMyCreateTeamList",
      getMyJoinTeamList: "getMyJoinTeamList",
    }),
  },
  watch: {
    team_list() {
      this.my_join_team_list = this.formatTeamData(this.getMyJoinTeamList());
      this.my_create_team_list = this.formatTeamData(
        this.getMyCreateTeamList()
      );
    },
  },
  created() {
    this.my_join_team_list = this.formatTeamData(this.getMyJoinTeamList());
    this.my_create_team_list = this.formatTeamData(this.getMyCreateTeamList());
  },
  data() {
    return {
      email_code: "",
      send_email_button: {
        status: false,
        text: "获取验证码",
      },
      team_reg: false,
      dialogBingEmail: false,
      dialogBingTeam: false,
      user_power_list: ["超级管理员", "管理员", "教师", "志愿者", "普通用户"],
      my_join_team_list: [],
      my_create_team_list: [],
    };
  },
  methods: {
    ChangeUserInfo() {
      this.$router.push("/perfectuserinfo");
    },
    async sendEmail(user_email) {
      this.send_email_button.status = true;
      let back_data = await sendEmailCode({
        email: user_email,
      });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        let time_out = 60;
        let inter = setInterval(() => {
          this.send_email_button.text = "请在" + time_out + "秒后再试";
          time_out--;
          if (time_out <= 0) {
            this.send_email_button.status = false;
            this.send_email_button.text = "获取验证码";
            clearInterval(inter);
          }
        }, 1000);
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async bindUserEmail(user_email) {
      let back_data = await bindUserEmail({
        email: user_email,
        code: this.email_code,
      });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getUserInfo");
        this.dialogBingEmail = false;
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    joinTeam() {
      console.log("join team");
    },
    deleteTeam() {
      console.log("delete team");
    },
    formatTeamData(val) {
      // console.log(val);
      return val.map((item) => ({
        team_id: item.class_id,
        team_nick: item.class_name,
        team_creator: item.class_creator,
        team_user_list: item.user_list,
        team_school: item.class_college,
        team_type: item.class_type,
        registration_time: this.$dayJS(item.create_time).format(
          "YYYY-MM-DD HH:mm:ss"
        ),
        team_introduce: item.class_introduce,
      }));
    },
  },
};
</script>

<style scoped>
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
