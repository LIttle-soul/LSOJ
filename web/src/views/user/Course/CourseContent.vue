<template>
  <div class="course-main">
    <div class="course-content">
      <div class="content-header">
        <div class="header-font">嵌入式开发</div>
      </div>
      <div class="video">
        <CourseVideo />
      </div>
    </div>
    <div class="course-catalogue">
      <div class="components">
        <CourseCatalogue :data="chapterData" @node-click="handleNodeClick" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getCourseChapter } from "@/api/course";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";

let route = useRoute();
let router = useRouter();

let courseTitle = ref({});

let chapterData = ref([
  {
    id: 1,
    label: "Level one 1",
    children: [
      {
        id: 4,
        label: "Level two 1-1",
      },
    ],
  },
]);
// 格式化章节列表
let formatData = (val: any) => {
  return val.map((item: any) => ({
    id: item.chapter_id,
    label: item.chapter_title,
    children:
      item.section_list?.map((res: any) => ({
        id: res.chapter_id,
        label: res.chapter_title,
      })) || [],
  }));
};
//获取章节列表
let getChapterData = async () => {
  // let loading = ElLoading.service({
  //   lock: true,
  //   text: "加载中....",
  //   background: "rgba(0,0,0,7)",
  // });
  let back_data = await getCourseChapter({
    course_id: Number(route.query.id),
  });
  console.log(back_data);
  if (back_data.status) {
    chapterData.value = formatData(back_data.message);
    // loading.close();
  } else {
    // loading.close();
  }
};

//挂载
onMounted(() => {
  // getChapterData();
});

let handleNodeClick = (data: any, node: any) => {
  if (node.isLeaf) {
    router.push({
      path: "/courseshow",
      query: {
        id: route.query.id,
      },
    });
  }
};
</script>

<style scoped lang="scss">
.course-main {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  height: auto;
}
.course-content {
  width: 75%;
  max-width: 1200px;
  margin: 10px auto;
  border: 1px solid #d6d6d6;
  box-shadow: 0px 0px 20px #d6d6d6;
  border-radius: 10px;
  float: left;
}
.video {
  width: 85%;
  margin: 15px auto;
}
.content-header {
  height: 50px;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid #d6d6d6;
  text-align: center;
}
.header-font {
  margin-left: 30px;
  height: 50px;
  line-height: 50px;
}
.course-catalogue {
  width: 20%;
  max-width: 300px;
  margin: 10px auto;
  height: auto;
  border: 1px solid #d6d6d6;
  box-shadow: 0px 0px 20px #d6d6d6;
  border-radius: 10px;
  float: right;
}
.components {
  margin: 5px 5px;
}
</style>
