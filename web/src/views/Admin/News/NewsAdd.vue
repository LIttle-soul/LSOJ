<template>
  <div class="news-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="news_form">
        <el-form-item label="新闻编号">
          <el-input-number
            v-model="news_form.news_id"
            disabled
            controls-position="right"
          ></el-input-number>
        </el-form-item>
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
        <el-form-item label="优先级">
          <el-input-number
            v-model="news_form.news_importance"
          ></el-input-number>
        </el-form-item>
      </el-form>
      <el-button
        type="primary"
        style="float: right; margin-bottom: 15px;"
        @click="submit"
        >提交</el-button
      >
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">新闻内容</span>
          <el-button
            class="button"
            type="text"
            @click="changeNews = !changeNews"
            >修改内容</el-button
          >
        </div>
      </template>
      <NewsChild
        mode="preview"
        :content="news_form.news_content"
        :key="new Date().getTime()"
      />
    </el-card>
    <el-dialog
      title="内容编辑"
      v-model="changeNews"
      width="90%"
      top="60px"
      center
    >
      <NewsChild
        height="800px"
        :content="news_form.news_content"
        @getContent="getContent"
      />
    </el-dialog>
  </div>
</template>

<script lang="js">
import NewsChild from "@/components/Editor/MarkdownEditor.vue";
import { submitNewsData, changeNewsData } from "@/api/news";
import { mapGetters } from "vuex";

export default {
  components: {
    NewsChild,
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
      changeNews: false,
      options: [
        { value: 0, title: "普通" },
        { value: 1, title: "竞赛新闻" },
        { value: 2, title: "课程新闻" },
      ],
      news_form: {
        news_id: 0,
        news_title: "",
        news_content: require("@/assets/markdown/新闻模板.md"),
        news_type: 0,
        news_importance: 0,
      },
    };
  },
  methods: {
    getContent(text) {
      this.news_form.news_content = text;
    },
    async submit() {
      let back_data =
        this.$route.params.news_id == ""
          ? await submitNewsData(this.news_form)
          : await changeNewsData(this.news_form);
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("news/getNewsList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    setData(data) {
      if (data != "") {
        let val = this.getNewsData(data);
        this.news_form = {
          news_id: val.news_id,
          news_title: val.news_title,
          news_content: val.news_introduce == null ? "" : val.news_introduce,
          news_type: val.news_type,
          news_importance: val.news_importance,
        };
      }
    },
  },
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
.news-add .el-card .el-form-item:nth-child(2) .el-input-number__decrease,
.news-add .el-card .el-form-item:nth-child(2) .el-input-number__increase {
  transform: translateY(1px);
}
.news-add .el-card .el-form-item:nth-child(3) .el-input-number__decrease,
.news-add .el-card .el-form-item:nth-child(3) .el-input-number__increase {
  transform: translateY(1px);
}
</style>
