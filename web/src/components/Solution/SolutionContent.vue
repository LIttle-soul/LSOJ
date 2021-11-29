<template>
  <div class="solution-content">
    <p>{{ result_data[solution_result.run_result].text }}</p>
    <p>提示信息: {{ solution_result.run_error }}</p>
    <p>正确: {{ solution_result.run_pass_rate }}组数据</p>
    <p>总: {{ solution_result.run_all_rate }}组数据</p>
  </div>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import { mapState, useStore } from "vuex";

let store = useStore();

let props = defineProps({
  solution_result: {
    type: undefined,
    default: {
      run_result: 0,
      run_error: null,
      run_pass_rate: 0,
      run_all_rate: 0,
    },
  },
});
let result_data = computed(
  mapState("code", ["result_data"]).result_data.bind({
    $store: store,
  })
);
</script>

<style scoped lang="scss">
.solution-content {
  padding: 20px;
  line-height: 26px;
  height: 100%;
  background: #d3cce3; /* fallback for old browsers */
  background: -webkit-linear-gradient(
    to right,
    rgb(211, 204, 227),
    rgb(233, 228, 240)
  ); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(
    to right,
    rgb(211, 204, 227),
    rgb(233, 228, 240)
  ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  color: rgba(160, 70, 10);
  font-weight: bold;
  font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
    "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
  p {
    font-size: 20px;
    background-image: #4776e6;
    background-image: -webkit-linear-gradient(
      to right,
      rgb(71, 118, 230),
      rgb(142, 84, 233)
    );
    background-image: linear-gradient(to right, rgb(71, 118, 230), rgb(142, 84, 233));
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
  }
}
</style>
