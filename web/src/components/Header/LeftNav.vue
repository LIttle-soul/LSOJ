<template>
  <el-menu
    :collapse="isCollapse"
    :class="{'activate-width':!isCollapse}"
    :unique-opened="true"
    :router="true"
    default-active="用户.用户管理"
    collapse-transition
    @select='hasSelect'
  >
    <el-sub-menu v-for="item in nav_menu" :key="item.key" :index="item.key">
      <template #title>
        <i :class="item.icon"></i>
        <span>{{ item.title }}</span>
      </template>
      <el-menu-item
        v-for="data in item.data"
        :key="data.index"
        :index="data.title"
        :route="{path: data.src}"
        >
          {{ data.title }}
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    isCollapse: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      nav_menu: state => state.admin.nav_menu
    })
  },
  data() {
    return {
      
    };
  },
  methods: {
    hasSelect(index, path){
      // console.log(index, path);
      this.$emit('hasSelect',path);
    }
  },
};
</script>

<style scoped>
.el-menu {
  background: none;
}
.activate-width {
  width: 160px;
}
.el-menu-item {
  min-width: 100px;
}
</style>
