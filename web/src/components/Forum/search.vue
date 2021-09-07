<template>
  <div>
    <el-input
      placeholder="请输入内容"
      prefix-icon="el-icon-search"
      v-model="input"
      @keyup.enter="search"
    >
    </el-input>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        input: ""
      }
    },

    methods: {
      search() {
        console.log(1);
        
        this.$emit("search", this.input);
        this.input = "";
      }
    }
  }
</script>

<style scoped>
  div {
    width: 300px;
    height: 30px;
    margin: 0 auto;
  }
</style>