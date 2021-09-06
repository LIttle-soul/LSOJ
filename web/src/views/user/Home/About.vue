<template>
<div class="editor">
  <v-md-editor 
  v-model="text" 
  mode='preview' 
  @copy-code-success="handleCopyCodeSuccess"></v-md-editor>
  </div>
</template>

<script>
import HelpCenter from '@/assets/markdown/帮助中心.md';
import ContactUs from '@/assets/markdown/联系我们.md';
import UserAgreement from '@/assets/markdown/用户协议.md';
import About52AC from '@/assets/markdown/关于52AC.md';

export default {
  created() {
    this.Refresh(this.$route.params.filer)
    this.$watch(
      () => this.$route.params,
      (toParams, ) => {
        this.Refresh(toParams.filer);
      }
    )
  },
  data() {
    return {
      text: HelpCenter,
    };
  },
  methods: {
    handleCopyCodeSuccess() {
      this.$message({
            type: "success",
            message: "复制成功",
          });
    },
    Refresh(val) {
      switch(val) {
      case 'HelpCenter':
        this.text = HelpCenter;
        break;
      case 'ContactUs':
        this.text = ContactUs;
        break;
      case 'UserAgreement':
        this.text = UserAgreement;
        break;
      case 'About52AC':
        this.text = About52AC;
        break;
    }
    }
  }
};
</script>

<style scoped>
.editor {
  width: 80%;
  max-width: 1200px;
  min-width: 360px;
  margin: 0 auto;
}
</style>