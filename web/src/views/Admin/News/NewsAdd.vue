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
          <el-input-number v-model="news_form.news_importance"></el-input-number>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="float: right; margin-bottom: 15px" @click="submit"
        >提交</el-button
      >
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">新闻内容</span>
          <el-button class="button" type="text" @click="changeNews = !changeNews"
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
    <el-dialog title="内容编辑" v-model="changeNews" width="90%" top="60px" center>
      <NewsChild
        height="800px"
        :content="news_form.news_content"
        @getContent="getContent"
      />
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import NewsChild from "@/components/Editor/MarkdownEditor.vue";
import { submitNewsData, changeNewsData, getNewsList } from "@/api/news";
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { ElMessage } from "element-plus";
import news_mode from "@/assets/markdown/新闻模板.md?raw";

let route = useRoute();
let router = useRouter();

let changeNews = ref(false);
let options = [
  { value: 0, title: "普通" },
  { value: 1, title: "竞赛新闻" },
  { value: 2, title: "课程新闻" },
];
let news_form = ref({
  news_id: 0,
  news_title: "",
  news_content: news_mode,
  news_type: 0,
  news_importance: 0,
});
let getContent = (text: string) => {
  news_form.value.news_content = text;
};
let submit = async () => {
  let back_data =
    route.params.news_id == ""
      ? await submitNewsData({
          news_title: news_form.value.news_title,
          news_introduce: news_form.value.news_content,
          news_type: news_form.value.news_type,
          news_importance: news_form.value.news_importance,
        })
      : await changeNewsData({
          news_id: news_form.value.news_id,
          news_title: news_form.value.news_title,
          news_introduce: news_form.value.news_content,
          news_type: news_form.value.news_type,
          news_importance: news_form.value.news_importance,
        });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    setTimeout(() => {
      router.push("/admin/newslist");
    }, 2000);
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let formatData = (val: any) => {
  return {
    news_id: val.news_id,
    news_title: val.news_title,
    news_content: val.news_introduce == null ? "" : val.news_introduce,
    news_type: val.news_type,
    news_importance: val.news_importance,
  };
};
let getNewsData = async (val: any) => {
  let back_data = await getNewsList({
    page: 1,
    total: 1,
    text: "",
    news_id: val,
  });
  // console.log(back_data);
  if (back_data.status) {
    news_form.value = formatData(back_data.message);
  }
};
onMounted(() => {
  if (route.params.news_id) {
    getNewsData(route.params.news_id[0]);
  }
});
</script>

<style lang="scss" scoped>
.news-add {
  width: 95%;
  margin: 40px auto;
  .card {
    margin: 30px 0;
    border-radius: 20px;
    .el-input {
      max-width: 400px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      .title {
        width: 100px;
        height: 20px;
        line-height: 20px;
        font-size: 20px;
        font-weight: 800;
        font-family: "宋体";
      }
      .button {
        width: 60px;
        height: 20px;
      }
    }
  }
}
</style>
