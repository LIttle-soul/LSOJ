<template>
  <div class="page">
    <div class="teacher-header" v-show="page.user_power">
      <el-select
        v-model="page.cur_class"
        placeholder="请选择班级"
        @change="getChapterList()"
      >
        <el-option
          v-for="item in page.class_list"
          :key="item.class_id"
          :label="item.class_name"
          :value="item.class_id"
        >
        </el-option>
      </el-select>
      <el-button type="primary" @click="setCourse" class="search-button"
        >编辑</el-button
      >
    </div>
    <div class="main">
      <div class="tree-header">
        <span class="catalog">目录</span>
        <span class="action">
          <span v-show="page.user_power">发放</span>
          <span>状态</span>
        </span>
      </div>
      <div class="tree-content">
        <el-tree
          :data="course_data.course_chapter"
          :default-expand-all="true"
          :expand-on-click-node="false"
        >
          <template #default="{ node, data }">
            <div class="tree-node">
              <span class="menu" @click="studyCourse(data, node)">{{
                node.label
              }}</span>
              <span class="action">
                <el-popover placement="left" :width="400" trigger="click">
                  <template #reference>
                    <el-button
                      type="text"
                      @click="giveOutCourse(node, data)"
                      v-show="page.user_power"
                      class="button"
                    >
                      <el-icon style="font-size: 18px">
                        <CircleCheck />
                      </el-icon>
                    </el-button>
                  </template>
                  <el-radio-group v-model="page.radio">
                    <el-radio label="3">
                      <el-icon>
                        <Key />
                      </el-icon>
                      <span style="font-size: 12px"
                        >公开（该章节学生可见，可学习）</span
                      >
                    </el-radio>
                    <el-radio label="6">
                      <el-icon>
                        <AlarmClock />
                      </el-icon>
                      <span style="font-size: 12px">定时发放</span>
                      <el-date-picker
                        v-model="page.value2"
                        type="datetimerange"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
                        size="mini"
                        style="width: 310px"
                      >
                      </el-date-picker>
                    </el-radio>
                    <el-radio label="12">
                      <el-icon>
                        <Lock />
                      </el-icon>
                      <span style="font-size: 12px"
                        >隐藏章节（该章节学生不可见）</span
                      >
                    </el-radio>
                  </el-radio-group>
                </el-popover>
                <el-progress
                  type="circle"
                  :percentage="+data.progress"
                  :width="18"
                  :stroke-width="4"
                  :show-text="false"
                  status="success"
                  class="button"
                ></el-progress>
              </span>
            </div>
          </template>
        </el-tree>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  Check,
  CircleCheck,
  AlarmClock,
  Key,
  Coordinate,
  Lock,
} from "@element-plus/icons";
import { ElLoading } from "element-plus";
import { getCourseChapter, getClassList, getUserPower } from "@/api/course";

let route = useRoute();
let router = useRouter();

let page = ref({
  course_id: route.params.course_id,
  user_power: false,
  class_list: [{ class_id: 1, class_name: "软件191" }],
  cur_class: "",
  image: "",
  value2: "",
  radio: "",
});

// 课程目录数据
let course_data = ref({
  course_chapter: [
    {
      label: "第一章 链表",
      progress: 10,
      id: 1,
      children: [
        {
          id: 3,
          label: "第一节 单链表",
          progress: 80,
        },
        {
          id: 4,
          label: "第二节 双向链表",
          progress: 40,
        },
      ],
    },
    {
      label: "第二章 图",
      id: 2,
      progress: 10,
      children: [
        {
          id: 5,
          label: "第一节 深搜",
          progress: 20,
        },
        {
          id: 6,
          label: "第二节 广搜",
          progress: 10,
        },
      ],
    },
  ],
});

// 编辑章节
let setCourse = async () => {
  router.push({
    path: `/coursedetails/${page.value.course_id}/chaptereditor/0`,
  });
};

// 发放课程
let giveOutCourse = (val: any, value: any) => {
  console.log(val, value);
};
// 进入学习
let studyCourse = (data: any, node: any) => {
  if (node.level === 2) {
    router.push({
      path: `/coursedetails/${page.value.course_id}/chaptereditor/${data.id}`,
    });
  }
};

// 获取章节列表
let getChapterList = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中...",
    background: "rgba(0,0,0,0.6)",
  });
  let back_data = await getCourseChapter({
    course_id: Number(page.value.course_id),
    class_id: page.value.cur_class || "",
  });
  // console.log(back_data);
  if (back_data.status) {
    course_data.value.course_chapter = formatChapterList(back_data.message);
    loading.close();
  } else {
    loading.close();
  }
};

// 格式化章节列表数据
let formatChapterList = (val: any) => {
  return val.map((res: any) => ({
    id: res.chapter_id,
    label: res.chapter_title,
    progress: res.chapter_finish,
    children: res.section_list.map((res2: any) => ({
      id: res2.chapter_id,
      label: res2.chapter_title,
      progress: res2.chapter_finish,
    })),
  }));
};

// 获取课程班级
let getCourseClass = async () => {
  let back_data = await getClassList({
    course_id: page.value.course_id,
  });
  // console.log(back_data);
  if (back_data.status) {
    page.value.class_list = formatClass(back_data.message);
  }
};

// 格式化课程班级
let formatClass = (val: any) => {
  return val.map((res: any) => ({
    class_id: res.class_id,
    class_name: res.class_name,
  }));
};

// 获取用户权限
let getPower = async () => {
  let back_data = await getUserPower({
    course_id: page.value.course_id,
  });
  if (back_data.status) {
    if (back_data.message) {
      page.value.user_power = true;
      getCourseClass();
    } else {
      page.value.user_power = false;
    }
  }
};

// 挂载加载数据
onMounted(() => {
  getPower();
  getChapterList();
});
</script>

<style lang="scss" scoped>
.page {
  width: 100%;
  .teacher-header {
    padding: 10px 20px;
    border-bottom: 3px dotted #aaaaaa;
    .search-button {
      margin-left: 10px;
    }
  }
  .main {
    margin-top: 20px;
    width: 100%;
    .tree-header {
      width: 100%;
      height: 30px;
      line-height: 30px;
      .catalog {
        width: 50%;
      }
      .menu {
        float: left;
        width: 50%;
        text-align: center;
      }
      .action {
        float: right;
        span {
          margin: 0 20px;
        }
      }
    }
    .tree-content {
      .tree-node {
        width: 100%;
        height: 40px;
        line-height: 40px;
        .menu {
          float: left;
          width: 50%;
        }
        .action {
          float: right;
          .button {
            margin: 0 25px;
          }
        }
      }
    }
  }
}
</style>
