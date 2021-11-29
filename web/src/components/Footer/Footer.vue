<template>
  <div class="web-footer">
    <div class="left-content">
      <span><img :src="school_log" alt="" /></span>
      <span><img :src="school_code" alt="" /></span>
      <span class="introduce" v-html="introduce"></span>
    </div>
    <div class="right-content">
      <p class="el-footer-right">
        <router-link
          v-for="item in nav_list"
          :key="item.index"
          :to="{ name: 'About', params: { filer: item.src } }"
        >
          | {{ item.title }}
        </router-link>
        |
      </p>
      <p class="el-footer-right" v-html="put_on_file"></p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import school_log from "@/assets/icon/schoolLogo.jpg?url";
import school_code from "@/assets/icon/QRcode.png?url";
const introduce = "在52AC，<br> 享受AC的快乐";
const src = "about";
const put_on_file =
  "2018-2021 , 52AC © Developed by the JhcOJ Team <br> 浙ICP备18051217号-1 All rights reserved.";
const nav_list = [
  {
    index: 1,
    title: "关于52AC",
    src: "About52AC",
  },
  {
    index: 2,
    title: "帮助中心",
    src: "HelpCenter",
  },
  {
    index: 3,
    title: "用户协议",
    src: "UserAgreement",
  },
  {
    index: 4,
    title: "联系我们",
    src: "ContactUs",
  },
];
</script>

<style scoped lang="scss">
.web-footer {
  height: 127px;
  background: #333333;
  // min-width: 800px;
  display: flex;
  .left-content {
    width: 50%;
    height: 100%;
    line-height: 100%;
    /* border-right: 1px solid #ffffff; */
    text-align: center;
    img {
      width: 80px;
      height: 80px;
      margin-top: 20px;
      margin-right: 20px;
    }
    .introduce {
      width: 50%;
      float: left;
      font-family: "楷体";
      font-size: 30px;
      line-height: 40px;
      margin-top: 20px;
      color: #ffffff;
    }
    @media screen and (max-width: 850px) {
      .introduce {
        display: none;
      }
    }
  }
  .right-content {
    width: 50%;
    color: rgba(255, 255, 255, 0.9);
    height: 60%;
    margin-top: 20px;
    text-align: center;
    p {
      line-height: 2em;
      font-size: 12px;
      margin: 0;
      .router-link-active {
        text-decoration: none;
      }
    }
    a {
      text-decoration: none;
      color: rgba(255, 255, 255, 0.9);
    }
  }

  @media screen and (max-width: 600px) {
    .left-content {
      display: none;
    }
    .right-content {
      width: 100%;
      text-align: center;
    }
  }
}
</style>
