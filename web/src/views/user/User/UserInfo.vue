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
        :data="upload_icon_data"
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

export default {
  components: {
    UserInfoCard: UserInfoCard,
  },
  mounted() {
    this.getUserIcon();
  },
  data() {
    return {
      fit: "fill",
      circleUrl:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      upload_icon_data: {
        token: this.$cookies.get("token"),
      },
    };
  },
  methods: {
    getUserIcon() {
      this.$http({
        url: "/api/user/getusericon/",
        method: "get",
        params: {
          token: this.$cookies.get("token"),
        },
      }).then((res) => {
        // console.log(res.data)
        this.circleUrl = "data:image/png;base64," + res.data.img;
      });
    },
    changeUserIcon() {
      this.$message({
        type: "success",
        message: "上传成功",
      });
      location.reload();
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
