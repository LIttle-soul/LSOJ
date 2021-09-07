<template>
<div class="add-discussion">
    <div class="header">
      <el-input v-model="title" placeholder="标题"></el-input>
      <el-button @click="submitDiscussion" type="success" plain>提交</el-button>
    </div>
    <v-md-editor height="600px" v-model="content"></v-md-editor>
    
</div>
</template>

<script>
  import { ElMessage } from 'element-plus'

  export default {
    mounted() {
      if (this.p_title != "") {
        this.id = this.p_id;
        this.title = this.p_title;
        this.content = this.p_content;
      }
    },
    props: ["type", "p_id", "p_title", "p_content"],
    data() {
      return {
        id: 0,
        title: "",
        content: "",
      }
    },
    methods: {
      submitDiscussion() {
        if (this.type != "modify") {
          this.createDiscussion();
        }
        else {
          this.modifyDiscussion();
        }
      },
      createDiscussion() {
        this.$http({
          url: "/api/forum/createforum/",
          method: "post",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          transformRequest: [
            function(data) {
              let ret = "";
              for (let it in data) {
                ret +=
                  encodeURIComponent(it) +
                  "=" +
                  encodeURIComponent(data[it]) +
                  "&";
              }
              return ret;
            },
          ],
          data: {
            token: this.$cookies.get('token'),
            forum_title: this.title,
            forum_content: this.content,
            forum_section: 0,
            section_id: 0
          }
        })
          .then((response) => {
            console.log(response);
            if (response.data.err !== undefined) {
              ElMessage(response.data.err);
              console.log(response.data.err);
            }
            else { 
              ElMessage.success({
                message: '添加成功',
                type: 'success'
              });
              this.$router.replace({
                name:'Discussion',
                params: {
                  id: response.data.forum_id
                }
              });
            }
          })
          .catch((error) => {
            console.log(error);
          });
      },
      modifyDiscussion() {
        this.$http({
          url: "/api/forum/modifyforum/",
          method: "post",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          transformRequest: [
            function(data) {
              let ret = "";
              for (let it in data) {
                ret +=
                  encodeURIComponent(it) +
                  "=" +
                  encodeURIComponent(data[it]) +
                  "&";
              }
              return ret;
            },
          ],
          data: {
            token: this.$cookies.get('token'),
            forum_id: this.id,
            forum_title: this.title,
            forum_content: this.content
          }
        })
          .then((response) => {
            console.log(response);
            if (response.data.err !== undefined) {
              ElMessage(response.data.err);
              console.log(response.data.err);
            }
            else { 
              ElMessage.success({
                message: '修改成功',
                type: 'success'
              });
              this.$emit("modifyDiscussion", false);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    watch: {
      p_id(now) {
        this.id = now;
      },
      p_title(now) {
        this.title = now;
      },
      p_content(now) {
        this.content = now;
      }
    }
  }
</script>

<style scoped>

  .add-discussion {
    width: 80%;
    max-width: 1200px;
    margin: 70px auto;

    word-break: break-all;
    font: "圆体"
  }
  .add-discussion .header{
    display: flex
  }

  .add-discussion .main {
    height: 400px;
    overflow: auto;
  }

  @media screen and (max-width: 600px) {
    .add-discussion {
      width: 100%;
    }
  }
</style>
