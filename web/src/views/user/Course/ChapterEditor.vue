<template>
  <div class="page">
    <div class="nav">
      <div class="nav-header">
        <span>章节目录</span>
        <el-button
          class="button"
          type="text"
          @click="append('menu')"
          v-if="page.power"
          >添加目录</el-button
        >
      </div>
      <div class="nav-content">
        <el-tree
          :data="course_data.course_catalog"
          :expand-on-click-node="false"
          :default-expand-all="true"
        >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span @click="switchTo(data.id)">{{ data.label }}</span>
              <span class="right" v-if="page.power">
                <el-button
                  type="text"
                  @click="append(data)"
                  v-if="node.level < 2"
                  >添加节点</el-button
                >
                <el-button type="text" @click="remove(data)">删除</el-button>
              </span>
            </span>
          </template>
        </el-tree>
      </div>
    </div>
    <div class="main">
      <div class="content-header" v-if="page.power">
        <el-button
          type="primary"
          @click="page.editor = !page.editor"
          size="mini"
          class="right"
        >
          {{ page.editor ? "预览" : "编辑" }}</el-button
        >
        <el-button type="success" @click="save()" size="mini" class="right"
          >保存</el-button
        >
      </div>
      <el-tabs
        type="card"
        :editable="page.power"
        @tab-add="page.add_action = true"
        @tab-remove="removeContent"
      >
        <el-tab-pane
          v-for="(item, index) in page.content"
          :key="index"
          :label="item.name"
          :name="index.toString()"
        >
          <MarkdownEditor
            v-if="item.type === 'text'"
            height="800px"
            :mode="page.editor ? 'editable' : 'preview'"
            :content="item.value"
            @getContent="getContent($event, index)"
          />
          <VideoPlay v-else-if="item.type === 'video'" :src="item.value" />
          <PDFShow v-else-if="item.type === 'ppt'" :src="item.value" />
        </el-tab-pane>
      </el-tabs>
    </div>
    <el-dialog v-model="page.add_action" title="内容类型" width="300px">
      <el-button @click="addContent('text')">文本</el-button>
      <el-button @click="addContent('video')">视频</el-button>
      <el-button @click="addContent('ppt')">PDF</el-button>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import MarkdownEditor from "@/components/editor/MarkdownEditor.vue";
import VideoPlay from "@/components/Other/VideoPlay.vue";
import PDFShow from "@/components/Other/PDFShow.vue";
import {
  addCourseChapter,
  getCourseChapter,
  deleteCourseChapter,
  addChapterContent,
  getUserPower,
} from "@/api/course";

let route = useRoute();
let router = useRouter();

let page = ref({
  course_id: route.params.course_id,
  add_action: false,
  editor: false,
  power: false,
  chapter_id: route.params.chapter_id,
  chapter_name: "",
  type: "",
  value: "",
  content: <any>[{}],
});

let course_data = ref({
  course_catalog: [
    {
      id: 1,
      label: "第一章 零零零零",
      children: [
        {
          id: 3,
          label: "第一节 树与图",
          content: [],
        },
        {
          id: 4,
          label: "第二节 二叉树",
          content: [],
        },
      ],
    },
    {
      id: 2,
      label: "第一章 零零零零",
      children: [
        {
          id: 5,
          label: "第一节 树与图",
          content: [],
        },
        {
          id: 6,
          label: "第二节 二叉树",
          content: [],
        },
      ],
    },
  ],
});

