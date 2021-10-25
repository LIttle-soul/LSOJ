<template>
  <div class="header-nav">
    <el-button
      class="nav-button"
      icon="el-icon-menu"
      circle
      @click="drawer = !drawer"
    ></el-button>
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
      style="border: none;"
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
        prefix-icon="el-icon-search"
        v-model="search_data"
        @keydown.enter="setSearchData(search_data)"
        placeholder="Enter搜索"
      >
      </el-input>
    </div>
  </div>
</template>

<script type="text/javascript">
import { mapState } from "vuex";
import { loadData } from "@/utils/loadData";
import { getMyContest } from "@/api/contest";
export default {
  name: "Header",
  computed: {
    ...mapState("user", {
      headerNav: (state) => state.user_nav,
      userNav: (state) => state.login_nav,
      user_info: (state) => state.user_info,
    }),
    ...mapState("userSettings", {
      web_icon: (state) => state.title,
    }),
  },
  watch: {
    user_info() {
      this.setInfo();
    },
  },
  mounted() {
    this.setInfo();
    // console.log(this.headerNav, this.userNav, this.user_info, this.web_icon);
  },
  data() {
    return {
      search_data: "",
      circleUrl: "/api/user/getusericon/",
      drawer: false,
    };
  },
  methods: {
    async linkTo(val) {
      if (val.name === "Logout") {
        this.$Cookies.remove("token");
        this.$store.commit("user/clearUserInfo");
        loadData();
        console.log("注销成功");
      } else if (val.name === "SolutionList") {
        this.$router.push({
          name: val.name,
          params: { user_id: this.user_info.user_id },
        });
      } else if (val.name === "ContestList") {
        let back_data = await getMyContest();
        if (back_data.status) {
          this.$router.push({
            name: val.name,
            params: { contest_list: back_data.message },
          });
        } else {
          this.$router.push({ name: val.name, params: { contest_list: [] } });
        }
      } else {
        this.$router.push({ name: val.name });
      }
    },
    setSearchData(val) {
      this.$store.commit("set_search_data", val);
    },
    setInfo() {
      let token = this.$Cookies.get("token");
      // console.log(token);
      if (token !== undefined && token !== null) {
        if (this.user_info === null || this.user_info === undefined) {
          this.$store.dispatch("user/getUserInfo");
        } else {
          this.circleUrl = this.user_info.user_icon
            ? `data:image/png;base64,${this.user_info.user_icon}`
            : "/api/user/getusericon/";
        }
        if (this.login_nav === null || this.login_nav === undefined) {
          this.$store.commit("user/setLoginNav");
        }
      } else {
        this.$store.commit("user/clearUserInfo");
        this.$store.commit("user/setLoginNav");
      }
    },
  },
};
</script>

<style scope>
a {
  text-decoration: none;
  color: black;
}
.textarea .el-input__inner {
  border-radius: 15px !important;
  background-color: rgba(250, 250, 250, 0.9) !important;
}
.header-nav {
  position: sticky;
  background-color: rgba(50, 50, 50, 0.8);
  height: 60px;
  line-height: 60px;
  /* border-radius: 28px; */
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
  margin: 0;
  color: rgba(0, 0, 0, 0.9);
  font-weight: bolder;
  float: left;
  cursor: pointer;
  position: relative;
  left: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
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
  border: unset;
}
.header-search {
  width: 20%;
  max-width: 200px;
  min-width: 150px;
  position: absolute;
  top: 0px;
  right: 80px;
}
.el-drawer__body {
  overflow: auto;
  /* overflow-x: auto; */
}
.el-drawer__container ::-webkit-scrollbar {
  display: none;
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
@media screen and (max-width: 350px) {
  .header-search {
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
</style>
