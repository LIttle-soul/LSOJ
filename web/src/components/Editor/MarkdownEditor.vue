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
    @copy-code-success="handleCopyCodeSuccess"
  ></v-md-editor>
</template>
<script>
import { upLoadImages } from "@/api/editor";
export default {
  props: {
    mode: {
      type: String,
      default: "editable",
    },
    height: {
      type: String,
      default: "auto",
    },
    content: {
      type: String,
      default: "",
    },
  },
  mounted() {
    this.SetText();
  },
  data() {
    return {
      text: "",
    };
  },
  methods: {
    handleCopyCodeSuccess() {
      this.$message({
        type: "success",
        message: "复制成功",
      });
    },
    async handleUploadImage(event, insertImage, files) {
      let data = await upLoadImages(files);
      console.log(data);
      insertImage({
        url: '/api/files/' + data.message,
        desc: undefined,
        width: "auto",
        height: "auto",
      });
    },
    save(text) {
      // console.log(text);
      this.$emit("getContent", text);
    },
    SetText() {
      this.text = this.content;
    },
  },
};
</script>
