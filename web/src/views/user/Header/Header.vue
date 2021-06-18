<template>
  <el-affix :offset="20">
    <div
      style="
        background-color: rgba(50, 50, 50, 0.8);
        height: 61px;
        line-height: 61px;
        border-radius: 28px;
      "
    >
      <el-button
        v-if="Width <= 750"
        icon="el-icon-menu"
        circle
        @click="drawer = !drawer"
        style="margin-left: 20px"
      ></el-button>
      <el-drawer
        title="LSOJ"
        v-model="drawer"
        :with-header="true"
        direction="ltr"
      >
        <el-menu
          text-color="#1af"
          active-text-color="#fa1"
          default-active="home"
          router
          style="width: 100%; text-align: center"
        >
          <el-menu-item
            v-for="item in headerNav"
            :key="item.index"
            :index="item.index"
            >{{ item.tittle }}</el-menu-item
          >
        </el-menu>
      </el-drawer>
      <blod
        v-if="Width > 750"
        style="
          font-size: 25px;
          width: 80px;
          color: black;
          font-weight: bolder;
          cursor: pointer;
          float: left;
          margin-left: 30px;
          font-style: oblique;
          font-family: '楷体';
        "
        >LSOJ</blod
      >
      <el-menu
        v-if="Width > 750"
        mode="horizontal"
        text-color="#1af"
        active-text-color="#fa1"
        default-active="home"
        router
        style="width: 50%; float: left; background: none; border: none"
      >
        <el-menu-item
          v-for="item in headerNav"
          :key="item.index"
          :index="item.index"
          >{{ item.tittle }}</el-menu-item
        >
      </el-menu>
      <el-dropdown
        type="primary"
        trigger="click"
        style="float: right; margin: 11px 20px"
      >
        <el-avatar :src="circleUrl"></el-avatar>
        <template #dropdown>
          <el-dropdown-item
            v-for="item in userNav"
            :key="item.index"
            :index="item.index"
            ><router-link :to="item.index">{{ item.tittle }}</router-link></el-dropdown-item
          >
        </template>
      </el-dropdown>
      <div style="width: 20%; max-width: 200px; min-width: 150px; float: right">
        <el-input
          v-if="Width > 350"
          size="mini"
          input-style="border-radius: 15px; background-color: rgba(240,240,240, 0.9)"
          prefix-icon="el-icon-search"
        >
        </el-input>
      </div>
    </div>
  </el-affix>
</template>

<script>
export default {
  components: {},
  updated() {},
  data() {
    return {
      activeIndex: "1",
      activeIndex2: "1",
      circleUrl:
        "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
      Width: innerWidth,
      drawer: false,
      headerNav: [
        { index: "home", tittle: "首页" },
        { index: "problems", tittle: "问题" },
        { index: "contest", tittle: "竞赛" },
        { index: "collage", tittle: "闯关" },
      ],
      userNav: [
        { index: "login", tittle: "登录" },
        { index: "logout", tittle: "注销" },
      ],
    };
  },
  methods: {},
};
</script>

<style scope>
.Info {
  flex: inherit;
  background-color: azure;
}
</style>
