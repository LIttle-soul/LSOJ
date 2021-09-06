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
          user_data.user_power
        }}</el-descriptions-item>
        <el-descriptions-item label="我的积分:">{{
          user_data.user_score
        }}</el-descriptions-item>
        <el-descriptions-item label="我的电话:">{{
          user_data.user_telephone
        }}</el-descriptions-item>
        <el-descriptions-item label="我的邮箱:"
          >{{ user_data.user_email }}
          <el-button size="mini" type="success" @click="dialogBingEmail=true"
            >绑定邮箱</el-button
          >
        </el-descriptions-item>
        <el-descriptions-item label="我的性别:">{{
          user_data.user_sex == 0 ? "男" : "女"
        }}</el-descriptions-item>
        <el-descriptions-item label="我的生日:">{{
          user_data.user_birthday
        }}</el-descriptions-item>
        <el-descriptions-item label="我的注册时间:">{{
          user_data.registration_time
        }}</el-descriptions-item>
        <el-descriptions-item label="我的地址:">{{
          user_data.user_address
        }}</el-descriptions-item>
        <el-descriptions-item label="我的学校:">{{
          user_data.user_school
        }}</el-descriptions-item>
        <el-descriptions-item label="我的学号:">{{
          user_data.student_id
        }}</el-descriptions-item>
        <el-descriptions-item label="我的团队:">{{
          user_data.user_team
        }}
        <el-button size="mini" type="success" @click="dialogBingTeam=true"
            >团队管理</el-button
          >
        </el-descriptions-item>
        <el-descriptions-item label="我的介绍:">{{
          user_data.user_introduce
        }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-dialog
      title="绑定邮箱"
      v-model="dialogBingEmail"
      width="30%"
    >
      <el-input v-model="user_data.user_email"></el-input>
      <template #footer>
          <el-button @click="dialogBingEmail = false">取消</el-button>
          <el-button type="primary" @click="bindUserEmail">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog
      title="团队管理"
      v-model="dialogBingTeam"
      width="50%"
    >
        <el-button type="primary" @click="createTeam">创建队伍</el-button>
        <el-button type="primary" @click="joinTeam">加入队伍</el-button>
        <el-button type="primary" @click="deleteTeam">退出队伍</el-button>
    </el-dialog>
  </div>
</template>

<script>
export default {
  mounted() {},
  setup() {},
  data() {
    return {
      dialogBingEmail: false,
      dialogBingTeam: false,
      user_power_list: ["超级管理员", "管理员", "教师", "志愿者", "普通用户"],
      user_data: {
        user_id: "未完善",
        user_nick: null,
        user_name: null,
        user_power: null,
        user_score: null,
        user_telephone: null,
        user_email: null,
        user_sex: 0,
        user_birthday: null,
        user_address: null,
        user_school: null,
        student_id: null,
        user_team: null,
        user_introduce: null,
        registration_time: null,
      },
    };
  },
  methods: {
    ChangeUserInfo() {
      this.$router.push("/perfectuserinfo");
    },
    InputUserInfo() {
      this.$http({
        url: "/api/user/perfectinfo/",
        methods: "get",
        params: {
          token: this.$cookies.get("token"),
        },
      }).then((res) => {
        // console.log(res.data.data);
        if (res.data.status) {
          this.user_data.user_id = res.data.data.user_id;
          this.user_data.user_nick = res.data.data.user_nick;
          this.user_data.user_name = res.data.data.user_name;
          this.user_data.user_power = this.user_power_list[
            res.data.data.user_power
          ];
          this.user_data.user_score = res.data.data.user_score;
          this.user_data.user_telephone = res.data.data.user_telephone;
          this.user_data.user_email = res.data.data.user_email;
          this.user_data.user_sex = res.data.data.user_sex;
          this.user_data.user_birthday = this.$dayJS(
            res.data.data.user_birthday
          ).format("YYYY-MM-DD");
          this.user_data.user_address =
            res.data.data.user_address.municipality_name;
          this.user_data.user_school = res.data.data.user_school.school_name;
          this.user_data.student_id = res.data.data.student_id;
          this.user_data.user_team = res.data.data.user_team;
          this.user_data.user_introduce = res.data.data.user_introduce;
          this.user_data.registration_time = this.$dayJS(
            res.data.data.registration_time
          ).format("YYYY-MM-DD");
        }
      });
    },
    bindUserEmail() {
      console.log("绑定邮箱");
    },
    createTeam() {
        console.log("create team");
    },
    joinTeam() {
        console.log("join team");
    },
    deleteTeam() {
        console.log("delete team");
    }
  },
};
</script>

<style scoped>
.user-info {
  border-radius: 20px;
  text-align: center;
  font-family: "楷体";
  font-size: 20px;
}
</style>
