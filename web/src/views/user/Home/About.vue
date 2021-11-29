<template>
  <div class="editor">
    <markdown-editor :content="text" mode="preview" />
  </div>
</template>

<script lang="ts" setup>
import HelpCenter from "@/assets/markdown/帮助中心.md?raw";
import ContactUs from "@/assets/markdown/联系我们.md?raw";
import UserAgreement from "@/assets/markdown/用户协议.md?raw";
import About52AC from "@/assets/markdown/关于52AC.md?raw";
import { getCurrentInstance } from "vue";
import { ref, watch } from "vue";
import markdownEditor from "@/components/Editor/MarkdownEditor.vue";
import { useRoute } from "vue-router";
let route = useRoute();

const Refresh = (val: String) => {
  switch (val) {
    case "HelpCenter":
      return HelpCenter;
    case "ContactUs":
      return ContactUs;
    case "UserAgreement":
      return UserAgreement;
    case "About52AC":
      return About52AC;
    default:
      return "";
  }
};
let text = ref("");
watch(
  () => route.params,
  (toParams) => {
    // console.log(toParams);
    text.value = Refresh(<string>toParams.filer);
  },
  {
    immediate: true,
    deep: false,
  }
);
</script>

<style scoped lang="scss">
.editor {
  width: 80%;
  max-width: 1200px;
  min-width: 360px;
  margin: 0 auto;
}
</style>
