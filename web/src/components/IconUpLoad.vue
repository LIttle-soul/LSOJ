
<template>
<el-upload
  class="avatar-uploader"
  :action="imageurl"
  name="file"
  :data="IconForm"
  :show-file-list="false"
  :on-success="handleAvatarSuccess"
  :before-upload="beforeAvatarUpload"
>
  <el-avatar v-if="imageurl" size="small" shape="square" :src="imageurl+'?token=' + this.$cookies.get('token')" class="avatar"></el-avatar>
  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
</el-upload>
</template>

<script>
  export default {
    data() {
      return {
        imageurl: '/api/bindusericon/',
        IconForm: {
          token: this.$cookies.get('token')
        }
      };
    },
    methods: {
      handleAvatarSuccess(res, file) {
        alert('头像上传成功')
        location.reload();
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      }
    }
  }
</script>

<style>
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 80px;
    height: 80px;
    line-height: 80px;
    text-align: center;
  }
  .avatar {
    width: 80px;
    height: 80px;
    display: block;
  }
</style>
