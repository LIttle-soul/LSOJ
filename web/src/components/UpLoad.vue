
<template>
<el-upload
  class="upload-demo"
  name="hunter"
  :data="FormData"
  drag
  :action="url"
  multiple>
  <i class="el-icon-upload"></i>
  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
  <template #tip>
    <div class="el-upload__tip">
      只能上传 jpg/png 文件，且不超过 500kb
    </div>
  </template>
</el-upload>
</template>

<script>
 export default {
   data() {
     return {
       url: '/api/upload/',
       FormData: {
         token: this.$cookies.get('token')
       }
     }
   }
 }
</script>

<style>

</style>
