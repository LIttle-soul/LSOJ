<template>
  <div class="course-card" @click="show_course(Data)">
    <div class="card-header">
      <!-- <img
        ref="bannerHeight"
        src="//edu-image.nosdn.127.net/F05ADA2CD454710CFF6D216D35512FBF.JPG?imageView&amp;quality=100&amp;thumbnail=230y130&amp;type=webp"
        alt="课程封面"
      /> -->
      <el-image :src="'data:image/png;base64'+Data.course_cover" class="images"></el-image>
    </div>
    <div class="card-content">
      <p class="title">{{Data.course_name}}</p>
      <p class="school">金华职业技术学院</p>
      <p class="teacher">{{Data.course_creator}}</p>
    </div>
  
  </div>
</template>

<script>
export default {
  props: {
    Data: {
      type: undefined,
      default: [],
    },
  },
  mounted() {
  },
  methods: {
    show_course(row) {
      console.log(row);
      if (!this.admin) {
       this.$router.push({
          path: "/showcourse",
          query: {
            course_title: escape(row.course_name),
          },
        }); 
      } 
    }
  },
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
  /* border-bottom: 1px solid black;  */
  background-color: #f1f1ef;
}
.images{
  height: 100%;
  width: 100%;
}
.course .title {
  font-size: 18px;
  margin-top: 1%;
  font-weight: bold;
}
.course .school {
  height: 12px;
  line-height: 12px;
  font-size: 13px;
  margin-top: 6px; 
  margin-top: 3.5%;
  color: #666;
  overflow: hidden;
}
.course .teacher {
  line-height: 17px;
  margin: 8px 0 0 0;
  font-size: 13px;
  color: #999;
  overflow: hidden;
}
</style>
