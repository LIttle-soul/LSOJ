<template>
  <v-md-editor 
  v-model="text" 
  :mode="mode"
  :toc-nav-position-right="true"
  :autofocus="true"
  left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code | save"
  right-toolbar="preview fullscreen toc sync-scroll"
  :height="height"
  :disabled-menus="[]"
  @save="save(text)"
  @upload-image="handleUploadImage"
  @copy-code-success="handleCopyCodeSuccess"></v-md-editor>
</template>

<script>
import NewsModel from '@/assets/temp/新闻模板.md';

  export default {
    props: {
      mode: {
        type: String,
        default: 'editable'
      },
      height: {
        type: String,
        default: 'auto'
      },
      content: {
        type: String,
        default: NewsModel
      }
    },
    mounted() {
      this.SetProblemText();
    },
    data() {
      return {
        text: ''
      }
    },
    methods: {
      handleCopyCodeSuccess() {
        this.$message({
            type: "success",
            message: "复制成功",
          });
      },
      handleUploadImage(event, insertImage, files) {
        console.log(files);
        insertImage({
          url: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1269952892,3525182336&fm=26&gp=0.jpg',
          desc: '七龙珠',
          width: 'auto',
          height: 'auto',
        });
      },
      save(text) {
        // console.log(text);
        this.$emit('getContent', text);
      },
      SetProblemText() {
        this.text = this.content;
      }
    }
  }
</script>

<style>

</style>
