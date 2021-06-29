<template>
    <div class="nav">
      <el-button
        class="nav-button"
        icon="el-icon-menu"
        circle
        @click="drawer = !drawer"
      ></el-button>
      <el-drawer
        title="LSOJ"
        v-model="drawer"
        :with-header="true"
        direction="ltr"
      >
        <el-menu
          class="nav-menu"
          text-color="#1af"
          active-text-color="#fa1"
          :default-active="$route.path"
          router
        >
          <el-menu-item
            v-for="item in headerNav"
            :key="item.index"
            :index="item.index"
            >{{ item.tittle }}</el-menu-item
          >
        </el-menu>
      </el-drawer>
      <blod class="icon">LSOJ</blod>
      <el-menu
        class="header-menu"
        mode="horizontal"
        text-color="#1af"
        active-text-color="#fa1"
        :default-active="$route.path"
        router
        style="border: none;"
      >
        <el-menu-item
          v-for="item in headerNav"
          :key="item.index"
          :index="item.index"
          >{{ item.tittle }}</el-menu-item
        >
      </el-menu>
      <el-dropdown class="header-head" type="primary" trigger="click">
        <el-avatar :src="circleUrl"></el-avatar>
        <template #dropdown>
          <el-dropdown-item
            v-for="item in userNav"
            :key="item.index"
            :index="item.index"
          >
            <router-link :to="item.index">
              {{ item.tittle }}
            </router-link>
          </el-dropdown-item>
        </template>
      </el-dropdown>
      <div class="header-search">
        <el-input
          size="mini"
          input-style="border-radius: 15px; background-color: rgba(240,240,240, 0.9)"
          prefix-icon="el-icon-search"
        >
        </el-input>
      </div>
    </div>
</template>

<script>
export default {
  name: "Header",
  components: {},
  updated() {},
  data() {
    return {
      circleUrl: "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
      drawer: false,
      headerNav: [
        { index: "/home", tittle: "首页" },
        { index: "/problems", tittle: "问题" },
        { index: "/ranking", tittle: "排名" },
        { index: "/contest", tittle: "竞赛" },
        { index: "/collage", tittle: "闯关" },
      ],
      userNav: [
        { index: "/login", tittle: "登录" },
        { index: "/forgetpassword", tittle: "忘记密码" },
      ],
    };
  },
};
</script>

<style scope>
.nav {
  position: sticky;
  background-color: rgba(50, 50, 50, 0.8);
  width: 100%;
  height: 60px;
  line-height: 60px;
  border-radius: 28px;
  position: relative;
}
.nav-button {
  position: absolute;
  top: 10px;
  left: 20px;
  display: none;
}
.icon {
  font-size: 25px;
  width: 80px;
  color: rgba(0, 0, 0, 0.9);
  font-weight: bolder;
  float: left;
  cursor: pointer;
  position: relative;
  left: 20px;
  font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.header-head {
  position: absolute;
  right: 20px;
  top: 10px;
}
.header-menu {
  margin-left: 20px;
  width: 50%;
  float: left;
  background: none;
}
.nav-menu {
  width: 100%;
  text-align: center;
}
.header-search {
  width: 20%;
  max-width: 200px;
  min-width: 150px;
  position: absolute;
  top: 0px;
  right: 80px;
}

@media screen and (max-width: 750px) {
  .nav-button {
    display: block;
  }
  .header-menu {
    display: none;
  }
  .icon {
    display: none;
  }
}
@media screen and (max-width: 350px) {
  .header-search {
    display: none;
  }
}
</style>
