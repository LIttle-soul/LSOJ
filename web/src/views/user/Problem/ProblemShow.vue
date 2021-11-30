<template>
  <div class="problem-show">
    <div class="header">
      <ProblemHeader
        :problem_title="problem_data.problem_title"
        :time_limit="problem_data.time_limit"
        :memory_limit="problem_data.memory_limit"
        :problem_id="submit_data.problem_id"
        :contest_id="submit_data.contest_id"
      />
    </div>
    <div class="content" ref="Content_ref">
      <div class="left" ref="Left_ref">
        <ProblemChild
          mode="preview"
          height="100%"
          :content="problem_data.problem_description"
        />
      </div>
      <div
        class="left-right"
        ref="LeftRight_ref"
        @mouseenter="hadelLeftRightEnter"
        @mouseleave="hadelLeftRightLevel"
        @mousedown="hadelLeftRightDown"
      >
        <button
          class="left-button"
          @click="hadelLeftButtonClick"
          ref="LeftRightLeftButton_ref"
        >
          <el-icon :size="16"><caret-left /></el-icon>
        </button>
        <button
          class="right-button"
          @click="hadelRightButtonClick"
          ref="LeftRightRightButton_ref"
        >
          <el-icon :size="16"><caret-right /></el-icon>
        </button>
        ⋮
      </div>
      <div class="right" ref="Right_ref">
        <div class="code" ref="Code_ref">
          <div class="code-header">
            <CodeHeader @changeLanguage="hadelChangeLanguage" />
          </div>
          <div class="code-content">
            <CodeEditor
              :language="submit_data.solution_language.code"
              ref="codeEditor_ref"
            />
          </div>
          <button
            class="info-style-button"
            @mousedown="hadelInfoButtonDown"
            ref="InfoStyleButton_ref"
          >
            <el-icon :size="16"><d-caret /></el-icon>
          </button>
        </div>
        <div class="info" ref="Info_ref">
          <div class="info-header">
            <SolutionHeader @submitData="submitData" />
          </div>
          <div class="info-content">
            <SolutionContent :solution_result="solution_result" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onUnmounted, reactive, ref, unref } from "vue";
import { mapGetters } from "vuex";
import { ElMessage } from "element-plus";
import { submitCode, getSolutionData } from "@/api/solution";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { DCaret, CaretLeft, CaretRight } from "@element-plus/icons";

import ProblemHeader from "@/components/Problem/ProblemHeader.vue";
import ProblemChild from "@/components/Editor/MarkdownEditor.vue";
import CodeEditor from "@/components/Editor/CodeEditor.vue";
import CodeHeader from "@/components/Editor/CodeHeader.vue";
import SolutionHeader from "@/components/Solution/SolutionHeader.vue";
import SolutionContent from "@/components/Solution/SolutionContent.vue";
import TempProblem from "@/assets/markdown/ProblemTemplet.md?raw";

let route = useRoute();

// console.log(route.query);

let left_right_open = ref(true);
let solution_result = ref({
  run_result: 0,
  run_error: null,
  run_pass_rate: 0,
  run_all_rate: 0,
});
let problem_data = reactive({
  problem_title: unescape(<string>route.query.problem_title) || "问题模板",
  problem_description: unescape(<string>route.query.problem_description) || TempProblem,
  time_limit: Number(route.query.time_limit) || 0,
  memory_limit: Number(route.query.memory_limit) || 0,
});
let submit_data = reactive({
  problem_id: Number(route.query.problem_id) || 0,
  solution_language: { value: 0, text: "C", code: "c" },
  solution_code: "",
  level_id: route.query.level_id || "",
  contest_id: Number(route.query.contest_id) || -1,
});

let codeEditor_ref = ref();

