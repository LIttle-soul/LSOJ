<template>
  <div id="app">
    <router-view ></router-view>
  </div>
</template>

<script>
// import { ref, nextTick, provide } from "vue";
// import BLank from "@/components/BLank.vue";
export default {
  name: "App",
  components: {
    // BLank,
  },
  created() {
    // this.$store.commit('getUserData');
    //在页面加载时读取sessionStorage里的状态信息
    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(sessionStorage.getItem('store'))));
    }

    //在页面刷新时将vuex里的信息保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state));
    });
  },
  mounted() {
  },
  data() {
    return {
      isRouterAlive: true
    }
  },
  methods: {
  }
  // setup() {
  //   // 局部组件刷新
  //   const isRouterAlive = ref(true);
  //   const reload = () => {
  //     isRouterAlive.value = false;
  //     nextTick(() => {
  //       isRouterAlive.value = true;
  //     });
  //   };
  //   provide("reload", reload);

  //   return {
  //     isRouterAlive,
  //   };
  // },
};
</script>

<style>
@import url('./assets/css/reset.css');

#app {
  position: relative;
  height: 100%;
}
</style>