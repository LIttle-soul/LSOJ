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
    <div class="content" ref="Content">
      <div class="left" ref="Left">
        <ProblemChild
          mode="preview"
          height="100%"
          :content="problem_data.problem_description"
        />
      </div>
      <div
        class="left-right"
        ref="LeftRight"
        @mouseenter="hadelLeftRightEnter"
        @mouseleave="hadelLeftRightLevel"
        @mousedown="hadelLeftRightDown"
      >
        <button
          class="left-button"
          @click="hadelLeftButtonClick"
          ref="LeftRightLeftButton"
        >
          <i class="el-icon-caret-left"></i>
        </button>
        <button
          class="right-button"
          @click="hadelRightButtonClick"
          ref="LeftRightRightButton"
        >
          <i class="el-icon-caret-right"></i>
        </button>
        ⋮
      </div>
      <div class="right" ref="Right">
        <div class="code" ref="Code">
          <div class="code-header">
            <CodeHeader @changeLanguage="hadelChangeLanguage" />
          </div>
          <div class="code-content">
            <CodeEditor
              :language="submit_data.solution_language.code"
              ref="codeEditor"
            />
          </div>
          <button
            class="info-style-button"
            @mousedown="hadelInfoButtonDown"
            ref="InfoStyleButton"
          >
            <i class="el-icon-d-caret"></i>
          </button>
        </div>
        <div class="info" ref="Info">
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

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { mapGetters } from "vuex";
import { submitCode, getSolutionData } from "@/api/solution";

export default {
  components: {
    ProblemHeader: defineAsyncComponent(() =>
      import("@/components/Problem/ProblemHeader.vue")
    ),
    ProblemChild: defineAsyncComponent(() =>
      import("@/components/Editor/MarkdownEditor.vue")
    ),
    CodeEditor: defineAsyncComponent(() =>
      import("@/components/Editor/CodeEditor.vue")
    ),
    CodeHeader: defineAsyncComponent(() =>
      import("@/components/Editor/CodeHeader.vue")
    ),
    SolutionHeader: defineAsyncComponent(() =>
      import("@/components/Solution/SolutionHeader.vue")
    ),
    SolutionContent: defineAsyncComponent(() =>
      import("@/components/Solution/SolutionContent.vue")
    ),
  },
  created() {
    this.setData(this.$route.query);
  },
  computed: {
    ...mapGetters("problem", {
      getProblemData: "getProblemData",
    }),
    ...mapGetters("solution", {
      getSolutionData: "getSolutionData",
    }),
  },
  data() {
    return {
      left_right_open: true,
      solution_result: {
        run_result: 0,
        run_error: null,
        run_pass_rate: 0,
        run_all_rate: 0,
      },
      problem_data: {
        problem_title: "Hello, World",
        problem_description: require("@/assets/markdown/问题模板.md"),
        time_limit: 1000,
        memory_limit: 128,
      },
      submit_data: {
        problem_id: "",
        solution_language: { value: 0, text: "C", code: "c" },
        solution_code: "",
        level_id: undefined,
        contest_id: undefined,
      },
    };
  },
  methods: {
    hadelChangeLanguage(val) {
      this.submit_data.solution_language = val;
    },
    async submitData() {
      this.submit_data.solution_code = this.$refs.codeEditor.getVal();
      let back_data = await submitCode({
        problem_id: this.submit_data.problem_id,
        solution_language: this.submit_data.solution_language.value,
        solution_code: this.submit_data.solution_code,
        level_id: null,
        contest_id: this.submit_data.contest_id,
      });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        let inter = setInterval(async () => {
          let val = await getSolutionData({
            solution_id: back_data.solution_id,
          });
          // console.log(val);
          if (val.status) {
            this.solution_result = val.message;
            if (val.message.run_result > 3) {
              clearInterval(inter);
              this.$store.dispatch("solution/getSolutionDataList");
              this.$store.dispatch("problem/getProblemDataList");
            }
          }
        }, 2000);
      } else {
        this.$message({
          type: "wrong",
          message: back_data.message,
        });
      }
    },

    setData(val) {
      // console.log(val);
      this.problem_data = {
        problem_title: unescape(val.problem_title),
        problem_description: unescape(val.problem_description),
        time_limit: +val.time_limit,
        memory_limit: +val.memory_limit,
      };
      this.submit_data.problem_id = +val.problem_id;
      this.submit_data.contest_id = +val.contest_id || null;
    },
    // 样式相关操作函数
    hadelLeftRightEnter() {
      this.left_right_open
        ? (this.$refs.LeftRightRightButton.style.display = "inline")
        : (this.$refs.LeftRightLeftButton.style.display = "inline");
    },
    hadelLeftRightLevel() {
      this.$refs.LeftRightRightButton.style.display = "none";
      this.$refs.LeftRightLeftButton.style.display = "none";
    },
    hadelLeftRightDown(e) {
      this.$refs.LeftRight.style.background = "#818181";
      let startX = e.clientX;
      let left_width = this.$refs.LeftRight.offsetLeft;
      document.onmousemove = (e) => {
        let endX = e.clientX;
        let moveLen = left_width + (endX - startX);
        let maxT =
          this.$refs.Content.clientWidth - this.$refs.LeftRight.offsetWidth;
        if (moveLen < 50) {
          this.$refs.Left.style.display = "none";
          moveLen = 0;
        } else if (moveLen > maxT - 100) {
          this.$refs.Right.style.display = "none";
          this.left_right_open = false;
          moveLen = maxT;
        } else {
          this.left_right_open = true;
          this.$refs.Right.style.display = "inline";
          this.$refs.Left.style.display = "inline";
        }
        let temp = (moveLen * 100) / this.$refs.Content.clientWidth;
        this.$refs.Left.style.width = temp + "%";
        this.$refs.Right.style.width = 100 - temp + "%";
      };
      document.onmouseup = () => {
        this.$refs.LeftRight.style.background = "#d6d6d6";
        document.onmousemove = null;
        document.onmouseup = null;
        this.$refs.LeftRight.releaseCapture &&
          this.$refs.LeftRight.releaseCapture();
      };
      this.$refs.LeftRight.setCapture && this.$refs.LeftRight.setCapture();
      return false;
    },
    hadelLeftButtonClick() {
      this.left_right_open = true;
      this.$refs.Left.style.width = "50%";
      this.$refs.Right.style.width = "50%";
      this.$refs.Right.style.display = "inline";
    },
    hadelRightButtonClick() {
      this.left_right_open = false;
      this.$refs.Left.style.width = "100%";
      this.$refs.Right.style.width = "50%";
      this.$refs.Right.style.display = "none";
    },
    hadelInfoButtonDown(e) {
      this.$refs.InfoStyleButton.style.background = "#818181";
      let startY = e.clientY;
      let top_height = this.$refs.Code.clientHeight;
      document.onmousemove = (e) => {
        let endY = e.clientY;
        let moveLen = top_height + (endY - startY);
        let maxT = this.$refs.Right.clientHeight;
        if (moveLen < 90) {
          moveLen = 90;
        } else if (moveLen > maxT - 45) {
          moveLen = maxT - 45;
        }
        let temp = (moveLen * 100) / this.$refs.Right.clientHeight;
        this.$refs.Code.style.height = temp + "%";
        this.$refs.Info.style.height = 100 - temp + "%";
      };
      document.onmouseup = () => {
        this.$refs.InfoStyleButton.style.background = "#dddddd";
        document.onmousemove = null;
        document.onmouseup = null;
        this.$refs.InfoStyleButton.releaseCapture &&
          this.$refs.InfoStyleButton.releaseCapture();
      };
      this.$refs.InfoStyleButton.setCapture &&
        this.$refs.InfoStyleButton.setCapture();
      return false;
    },
  },
};
</script>

