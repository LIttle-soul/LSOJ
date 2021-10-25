<template>
  <div class="solution-header">
    <el-button
      @click="submitData"
      size="mini"
      type="success"
      class="submit-button"
      :disabled="button_status"
      >提交</el-button
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      button_status: false,
    };
  },
  methods: {
    submitData() {
      this.button_status = true;
      this.$emit("submitData");
      setTimeout(() => {
        this.button_status = false;
      }, 3000);
    },
  },
};
</script>

<style scoped>
.solution-header {
  width: 100%;
  height: 100%;
  position: relative;
}
.submit-button {
  position: absolute;
  right: 10px;
  top: 8px;
}
</style>
