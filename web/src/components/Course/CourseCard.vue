<template>
  <div class="course-child">
    <div class="course-card" v-for="(item, index) in Data" :key="index">
      <div class="course-item" @click="linkTo(item.course_id)">
        <div class="glass"></div>
        <div class="card-header">
          <el-image class="card-image" :src="item.src" fit="fill"></el-image>
        </div>
        <div class="card-content">
          <h4 class="title">{{ item.title }}</h4>
          <p class="auther">{{ item.auther }}</p>
        </div>
        <div class="card-footer">
          <div class="status">
            {{ item.status }}
          </div>
          <div class="join">{{ item.join }}人参加</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

let router = useRouter();

let props = defineProps({
  Data: {
    type: undefined,
    default: [
      {
        course_id: 1,
        src: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        title: "法语入门",
        auther: "LiSoul",
        join: 100,
        status: "已结束",
      },
    ],
  },
});

let linkTo = (val: number) => {
  router.push({
    path: "/courseshow",
    query: {
      id: val,
    },
  });
};
</script>

<style lang="scss" scoped>
.course-child {
  width: 100%;
  margin: 20px 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  grid-gap: 20px;
  .course-card {
    .course-item {
      width: 180px;
      height: 200px;
      margin: 0 auto;
      overflow: hidden;
      box-shadow: 0 0 0 1px hsla(0, 0%, 100%, 0.3) inset, 0 0.5em 1em rgba(0, 0, 0, 0.6);
      text-shadow: 0 1px 1px hsla(0, 0%, 100%, 0.3);
      border-radius: 15px;
      overflow: hidden;
      background-color: rgba(210, 210, 210, 0.4);
      position: relative;
      .glass {
        position: absolute;
        background: #e9ebfe;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: -1;
        -webkit-filter: blur(10px);
        filter: blur(10px);
      }
      .card-header {
        width: 100%;
        height: 60%;
        .card-image {
          width: 100%;
          height: 100%;
        }
      }
      .card-content {
        width: 100%;
        height: calc(40% - 40px);
        padding: 10px;
        .title {
          font-family: "STKaiti";
          font-weight: bold;
          font-size: 20px;
        }
        .auther {
          font-size: 14px;
        }
      }
      .card-footer {
        width: 100%;
        height: 20px;
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        line-height: 20px;
        .status {
          margin: 0 10px;
        }
        .join {
          margin: 0 10px;
        }
      }
    }
  }
}
</style>
