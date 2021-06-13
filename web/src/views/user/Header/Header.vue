<template>
  <el-affix :offset="10">
    <el-row
      class='Info'
      type='flex'
      justify='center'
      align='top'
    >
      <el-col
        :xs=3
        :sm=2
        :md=1
        class='hidden-xl-and-up'
      >
        <i class="el-icon-menu"></i>
      </el-col>
      <el-col
        :xs=18
        :sm=20
        :md=22
        class='hidden-sm-and-down'
      >
        2222
      </el-col>
      <el-col
        :xs=3
        :sm=2
        :md=1
      >
        <i class="el-icon-s-custom"></i>
      </el-col>
    </el-row>
  </el-affix>
</template>

<script>
  export default {
    updated() {

    },
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style scope>
.Info {
  flex: inherit;
  background-color: azure;
}
</style>
