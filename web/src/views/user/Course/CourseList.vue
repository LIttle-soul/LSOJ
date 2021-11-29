<template>
  <div class="course">
      <h2>课程推荐</h2>
       <el-input
        placeholder="请输入内容"
        size="mini"
        v-model="search_data"
        class="input-with-select"
      >
        <template #append>
          <el-button
            icon="el-icon-search"
            @click="search_all_data(search_data)"
          ></el-button>
        </template>
      </el-input>
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
        :datas="Data"
        :v-model="true"
        direction="right"
        :isWatch="true"
        :hover="true"
        :limitScrollNum="4"
        :step="scroll_step"
        class="scroll"
      >
        <div style="display: flex;">
          <div v-for="item in Data" :key="item" class="scroll-item">
            <CourseCard :Data="item"></CourseCard>
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
      <li v-for="item in Data" :key="item" class="content-item">
        <CourseCard :Data="item"></CourseCard>
      </li>
    </ul>
  </div>
</template> 
<script>
import CourseCard from "@/components/Course/CourseCard.vue";
import { DArrowLeft, DArrowRight } from "@element-plus/icons";
import { mapGetters, mapState } from "vuex";
export default {
  components: {
    CourseCard: CourseCard,
    DArrowLeft,
    DArrowRight,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("course", {
      temp_data: (state) => state.course_list,
    }),
    ...mapGetters("course", {
      filterCourseList: "filterCourseList",
    })
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data(this.search_data);
    },
    temp_data() {
      this.Data = this.formatData(this.temp_data);
    },
  },

  created() {
    this.$store.dispatch('course/getCourseList');
    this.Data = this.formatData(this.temp_data);
  },
  data() {
    return {
      search_data: "",
      scroll_step: 0.6,
      Data: [
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
        {
          title: "Vue3.0 无缝滚动组件展示数据第5条",
          date: Date.now(),
        },
        {
          title: "Vue3.0 无缝滚动组件展示数据第5条",
          date: Date.now(),
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      this.Data = this.formatData(this.filterCourseList(this.temp_data, val));
    },
    formatData(val) {
      return val.map((item) => ({
        course_id: item.course_id,
        course_name: item.course_name,
        course_creator: item.course_creator,
        course_cover: item.course_cover,
      }));
    },
  }
};
</script>
<style  lang="css">
.input-with-select {
  width: 230px;
  float: right;
  margin-top: -5%;
  transform: translateY(-1px);
}
</style>

<style scoped>

/* .course-list {
  width: 85%;
  max-width: 1400px;
  margin: 70px auto;
  position: relative;
  float: right;
} */

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
