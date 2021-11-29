<template>
  <el-menu
    :collapse="isCollapse"
    :class="{ 'activate-width': !isCollapse }"
    :unique-opened="true"
    :router="true"
    default-active="用户.用户管理"
    collapse-transition
    @select="hasSelect"
  >
    <el-sub-menu v-for="item in nav_menu" :key="item.key" :index="item.key">
      <template #title>
        <el-icon><i :class="item.icon"></i></el-icon>
        <span>{{ item.title }}</span>
      </template>
      <el-menu-item
        v-for="data in item.data"
        :key="data.index"
        :index="data.title"
        :route="{ path: data.src }"
      >
        {{ data.title }}
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import { useStore, mapState } from "vuex";

let store = useStore();

let props = defineProps({
  isCollapse: {
    type: Boolean,
    default: false,
  },
});

let emit = defineEmits(["hasSelect"]);

let nav_menu = computed(mapState("admin", ["nav_menu"]).nav_menu.bind({ $store: store }));

let hasSelect = (index: number, path: string) => {
  emit("hasSelect", path);
};
</script>

<style scoped lang="scss">
.el-menu {
  background: none;
  .el-menu-item {
    min-width: 100px;
  }
}
.activate-width {
  width: 160px;
}
</style>
