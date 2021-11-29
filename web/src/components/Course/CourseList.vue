<template>
  <div class="course">
    <h2>课程推荐</h2>
    <div class="header">
      <!-- 
        datas: 无缝滚动列表数据，组件内部使用列表长度。
        v-model: 通过v-model控制动画滚动与停止，默认开始滚动
        direction: 控制滚动方向，可选值up，down，left，right
        isWatch: 开启数据更新监听
        hover: 是否开启鼠标悬停
        limitScrollNum: 开启滚动的数据量，只有列表长度大于等于该值才会滚动
        step: 步进速度
       -->
      <js-seamless-scroll
        :datas="datas"
        :v-model="true"
        direction="right"
        :isWatch="true"
        :hover="true"
        :limitScrollNum="4"
        :step="scroll_step"
        class="scroll"
      >
        <div style="display: flex;">
          <div v-for="item in 12" :key="item" class="scroll-item">
            <course-card></course-card>
          </div>
        </div>
      </js-seamless-scroll>
      <el-button
        class="left"
        type="text"
        @click="scroll_step = scroll_step - 0.5"
        @dblclick="scroll_step = -Math.abs(scroll_step)"
      >
        <el-icon :size="33">
          <d-arrow-left />
        </el-icon>
      </el-button>
      <el-button
        class="right"
        type="text"
        @click="scroll_step = scroll_step + 0.5"
        @dblclick="scroll_step = Math.abs(scroll_step)"
      >
        <el-icon :size="33">
          <d-arrow-right />
        </el-icon>
      </el-button>
    </div>
    <h2>课程列表</h2>
    <ul class="content">
      <li v-for="item in 12" :key="item" class="content-item">
        <course-card></course-card>
      </li>
    </ul>
  </div>
</template>
<script>
import CourseCard from "./CourseCard.vue";
import { DArrowLeft, DArrowRight } from "@element-plus/icons";
export default {
  components: {
    "course-card": CourseCard,
    DArrowLeft,
    DArrowRight,
  },
  data() {
    return {
      scroll_step: 0.6,
      datas: [
        {
          title: "Vue3.0 无缝滚动组件展示数据第1条",
          date: Date.now(),
        },
        {
          title: "Vue3.0 无缝滚动组件展示数据第2条",
          date: Date.now(),
        },
        {
          title: "Vue3.0 无缝滚动组件展示数据第3条",
          date: Date.now(),
        },
        {
          title: "Vue3.0 无缝滚动组件展示数据第4条",
          date: Date.now(),
        },
        {
          title: "Vue3.0 无缝滚动组件展示数据第5条",
          date: Date.now(),
        },
      ],
    };
  },
};
</script>

<style scoped>
.course {
  width: 80%;
  min-width: 800px;
  margin: 0 auto;
}
.course h2 {
  font-size: 1.8em;
  font-weight: bolder;
  font-family: "楷体";
  margin: 40px 60px;
}
.course .header {
  width: 100%;
  height: 210px;
  overflow: hidden;
  border-radius: 20px;
  box-shadow: 3px 3px 0.4em rgb(155, 163, 38), -3px 0 0.4em olive;
  padding: 50px 0;
  position: relative;
}
.left {
  width: 40px;
  height: 40px;
  /* background-color: black; */
  color: rgb(63, 15, 151);
  position: absolute;
  bottom: 10px;
  left: 30%;
}
.right {
  width: 40px;
  height: 40px;
  /* background-color: black; */
  color: rgb(63, 15, 151);
  position: absolute;
  bottom: 10px;
  right: 30%;
}
.course .header .scroll {
  height: 100%;
  width: 10000px;
}
.course .header .scroll .scroll-item {
  margin: 0 20px;
}
.course .content {
  width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  /* overflow: auto; */
  justify-content: center;
}
.course .content-item {
  margin: 20px 20px;
}
</style>