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
<script lang="ts" setup>
import { upLoadImages } from "@/api/editor";
import { ElMessage } from "element-plus";
import { ref, watch } from "vue";

let props = defineProps({
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
});

let emits = defineEmits(["getContent"]);

let text = ref("");

let handleCopyCodeSuccess = () => {
  ElMessage({
    type: "success",
    message: "复制成功",
  });
};
let handleUploadImage = async (event: any, insertImage: any, files: any) => {
  let data = await upLoadImages(files);
  // console.log(data);
  insertImage({
    url: "/api/files/" + data.message,
    desc: undefined,
    width: "auto",
    height: "auto",
  });
};
let save = (text: any) => {
  emits("getContent", text);
};
watch(
  props,
  () => {
    text.value = props.content;
  },
  {
    immediate: true,
  }
);
</script>
