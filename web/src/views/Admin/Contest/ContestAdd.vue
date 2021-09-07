<template>
  <div class="news-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="news_form">
        <el-form-item label="新闻标题">
          <el-input v-model="news_form.news_title"></el-input>
        </el-form-item>
        <el-form-item label="新闻类型">
          <el-select v-model="news_form.news_type" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.title"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">新闻内容</span>
          <el-button class="button" type="text" @click="changeNews=!changeNews">修改内容</el-button>
        </div>
      </template>
      <NewsChild mode="preview" :content="news_form.news_content" :key="new Date().getTime()" />
    </el-card>
    <el-dialog
    title="内容编辑"
    v-model="changeNews"
    width="90%"
    top="60px"
    center>
        <NewsChild height="800px" :content="news_form.news_content" @getContent="getContent"/>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import NewsChild from "@/components/Editor/MarkdownEditor.vue";
import NewsModel from '@/assets/markdown/新闻模板.md';

export default {
  components: {
    NewsChild
  },
  setup() {},
  data() {
    return {
        changeNews: false,
      options: [
          {value: 0, title: '普通'},
          {value: 1, title: '竞赛新闻'},
          {value: 2, title: '课程新闻'},
      ],
      news_form: {
        news_title: "",
        news_content: NewsModel,
        news_type: null,
      },
    };
  },
  methods: {
      getContent(text){
        this.news_form.news_content = text;
      }
  }
};
</script>

<style>
.news-add {
  width: 90%;
  margin: 40px auto;
}
.news-add .el-input {
  max-width: 500px;
}
.news-add .el-card {
  margin: 20px 0;
}
.news-span {
  font-size: 18px;
  font-weight: 800;
  margin-left: 20px;
}
.news-add .el-card__header {
  height: 60px;
  padding: 0 40px;
}
.news-add .card-header {
  justify-content: space-between;
  align-items: center;
}
.news-add .title {
  float: left;
  /* background-color: rgba(15, 105, 214, 0.2); */
  width: 100px;
  height: 60px;
  line-height: 60px;
  font-size: 20px;
  font-weight: 800;
  font-family: "宋体";
}
.news-add .button {
  float: right;
  width: 60px;
  height: 60px;
}
</style>
