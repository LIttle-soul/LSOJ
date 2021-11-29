<template>
  <div class="problem-header">
    <div class="left">
      <div class="left-text">
        <el-icon :size="30" class="icon"><management /></el-icon>{{ props.problem_title }}
      </div>
      <div class="left-info">
        <p>时间限制: {{ props.time_limit }}ms</p>
        <p>空间限制：{{ props.memory_limit }}mb</p>
      </div>
    </div>
    <div class="right">
      <el-button
        v-show="!(props.contest_id && props.contest_id !== -1)"
        type="text"
        @click="routerTo('ProblemList')"
        >返回列表</el-button
      >
      <el-button
        v-show="!(props.contest_id && props.contest_id !== -1)"
        type="text"
        @click="routerTo('SolutionList')"
        >我的提交</el-button
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { useStore, mapState } from "vuex";
import { useRouter } from "vue-router";
import { Management } from "@element-plus/icons";

let store = useStore();
let router = useRouter();

let user_info = computed(
  mapState("user", ["user_info"]).user_info.bind({ $store: store })
);

let user_id = user_info.value?.user_id || "";

let props = defineProps({
  problem_title: {
    type: String,
    default: "背包问题",
  },
  problem_id: {
    type: Number,
    default: -1,
  },
  contest_id: {
    type: Number,
    default: -1,
  },
  time_limit: {
    type: Number,
    default: 1000,
  },
  memory_limit: {
    type: Number,
    default: 128,
  },
});

let routerTo = (val: any) => {
  if (val === "SolutionList") {
    router.push({
      name: val,
      params: { user_id: user_id, problem_id: props.problem_id },
    });
  } else {
    router.push({
      name: val,
    });
  }
};
</script>

<style scoped lang="scss">
.problem-header {
  width: 100%;
  height: 100%;
  display: flex;
  .left {
    // background: #aaa;
    width: 60%;
    height: 50px;
    display: flex;
    font-family: "楷体";
    color: aliceblue;
    text-align: left;

    .left-text {
      // background: #aa6;
      width: 60%;
      min-width: auto;
      height: 50px;
      line-height: 50px;
      font-size: 18px;
      .icon {
        color: #fff;
        transform: translateY(8px);
      }
    }
    .left-info {
      height: 25px;
      line-height: 20px;
      padding: 5px 0;
    }
  }
  .right {
    // background: #660099;
    width: 40%;
    height: 100%;
    line-height: 100%;
    color: #fff;
    .el-button {
      float: right;
      font-size: 18px;
      font-family: "宋体";
      color: aliceblue;
      margin-right: 20px;
    }
  }
}
</style>
