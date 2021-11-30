<template>
  <div class="news-show">
    <div class="header">
      <h1>{{ news_info.news_title }}</h1>
      <p>作者：{{ news_info.news_creator }}</p>
      <p>创建时间：{{ news_info.news_create_time }}</p>
    </div>
    <div class="content">
      <NewsChild mode="preview" :content="news_info.news_context" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { mapGetters } from "vuex";
import { useRoute } from "vue-router";
import dayJS from "dayjs";
import { ElLoading, ElMessage } from "element-plus";
import { getNewsList } from "@/api/news";
import NewsChild from "@/components/Editor/MarkdownEditor.vue";
import temp_news from "@/assets/markdown/NewsTemplet.md?raw";

let route = useRoute();

let news_info = ref({
  news_title: "平台开发新闻模板",
  news_creator: "LiSoul",
  news_create_time: "2020年01月01日 12时25分36秒",
  news_context: temp_news,
});
let setData = (val: any) => {
  news_info.value = {
    news_title: val.news_title,
    news_creator: val.news_creator,
    news_create_time: dayJS(val.create_time).format("YYYY年MM月DD日 HH时mm分ss秒"),
    news_context: val.news_introduce == null ? "# 无" : val.news_introduce,
  };
};
let getData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中...",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getNewsList({
    page: 1,
    total: 50,
    news_id: route.params.news_id,
    text: "",
  });
  // console.log(back_data);
  if (back_data.status) {
    setData(back_data.message);
    loading.close();
  } else {
    loading.close();
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
onMounted(() => {
  getData();
});
</script>

<style scoped lang="scss">
.news-show {
  width: 80%;
  max-width: 1600px;
  margin: 80px auto;
  .header {
    width: 100%;
    text-align: center;
    h1 {
      font-size: 24px;
      font-weight: bolder;
      line-height: 50px;
    }
    p {
      font-size: 16px;
      line-height: 30px;
      font-family: "宋体";
    }
  }
  .content {
    width: 100%;
  }
}
</style>
