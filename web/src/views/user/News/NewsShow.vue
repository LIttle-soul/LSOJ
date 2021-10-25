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

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { mapGetters } from "vuex";

export default {
  components: {
    NewsChild: defineAsyncComponent(() =>
      import("@/components/Editor/MarkdownEditor.vue")
    ),
  },
  created() {
    this.setData(this.$route.params.news_id);
  },
  computed: {
    ...mapGetters("news", {
      getNewsData: "getNewsData",
    }),
  },
  data() {
    return {
      news_info: {
        news_title: "平台开发新闻模板",
        news_creator: "LiSoul",
        news_create_time: "2020年01月01日 12时25分36秒",
        news_context: require("@/assets/markdown/新闻模板.md"),
      },
    };
  },
  methods: {
    setData(data) {
      let val = this.getNewsData(data);
      this.news_info = {
        news_title: val.news_title,
        news_creator: val.news_creator,
        news_create_time: this.$dayJS(val.create_time).format(
          "YYYY年MM月DD日 HH时mm分ss秒"
        ),
        news_context: val.news_introduce == null ? "# 无" : val.news_introduce,
      };
    },
  },
};
</script>

<style scoped>
.news-show {
  width: 80%;
  max-width: 1600px;
  margin: 80px auto;
}
.header {
  width: 100%;
  text-align: center;
}
.header h1 {
  font-size: 24px;
  font-weight: bolder;
  line-height: 50px;
}
.header p {
  font-size: 16px;
  line-height: 30px;
  font-family: "宋体";
}
.content {
  width: 100%;
}
</style>
