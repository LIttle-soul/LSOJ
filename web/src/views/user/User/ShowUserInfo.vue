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

<script lang="ts" setup>
import UserInfoCard from "@/components/User/UserInfoCard.vue";
import { computed, ref, watchEffect } from "vue";
import { useStore, mapState } from "vuex";
import { ElMessage } from "element-plus";

// 数据绑定
let fit = ref("fill");
let circleUrl = ref("");

let store = useStore();

// vuex数据获取
let user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);

// 改变头像
let changeUserIcon = () => {
  store.dispatch("user/getUserInfo");
  ElMessage({
    type: "success",
    message: "上传成功",
  });
};

// 数据监听
watchEffect(() => {
  circleUrl.value = user_info.value?.user_icon
    ? `data:image/png;base64,${user_info.value.user_icon}`
    : "https://tse3-mm.cn.bing.net/th/id/OIP-C.CBSLTkaar6S3UeNVGnZpXgHaHa?pid=ImgDet&rs=1";
});
</script>

<style scoped lang="scss">
.show-user-info {
  width: 80%;
  max-width: 600px;
  margin: 70px auto;
  .user-icon {
    width: 150px;
    height: 180px;
    text-align: center;
    margin: 0 auto;
    margin-bottom: 50px;
    /* background-color: rgba(0, 0, 0, 0.1); */
    .el-button {
      margin-top: 10px;
    }
  }
}
</style>
