<template>
  <div class="solution-content">
    <p>{{ filter_result_data[solution_result.run_result].text }}</p>
    <p>提示信息: {{ solution_result.run_error }}</p>
    <p>正确: {{ solution_result.run_pass_rate }}组数据</p>
    <p>总: {{ solution_result.run_all_rate }}组数据</p>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    solution_result: {
      type: undefined,
      default: {
        run_result: 0,
        run_error: null,
        run_pass_rate: 0,
        run_all_rate: 0,
      },
    },
  },
  computed: {
    ...mapState("code", {
      filter_result_data: (state) => state.filter_result_data,
      //   filter_language_data: (state) => state.filter_language_data,
    }),
  },
};
</script>

<style scoped>
.solution-content {
  padding: 20px;
  line-height: 26px;
}
</style>
