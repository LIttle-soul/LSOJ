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
      <h3 class="icon">LSOJ</h3>
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
            <router-link v-if="item.sort_index === 8" :to="item.index" @click="logout">
              {{ item.tittle }}
            </router-link>
            <router-link v-else :to="item.index">
              {{ item.tittle }}
            </router-link>
          </el-dropdown-item>
        </template>
      </el-dropdown>
      <div class="header-search">
        <el-input
          class="textarea"
          size="mini"
          prefix-icon="el-icon-search"
        >
        </el-input>
      </div>
    </div>
</template>

<script type="text/javascript">
export default {
  name: "Header",
  mounted() {
    this.getUserProvince();
  },
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
  methods: {
    SelectUserMenu(province) {
      this.userNav = []
      while(province != -1){
        switch (province) {
          case 0:     // 超级管理员菜单列表
            this.userNav.push({ index: "/admin", tittle: "我的管理", sort_index: 1});
            province = 4;
            break;
          case 1:    // 管理员菜单列表
            this.userNav.push({ index: "/home1", tittle: "我的管理", sort_index: 1});
            province = 4;
            break;
          case 2:     // 教师菜单列表
            this.userNav.push({ index: "/home1", tittle: "我的管理", sort_index: 1});
            province = 4;
            break;
          case 3:     // 志愿者菜单列表
            this.userNav.push({ index: "/home1", tittle: "我的管理", sort_index: 1});
            province = 4;
            break;
          case 4:     // 普通用户菜单列表
            this.userNav.push({ index: "/home2", tittle: "我的信息", sort_index: 2});
            this.userNav.push({ index: "/home3", tittle: "我的状态", sort_index: 3});
            this.userNav.push({ index: "/home4", tittle: "我的题解", sort_index: 4});
            this.userNav.push({ index: "/home5", tittle: "我的收藏", sort_index: 5});
            this.userNav.push({ index: "/home6", tittle: "我的比赛", sort_index: 6});
            this.userNav.push({ index: "/home7", tittle: "我的提交", sort_index: 7});
            this.userNav.push({ index: "/home", tittle: "用户注销", sort_index: 8});
            province = -1;
            break;
          default:    // 未登录用户菜单列表
            this.userNav.push({ index: "/login", tittle: "登录", sort_index: 1});
            this.userNav.push({ index: "/forgetpassword", tittle: "忘记密码" , sort_index: 2});
            province = -1;
        }
      }
    },
    getUserProvince() {
      if(this.$cookies.isKey('token')) {
        this.$http({
          url: '/api/getusertokeninfo/',
          methods: 'get',
          params: {
            'token': this.$cookies.get('token')
          }
        }).then( res => {
          // console.log(res.data)
          this.SelectUserMenu(res.data.data.data.capacity)
          if(res.data.remind) {
            this.$cookies.set('token', res.data.new_token)
            console.log('set new token!')
          }
        })
      } else {
        this.SelectUserMenu(5)
      }
    },
    logout() {
      this.$cookies.remove('token');
      location.reload();
    }
  }
};
</script>

<style scope>
a {
  text-decoration: none;
  color: black;
}
.textarea .el-input__inner {
  border-radius: 15px!important; 
  background-color: rgba(240,240,240, 0.9)!important;
}
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
