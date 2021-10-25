<template>
  <div class="contest-join">
    <el-select v-model="team" placeholder="请选择所要报名团队">
      <el-option
        v-for="item in team_list"
        :key="item.team_id"
        :label="item.team_name"
        :value="item.team_id"
      >
      </el-option>
    </el-select>
    <div class="bottom-button">
      <el-button type="primary" @click="JoinByUser">个人报名</el-button>
      <el-button type="primary" @click="JoinByTeam">团队报名</el-button>
      <el-button type="primary" @click="team_reg = true">团队注册</el-button>
    </div>
    <el-dialog v-model="team_reg" title="团队注册" width="400px">
      <TeamReg />
    </el-dialog>
  </div>
</template>
<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { joinContestByUser } from "@/api/contest";

export default {
  components: {
    TeamReg: defineAsyncComponent(() =>
      import("@/components/User/TeamRegistration")
    ),
  },
  props: {
    contest_id: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      team_list: [
        {
          team_id: 1002,
          time_name: "Hello Team",
        },
      ],
      team_reg: false,
      team: null,
    };
  },
  methods: {
    async JoinByUser() {
      let back_data = await joinContestByUser({
        contest_id: this.contest_id,
      });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("contest/getContestList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    JoinByTeam() {
      console.log("join bu team");
    },
  },
};
</script>
<style scoped>
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