let hadelChangeLanguage = (val: any) => {
  submit_data.solution_language = val;
};
let inter: NodeJS.Timer;
let submitData = async () => {
  // console.log("获取值父组件");
  var editor = unref(codeEditor_ref);
  submit_data.solution_code = editor.getVal();
  // console.log(submit_data);
  let back_data = await submitCode({
    problem_id: submit_data.problem_id,
    solution_language: submit_data.solution_language.value,
    solution_code: submit_data.solution_code,
    level_id: submit_data.level_id || "",
    contest_id: submit_data.contest_id || -1,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    inter = setInterval(async () => {
      let val = await getSolutionData({
        solution_id: back_data.solution_id,
      });
      if (val.status) {
        solution_result.value = val.message;
        if (val.message.run_result > 3) {
          clearInterval(inter);
        }
      }
    }, 2000);
  } else {
    ElMessage({
      type: "warning",
      message: back_data.message,
    });
  }
};
onUnmounted(() => {
  clearInterval(inter);
});

// 样式操作相关函数
let Content_ref = ref();
let Left_ref = ref();
let LeftRight_ref = ref();
let LeftRightLeftButton_ref = ref();
let LeftRightRightButton_ref = ref();
let Right_ref = ref();
let Code_ref = ref();
let InfoStyleButton_ref = ref();
let Info_ref = ref();

let hadelLeftRightEnter = () => {
  let LeftRightRightButton = unref(LeftRightRightButton_ref);
  let LeftRightLeftButton = unref(LeftRightLeftButton_ref);
  left_right_open.value
    ? (LeftRightRightButton.style.display = "inline")
    : (LeftRightLeftButton.style.display = "inline");
};
let hadelLeftRightLevel = () => {
  let LeftRightRightButton = unref(LeftRightRightButton_ref);
  let LeftRightLeftButton = unref(LeftRightLeftButton_ref);
  LeftRightRightButton.style.display = "none";
  LeftRightLeftButton.style.display = "none";
};
let hadelLeftRightDown = (e: any) => {
  let Left = unref(Left_ref);
  let Right = unref(Right_ref);
  let LeftRight = unref(LeftRight_ref);
  let Content = unref(Content_ref);
  LeftRight.style.background = "#818181";
  let startX = e.clientX;
  let left_width = LeftRight.offsetLeft;
  document.onmousemove = (e) => {
    let endX = e.clientX;
    let moveLen = left_width + (endX - startX);
    let maxT = Content.clientWidth - LeftRight.offsetWidth;
    if (moveLen < 50) {
      Left.style.display = "none";
      moveLen = 0;
    } else if (moveLen > maxT - 100) {
      Right.style.display = "none";
      left_right_open.value = false;
      moveLen = maxT;
    } else {
      left_right_open.value = true;
      Right.style.display = "inline";
      Left.style.display = "inline";
    }
    let temp = (moveLen * 100) / Content.clientWidth;
    Left.style.width = temp + "%";
    Right.style.width = 100 - temp + "%";
  };
  document.onmouseup = () => {
    LeftRight.style.background = "#d6d6d6";
    document.onmousemove = null;
    document.onmouseup = null;
    LeftRight.releaseCapture && LeftRight.releaseCapture();
  };
  LeftRight.setCapture && LeftRight.setCapture();
  return false;
};
let hadelLeftButtonClick = () => {
  let Left = unref(Left_ref);
  let Right = unref(Right_ref);
  left_right_open.value = true;
  Left.style.width = "50%";
  Right.style.width = "50%";
  Right.style.display = "inline";
};
let hadelRightButtonClick = () => {
  let Left = unref(Left_ref);
  let Right = unref(Right_ref);
  left_right_open.value = false;
  Left.style.width = "100%";
  Right.style.width = "50%";
  Right.style.display = "none";
};
let hadelInfoButtonDown = (e: any) => {
  let Right = unref(Right_ref);
  let Code = unref(Code_ref);
  let InfoStyleButton = unref(InfoStyleButton_ref);
  let Info = unref(Info_ref);
  InfoStyleButton.style.background = "#818181";
  let startY = e.clientY;
  let top_height = Code.clientHeight;
  document.onmousemove = (e) => {
    let endY = e.clientY;
    let moveLen = top_height + (endY - startY);
    let maxT = Right.clientHeight;
    if (moveLen < 90) {
      moveLen = 90;
    } else if (moveLen > maxT - 45) {
      moveLen = maxT - 45;
    }
    let temp = (moveLen * 100) / Right.clientHeight;
    Code.style.height = temp + "%";
    Info.style.height = 100 - temp + "%";
  };
  document.onmouseup = () => {
    InfoStyleButton.style.background = "#dddddd";
    document.onmousemove = null;
    document.onmouseup = null;
    InfoStyleButton.releaseCapture && InfoStyleButton.releaseCapture();
  };
  InfoStyleButton.setCapture && InfoStyleButton.setCapture();
  return false;
};
</script>

<style scoped lang="scss">
.problem-show {
  width: 100%;
  height: 100vh;
  position: relative;
  .header {
    width: 100%;
    height: 50px;
    line-height: 50px;
    text-align: center;
    background-color: rgba(0, 25, 35, 0.9);
    position: relative;
  }
  .content {
    height: calc(100% - 50px);
    width: 100%;
    position: relative;
    display: flex;
    /* background-color: rgba(12, 128, 241, 0.2); */
    box-shadow: -1px 9px 10px 3px rgba(0, 0, 0, 0.11);
    .left {
      height: 100%;
      width: calc(50% - 10px);
      background-color: rgba(12, 128, 241, 0.2);
      box-shadow: -1px 4px 5px 3px rgba(0, 0, 0, 0.11);
      overflow: auto;
    }
    .right {
      height: 100%;
      width: 50%;
      /* background-color: rgba(12, 128, 24, 0.2); */
      box-shadow: -1px 4px 5px 3px rgba(0, 0, 0, 0.11);
      display: inline;
      .code {
        width: 100%;
        height: calc(100% - 200px);
        background-color: rgba(25, 12, 41, 0.2);
        position: relative;
        .code-header {
          width: 100%;
          height: 45px;
          line-height: 45px;
          text-align: center;
          background-color: rgba(1, 18, 25, 0.8);
          color: aliceblue;
          position: relative;
        }
        .code-content {
          width: 100%;
          height: calc(100% - 45px);
        }
        .info-style-button {
          width: 30px;
          height: 30px;
          text-align: center;
          position: absolute;
          background: #d6d6d6;
          border: none;
          border-radius: 50%;
          bottom: 0px;
          left: 50%;
          transform: translate(-15px, 15px);
          display: inline;
          z-index: 10;
        }
      }
      .info {
        width: 100%;
        height: 200px;
        background-color: unset;
        overflow: hidden;
        position: relative;
        .info-header {
          width: 100%;
          height: 45px;
          line-height: 45px;
          text-align: center;
          background-color: rgba(28, 24, 41, 0.9);
          color: aliceblue;
        }
        .info-content {
          width: 100%;
          height: calc(100% - 45px);
        }
      }
    }
    .left-right {
      height: 50px;
      line-height: 50px;
      width: 10px;
      background-color: #d6d6d6;
      background-size: cover;
      background-position: center;
      border-radius: 5px;
      font-size: 32px;
      color: white;
      position: relative;
      top: 45%;
      cursor: col-resize;
      .left-button,
      .right-button {
        width: 30px;
        height: 30px;
        text-align: center;
        position: absolute;
        background: rgba(160, 150, 255, 0.6);
        border: none;
        top: 50%;
        left: -10px;
        z-index: 100;
      }
      .left-button {
        transform: translate(-20px, -15px);
        border-radius: 50% 0 0 50%;
        display: none;
      }
      .right-button {
        transform: translate(20px, -15px);
        border-radius: 0 50% 50% 0;
        display: none;
      }
    }
    .left-right:hover {
      color: #444444;
    }
  }
}
</style>
