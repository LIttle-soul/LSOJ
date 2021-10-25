<template>
  <input type="file" ref="myfile">
  <el-button @click="importData">添加</el-button>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      fileList: [
        {
          name: "food.jpeg",
          url:
            "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100",
        },
        {
          name: "food2.jpeg",
          url:
            "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100",
        },
      ],
    };
  },
  methods: {
    importData() {
        let myfile = this.$refs.myfile;
        let files = myfile.files;
        let file = files[0];
        var formData = new FormData();
        formData.append("images", file);
        console.log(formData, file);
        axios.post("/api/problem/upimage", formData).then(res => {
            console.log(res);
        })
    }
  },
};
</script>

<style></style>
