<template>
  <div class="header-nav">
    <el-button class="nav-button" circle @click="drawer = !drawer">
      <el-icon><Menu /></el-icon>
    </el-button>
    <el-drawer
      :title="web_icon"
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
          >{{ item.title }}</el-menu-item
        >
      </el-menu>
    </el-drawer>
    <h3 class="icon">{{ web_icon }}</h3>
    <el-menu
      class="header-menu"
      mode="horizontal"
      text-color="#1af"
      active-text-color="#fa1"
      :default-active="$route.path"
      router
      style="border: none"
    >
      <el-menu-item
        v-for="item in headerNav"
        :key="item.index"
        :index="item.index"
        >{{ item.title }}</el-menu-item
      >
    </el-menu>
    <el-dropdown class="header-head" type="primary" trigger="hover">
      <el-avatar :src="circleUrl"></el-avatar>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            v-for="(item, index) in userNav"
            :key="index"
            @click="linkTo(item)"
            >{{ item.title }}</el-dropdown-item
          >
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="header-search">
      <el-input
        class="textarea"
        size="mini"
        v-model="search_data"
        @keydown.enter="setSearchData(search_data)"
        placeholder="Enter搜索"
      >
        <template #prefix>
          <el-icon
            color="#AAAAAA"
            style="font-size: 1.1rem; transform: translateY(4px)"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              data-v-394d1fd8=""
            >
              <path
                fill="currentColor"
                d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704z"
              ></path>
            </svg>
          </el-icon>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Menu } from "@element-plus/icons";
import { ref, computed, watch, watchEffect } from "vue";
import { useStore, mapState, mapGetters, mapActions, mapMutations } from "vuex";
import { useRouter } from "vue-router";
import cookies from "vue-cookies";
import { ElMessage } from "element-plus";
import { getMyContest } from "@/api/contest";
const router = useRouter();

// 获取vuex中数据
const store = useStore();
const headerNav = computed(
  mapState("user", ["user_nav"]).user_nav.bind({ $store: store })
);
const userNav = computed(
  mapState("user", ["login_nav"]).login_nav.bind({ $store: store })
);
const user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);
const login_status = computed(
  mapState("user", ["has_login"]).has_login.bind({ $store: store })
);

// 数值绑定
let drawer = ref(false);
let web_icon = ref("LSOJ");
let search_data = ref("");
let circleUrl = ref("");

// 数据监听
watchEffect(() => {
  circleUrl.value = user_info.value?.user_icon
    ? `data:image/png;base64,${user_info.value.user_icon}`
    : "https://tse3-mm.cn.bing.net/th/id/OIP-C.CBSLTkaar6S3UeNVGnZpXgHaHa?pid=ImgDet&rs=1";
  if (login_status.value && !user_info.value) {
    router.push({ path: "/perfectuserinfo" });
  }
});

// 全局搜索
let setSearchData = (val: String) => {
  store.commit("set_search_data", val);
  search_data.value = "";
};

// 路由跳转
let linkTo = async (val: any) => {
  if (val.name === "Logout") {
    router.push({ path: "/home" });
    ElMessage({
      type: "success",
      message: "注销成功",
    });
    setTimeout(() => {
      store.commit("user/logout");
    }, 500);
  } else if (val.name === "SolutionList") {
    router.push({
      name: val.name,
      params: { user_id: user_info.value.user_id },
    });
  } else if (val.name === "ContestList") {
    let back_data = await getMyContest();
    if (back_data.status) {
      router.push({
        name: val.name,
        params: { me: "True" },
      });
    } else {
      router.push({ name: val.name, params: { contest_list: [] } });
    }
  } else if (val.name === "MyCourseList") {
    // console.log(val)
    router.push({
      name: "WeCourseHomeMyCourseList",
    });
  } else {
    router.push({ name: val.name });
  }
};

// 检查缓存的数据信息是否有效
let token = cookies.get("token");
if (token !== undefined && token !== null) {
  if (user_info.value === null || user_info.value === undefined) {
    store.dispatch("user/getUserInfo");
  }
  if (userNav.value === null || userNav.value === undefined) {
    store.commit("user/setLoginNav");
  }
} else {
  store.commit("user/logout");
}
</script>

<style scope lang="scss">
.header-nav {
  background-color: rgba(100, 100, 100);
  height: 60px;
  line-height: 60px;
  position: relative;
  top: 0;
  width: 100%;
  min-width: 800px;
  z-index: 100;
  box-shadow: 0px 3px 5px #aaa;
  border-radius: 0 0 25px 25px;
  .nav-button {
    position: absolute;
    top: 10px;
    left: 20px;
    display: none;
  }
  .el-drawer__body {
    overflow: auto;
  }
  .el-drawer__container ::-webkit-scrollbar {
    display: none;
  }
  .nav-menu {
    width: 100%;
    text-align: center;
    border: unset;
  }
  .icon {
    font-size: 25px;
    width: 80px;
    margin: 0;
    color: rgba(0, 0, 0, 0.9);
    font-weight: bolder;
    float: left;
    cursor: pointer;
    position: relative;
    left: 20px;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }
  .header-menu {
    margin-left: 20px;
    width: 50%;
    float: left;
    background: none;
  }
  .header-head {
    position: absolute;
    right: 20px;
    top: 10px;
  }
  .header-search {
    width: 20%;
    max-width: 200px;
    min-width: 150px;
    position: absolute;
    top: 0px;
    right: 80px;
  }
  .textarea {
    .el-input__inner {
      border-radius: 15px;
      background-color: rgba(250, 250, 250, 0.9);
    }
  }
  @media screen and (max-width: 1000px) {
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
  @media screen and (max-height: 400px) {
    .header-nav {
      background: none;
    }
    .header-search {
      display: none;
    }
  }
}
</style>
