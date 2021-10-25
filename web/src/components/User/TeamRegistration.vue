<template>
  <div class="team-registration">
    <el-form>
      <el-form-item label="团队名称">
        <el-input v-model="teamData.team_title"></el-input>
      </el-form-item>
      <el-form-item label="团队介绍">
        <el-input type="textarea" v-model="teamData.team_introduce"></el-input>
      </el-form-item>
      <el-form-item
        v-for="(item, index) in teamData.team_user_list"
        :key="index"
        :label="'成员' + (index + 1)"
      >
        <el-select v-model="item.user_id" filterable placeholder="Select">
          <el-option
            v-for="item2 in user_list"
            :key="item2.user_id"
            :label="item2.user_id"
            :value="item2.user_id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="指导老师">
        <el-select
          v-model="teamData.team_teacher"
          filterable
          placeholder="Select"
        >
          <el-option
            v-for="item in user_list"
            :key="item.user_id"
            :label="item.user_id"
            :value="item.user_id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="学校">
        <el-select
          v-model="teamData.team_school"
          filterable
          placeholder="Select"
        >
          <el-option
            v-for="item in school_list"
            :key="item.school_id"
            :label="item.school_name"
            :value="item.school_id"
          ></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div class="bottom-button">
      <el-button type="primary" size="medium" @click="submitTeamData(teamData)"
        >提交</el-button
      >
      <el-button
        type="danger"
        size="medium"
        style="float: right"
        @click="deleteTeamUser"
        >删除成员</el-button
      >
      <el-button
        type="success"
        size="medium"
        style="float: right;"
        @click="addTeamUser"
        >添加成员</el-button
      >
    </div>
  </div>
</template>

<script>
import { teamRegistration } from "@/api/user";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("user", {
      user_list: (state) => state.user_list,
    }),
    ...mapState("school", {
      school_list: (state) => state.school_list,
    }),
  },
  data() {
    return {
      teamData: {
        team_title: "",
        team_introduce: "",
        team_school: "",
        team_user_list: new Array({ user_id: "" }),
        team_teacher: "",
        team_type: "",
      },
    };
  },
  methods: {
    async submitTeamData(val) {
      let back_data = await teamRegistration(val);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getTeamList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    addTeamUser() {
      this.teamData.team_user_list.push({ user_id: "" });
    },
    deleteTeamUser() {
      this.teamData.team_user_list.pop();
    },
  },
};
</script>
