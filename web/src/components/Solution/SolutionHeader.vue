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

<script lang="ts" setup>
import { ref } from "vue";

let button_status = ref(false);
let emit = defineEmits(["submitData"]);

let submitData = () => {
  button_status.value = true;
  emit("submitData");
  setTimeout(() => {
    button_status.value = false;
  }, 3000);
};
</script>

<style scoped lang="scss">
.solution-header {
  width: 100%;
  height: 100%;
  position: relative;
  .submit-button {
    position: absolute;
    right: 10px;
    top: 8px;
  }
}
</style>
