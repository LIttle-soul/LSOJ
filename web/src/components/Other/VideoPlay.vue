<template>
  <div class="page">
    <VideoPlay v-bind="options" :poster="props.image" />
  </div>
</template>

<script lang="ts" setup>
import VideoPlay from "vue3-video-play";
import "vue3-video-play/dist/style.css";

import { ref } from "vue";

let props = defineProps({
  title: {
    type: String,
    default: "我的视屏",
  },
  image: {
    type: String,
    default: "https://cdn.jsdelivr.net/gh/xdlumia/files/video-play/ironMan.jpg",
  },
  src: {
    type: String,
    default: "",
  },
});
const options = ref({
  width: "100%", //播放器高度
  height: "100%", //播放器高度
  color: "#409eff", //主题色
  title: props.title || "", //视频名称
  src:
    props.src ||
    "http://10.46.2.3/videos//%E7%AE%97%E6%B3%95%E8%BF%9B%E9%98%B6/1-2%20sat.mp4", //视频源
  muted: false, //静音
  webFullScreen: false,
  speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
  autoPlay: false, //自动播放
  loop: false, //循环播放
  mirror: false, //镜像画面
  ligthOff: false, //关灯模式
  volume: 0.3, //默认音量大小
  control: true, //是否显示控制
  controlBtns: [
    "audioTrack",
    "quality",
    "speedRate",
    "volume",
    "setting",
    "pip",
    "pageFullScreen",
    "fullScreen",
  ], //显示所有按钮,
});
</script>

<style scoped lang="scss">
.page {
  width: 100%;
  height: 100%;
}
</style>
