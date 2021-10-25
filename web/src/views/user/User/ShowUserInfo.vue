<template>
  <div class="show-user-info">
    <div class="user-icon">
      <el-avatar
        shape="square"
        :size="150"
        :fit="fit"
        :src="circleUrl"
      ></el-avatar>
      <el-upload
        action="/api/user/getusericon/"
        name="file"
        :on-success="changeUserIcon"
      >
        <el-button size="mini" type="primary">更换头像</el-button>
      </el-upload>
    </div>
    <UserInfoCard />
  </div>
</template>

<script>
import UserInfoCard from "@/components/User/UserInfoCard.vue";
import { mapState } from "vuex";

export default {
  components: {
    UserInfoCard: UserInfoCard,
  },
  computed: {
    ...mapState("user", {
      user_info: (state) => state.user_info,
    }),
  },
  watch: {
    user_info() {
      this.circleUrl = this.user_info.user_icon
        ? `data:image/png;base64,${this.user_info.user_icon}`
        : "/api/user/getusericon/";
    },
  },
  created() {
    this.circleUrl = this.user_info.user_icon
      ? `data:image/png;base64,${this.user_info.user_icon}`
      : "/api/user/getusericon/";
  },
  data() {
    return {
      fit: "fill",
      circleUrl: "/api/user/getusericon/",
    };
  },
  methods: {
    changeUserIcon() {
      this.$store.dispatch("user/getUserInfo");
      this.$message({
        type: "success",
        message: "上传成功",
      });
    },
  },
};
</script>

<style scoped>
.show-user-info {
  width: 80%;
  max-width: 600px;
  margin: 70px auto;
}
.user-icon {
  width: 150px;
  height: 180px;
  text-align: center;
  margin: 0 auto;
  margin-bottom: 50px;
  /* background-color: rgba(0, 0, 0, 0.1); */
}
.user-icon .el-button {
  margin-top: 10px;
}
</style>