// 添加章节
let append = (data: any) => {
  ElMessageBox.prompt("请输入名称", "目录添加")
    .then(async ({ value }) => {
      // console.log(value, data);
      let back_data = await addCourseChapter({
        course_id: page.value.course_id,
        chapter_title: value,
        pre_chapter: data?.id || "",
      });
      console.log(back_data);
      if (back_data.status) {
        getChapter();
        ElMessage({
          type: "success",
          message: "添加成功",
        });
      } else {
        ElMessage({
          type: "error",
          message: "添加失败",
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消添加",
      });
    });
};
// 删除章节
let remove = async (data: any) => {
  let back_data = await deleteCourseChapter({
    chapter_id: data.id,
  });
  console.log(back_data);
  if (back_data.status) {
    getChapter();
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
// 添加内容
let addContent = (val: string) => {
  if (val === "text") {
    page.value.content.push({
      type: "text",
      name: "文本",
      value: "",
    });
    page.value.add_action = false;
  } else if (val === "video") {
    ElMessageBox.prompt("请输入视频地址", "视频添加")
      .then(({ value }) => {
        page.value.content.push({
          type: "video",
          name: "视频",
          value: value,
        });
        page.value.add_action = false;
      })
      .catch(() => {
        ElMessage({
          type: "info",
          message: "取消添加",
        });
      });
  } else if (val === "ppt") {
    ElMessageBox.prompt("请输入地址", "PDF添加")
      .then(({ value }) => {
        page.value.content.push({
          type: "ppt",
          name: "演示",
          value: value,
        });
        page.value.add_action = false;
      })
      .catch(() => {
        ElMessage({
          type: "info",
          message: "取消添加",
        });
      });
  }
};

// 删除内容
let removeContent = (val: any) => {
  page.value.content.splice(val, 1);
};

// 递归查找内容
let findChapter = (list: any, val: number) => {
  for (let o of list || []) {
    if (o.id === val) {
      return o;
    }
    const o_: any = findChapter(o.children, val);
    if (o_) {
      return o_;
    }
  }
};

// 切换到对应章节内容
let switchTo = (val: number) => {
  // console.log(val);
  router.push({
    path: `/coursedetails/${page.value.course_id}/chaptereditor/${val}`,
  });
  let temp = findChapter(course_data.value.course_catalog, val);
  page.value.chapter_id = temp?.id || 0;
  page.value.chapter_name = temp?.label || "";
  page.value.content = temp?.content || [];
  // console.log(temp);
};

// 监听路由

// 获取编辑器内容
let getContent = (res: string, val: number) => {
  page.value.content[val].value = res;
  // console.log(page.value);
};

// 保存内容
let save = async () => {
  let back_data = await addChapterContent({
    course_id: Number(page.value.course_id),
    chapter_id: page.value.chapter_id,
    chapter_content: JSON.stringify(page.value.content),
  });
  if (back_data.status) {
    getChapter();
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};

// 获取章节列表
let getChapter = async () => {
  let back_data = await getCourseChapter({
    course_id: Number(page.value.course_id),
    class_id: "",
  });
  // console.log(back_data);
  if (back_data.status) {
    course_data.value.course_catalog = formatChapterData(back_data.message);
  }
};

// 格式化章节内容
let formatChapterData = (val: any) => {
  return val.map((res: any) => ({
    id: res.chapter_id,
    label: res.chapter_title,
    children: res.section_list.map((res2: any) => ({
      id: res2.chapter_id,
      label: res2.chapter_title,
      content: res2.content_list || [],
    })),
  }));
};

// 获取用户身份
let getPower = async () => {
  let back_data = await getUserPower({
    course_id: page.value.course_id,
  });
  if (back_data.status) {
    page.value.power = back_data.message;
    // page.value.power = true;
  }
};

onMounted(() => {
  getPower();
  getChapter().then(() => {
    switchTo(Number(route.params.chapter_id) || 0);
  });
});
</script>

<style scoped lang="scss">
.page {
  width: 100%;
  .nav {
    width: 300px;
    float: left;
    border: 1px solid #999999;
    border-radius: 10px;
    overflow: hidden;
    .nav-header {
      height: 50px;
      line-height: 50px;
      border-bottom: 1px dotted #aaaaaa;
      padding: 0 20px;
      span {
        font-size: 20px;
        font-weight: bold;
      }
      button {
        float: right;
        line-height: 30px;
      }
    }
    .nav-content {
      width: 100%;
      height: 800px;
      overflow-y: auto;
      .custom-tree-node {
        width: 100%;
        .right {
          margin-left: 20px;
        }
      }
    }
  }
  .main {
    width: calc(100% - 350px);
    float: right;
    min-height: 300px;
    .content-header {
      width: 100%;
      height: 30px;
      line-height: 30px;
      border-bottom: 2px solid #aaaaaa;
      margin-bottom: 20px;
      display: flex;
      justify-content: end;
      .right {
        height: 20px;
      }
    }
  }
}
</style>
