<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
// import { ref, nextTick, provide } from "vue";
// import BLank from "@/components/BLank.vue";
import { loadData } from "@/utils/loadData";

export default {
  name: "App",
  components: {
    // BLank,
  },
  beforeCreate() {
    loadData();
  },
  mounted() {},
  data() {
    return {
      isRouterAlive: true,
    };
  },
  computed: {},
  methods: {},
};
</script>

<style>
@import url("./assets/css/reset.css");

#app {
  position: relative;
  height: 100%;
}
</style>
