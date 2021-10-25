<template>
  <div class="course-card">
    <div class="card-header">
      <img
        ref="bannerHeight"
        src="//edu-image.nosdn.127.net/F05ADA2CD454710CFF6D216D35512FBF.JPG?imageView&amp;quality=100&amp;thumbnail=230y130&amp;type=webp"
        alt="课程封面"
      />
    </div>
    <div class="card-content">
      <h3 class="title">课程标题</h3>
      <p class="school">金华职业技术学院</p>
      <p class="teacher">梅旭时</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {},
  mounted() {},
  methods: {},
};
</script>

<style scoped>
.course-card {
  width: 226px;
  height: 200px;
  padding: 0;
  border-radius: 8px;
}
.course-card .card-header {
  width: 100%;
  height: 65%;
  border-radius: 8px 8px 0 0;
}
.course-card .card-header img {
  width: 100%;
  height: 100%;
  border-radius: 8px 8px 0 0;
}
.course-card .card-content {
  height: 35%;
  width: 100%;
  border-radius: 0 0 8px 8px;
  /* border-bottom: 1px solid black; */
  background-color: #f1f1ef;
}
.course .title {
  font-size: 14px;
  font-weight: bold;
}
.course .school {
  height: 12px;
  line-height: 12px;
  font-size: 12px;
  margin-top: 6px;
  color: #666;
  overflow: hidden;
}
.course .teacher {
  line-height: 17px;
  margin: 8px 0 0 0;
  font-size: 12px;
  color: #999;
  overflow: hidden;
}
</style>