<style scoped>
.problem-show {
  width: 100%;
  height: 100vh;
  position: relative;
}
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
}
.content .left {
  height: 100%;
  width: calc(50% - 10px);
  background-color: rgba(12, 128, 241, 0.2);
  box-shadow: -1px 4px 5px 3px rgba(0, 0, 0, 0.11);
  overflow: auto;
}
.content .right {
  height: 100%;
  width: 50%;
  /* background-color: rgba(12, 128, 24, 0.2); */
  box-shadow: -1px 4px 5px 3px rgba(0, 0, 0, 0.11);
  display: inline;
}
.content .left-right {
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
}
.content .left-right:hover {
  color: #444444;
}
.content .left-right .left-button,
.content .left-right .right-button {
  width: 30px;
  height: 30px;
  text-align: center;
  position: absolute;
  background: rgba(25, 12, 41, 0.2);
  border: none;
  top: 50%;
  left: -10px;
  z-index: 100;
}
.content .left-right .left-button {
  transform: translate(-20px, -15px);
  border-radius: 50% 0 0 50%;
  display: none;
}
.content .left-right .right-button {
  transform: translate(20px, -15px);
  border-radius: 0 50% 50% 0;
  display: none;
}

.content .right .code {
  width: 100%;
  height: calc(100% - 45px);
  background-color: rgba(25, 12, 41, 0.2);
  position: relative;
}
.content .right .code .code-header {
  width: 100%;
  height: 45px;
  line-height: 45px;
  text-align: center;
  background-color: rgba(1, 18, 25, 0.8);
  color: aliceblue;
  position: relative;
}
.content .right .code .code-content {
  width: 100%;
  height: calc(100% - 45px);
}
.content .right .info {
  width: 100%;
  height: 45px;
  background-color: unset;
  overflow: hidden;
  position: relative;
}
.content .right .info-style-button {
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
.content .right .info .info-header {
  width: 100%;
  height: 45px;
  line-height: 45px;
  text-align: center;
  background-color: rgba(28, 24, 41, 0.9);
  color: aliceblue;
}
.content .right .info .info-content {
  width: 100%;
  height: calc(100% - 45px);
}
</style>
