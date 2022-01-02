<template>
  <div>
    <el-table :data="props.Data" style="width: 100%">
      <el-table-column prop="forum_id" width="100px" label="论坛编号" />
      <el-table-column label="论坛标题">
        <template #default="scope">
          <div>{{ scope.row.forum_title?.slice(0, 30) }}</div>
        </template>
      </el-table-column>
      <el-table-column label="论坛内容">
        <template #default="scope">
          <div class="forum_title">
            {{ scope.row.forum_content?.slice(0, 30) + "..." }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="forum_section" width="100px" label="论坛板块" />
      <el-table-column prop="section_id" width="100px" label="版块编号" />
      <el-table-column prop="create_time" width="180px" label="创建时间" />
      <el-table-column prop="forum_top" width="50px" label="置顶">
        <template #default="scope">
          <el-switch
            v-model="scope.row.forum_top"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @click="upTheForum(scope.row.forum_id)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column prop="forum_status" width="50px" label="状态">
        <template #default="scope">
          <el-switch
            v-model="scope.row.forum_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @click="putTheForumStatus(scope.row.forum_id)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="130px">
        <template #default="scope">
          <div class="forum_button">
            <el-button
              size="mini"
              circle
              @click="
                getForumData({
                  forum_id: scope.row.forum_id,
                  forum_content: scope.row.forum_content,
                })
              "
              ><el-icon><Search /></el-icon
            ></el-button>
            <el-button
              type="primary"
              size="mini"
              circle
              @click="
                putForum({
                  forum_id: scope.row.forum_id,
                  forum_title: scope.row.forum_title,
                  forum_content: scope.row.forum_content,
                  forum_section: scope.row.forum_section,
                  section_id: scope.row.section_id,
                })
              "
              ><el-icon><Edit /></el-icon
            ></el-button>
            <el-button
              type="danger"
              size="mini"
              circle
              @click="deleteTheForum(scope.row.forum_id)"
              ><el-icon><Delete /></el-icon
            ></el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import { Search, Edit, Delete } from "@element-plus/icons";
import { deleteForum, upForum, putForumStatus } from "@/api/forum";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

let router = useRouter();
let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
});
let emits = defineEmits(["deleteForum", "upForum"]);

let getForumData = (val: any) => {
  router.push({
    path: "/showforum",
    query: {
      forum_id: val.forum_id,
      forum_content: val.forum_content,
    },
  });
};
let putForum = (val: any) => {
  router.push({
    path: "/createforum",
    query: {
      forum_id: val.forum_id,
      forum_section: val.forum_section,
      section_id: val.section_id,
      forum_title: val.forum_title,
      forum_content: val.forum_content,
    },
  });
};
let deleteTheForum = async (val: number) => {
  let data = {
    forum_id: val,
  };
  let forum = await deleteForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    emits("deleteForum");
  } else {
    ElMessage.error(forum.message);
  }
};
let upTheForum = async (val: number) => {
  let data = {
    forum_id: val,
  };
  let forum = await upForum(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    emits("upForum");
  } else {
    ElMessage.error(forum.message);
  }
};
let putTheForumStatus = async (val: number) => {
  let data = {
    forum_id: val,
  };
  let forum = await putForumStatus(data);
  if (forum.status) {
    ElMessage({
      message: forum.message,
      type: "success",
    });
    emits("upForum");
  } else {
    ElMessage.error(forum.message);
  }
};
let ellipsis = (value: string) => {
  if (!value) return "";
  if (value.length > 30) {
    return value.slice(0, 30) + "...";
  }
  return value;
};
</script>

<style scoped lang="scss">
.forum_button {
  display: flex;
}
.fourm_title {
  width: 200px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
