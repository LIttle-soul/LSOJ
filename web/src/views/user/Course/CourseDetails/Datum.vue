<template>
  <div class="datum">
    <div class="datum-header">
      <div style="float: left">
        <el-input
          placeholder="请输入内容"
          size="small"
          v-model="page.text"
          class="input-with-select"
          @keydown.enter="search_all_data(page.text)"
        >
          <template #prefix>
            <el-icon
              color="#AAAAAA"
              style="font-size: 1.1rem; transform: translateY(7px)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1024 1024"
                data-v-394d1fd8=""
              >
                <path
                  fill="currentColor"
                  d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704z"
                ></path>
              </svg>
            </el-icon>
          </template>
          <template #append>
            <el-button @click="search_all_data(page.text)">搜索</el-button>
          </template>
        </el-input>
      </div>
      <div style="float: right">
        <el-upload
          action="/api/course/uploadfile/"
          :data="upload_data"
          name="file"
          :on-success="successUpload"
        >
          <el-button type="primary" v-show="page.user_identity">上传文件</el-button>
        </el-upload>
      </div>
    </div>
    <div style="margin-top: 20px">
      <el-table :data="materialData" border style="width: 100%">
        <el-table-column prop="file_name" label="文件名"></el-table-column>
        <el-table-column prop="file_type" label="文件类型" />
        <el-table-column prop="upload_user_name" label="上传者" />
        <el-table-column prop="file_size" label="大小" />
        <el-table-column prop="upload_time" label="上传日期" />
        <el-table-column label="操作">
          <template #default="scope">
            <div class="button-box">
              <el-button
                size="medium"
                type="success"
                :icon="Check"
                circle
                @click="handleDownloadClick(scope.row)"
              >
              </el-button>
              <el-button
                size="medium"
                type="danger"
                :icon="Delete"
                circle
                @click="handleDeleteClick(scope.row)"
                v-show="page.user_identity"
              ></el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Check, Delete } from "@element-plus/icons-vue";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElLoading, ElMessage, ElMessageBox } from "element-plus";
import { getDatum, deleteFile, downLoad, getUserPower } from "@/api/course";
import dayJS from "dayjs";

let router = useRouter();
let route = useRoute();

let page = ref({
  course_id: route.params.course_id,
  shoa: false,
  options: <any>[],
  value: "",
  text: "",
  user_identity: 1,
});
console.log(page.value.course_id);
let upload_data = ref({
  filename: "",
  course_id: page.value.course_id,
});

let successUpload = () => {
  getDatumData();
  ElMessage({
    type: "success",
    message: "上传成功",
  });
};

//资料虚拟数据
let materialData = ref([
  {
    file_id: 0,
    file_name: "教学视频",
    upload_user_name: "烟雨",
    file_size: "32MB",
    upload_time: "2021-12-18",
    file_type: "文件",
  },
]);

let formatDatumData = (val: any) => {
  return val.map((res: any) => ({
    file_id: res.file_id,
    file_name: res.file_name,
    upload_user_name: res.user_name,
    upload_time: dayJS(res.create_time).format("YYYY-MM-DD"),
    file_type: res.file_type,
    file_size: res.size,
  }));
};

let search_all_data = (text: string) => {
  page.value.text = text || "";
  getDatumData();
};

let getDatumData = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,7)",
  });
  let back_data = await getDatum({
    course_id: Number(page.value.course_id),
    text: page.value.text,
  });
  if (back_data.status) {
    materialData.value = formatDatumData(back_data.message);
    loading.close();
  } else {
    loading.close();
  }
};
let handleDownloadClick = async (val: any) => {
  // console.log(val)
  let back_data = await downLoad({
    file_id: val.file_id,
  });
  if (back_data.status) {
    let ele = document.createElement("a");
    ele.setAttribute("href", `/api/course/uploadfile/?file_id=${val.file_id}`);
    ele.setAttribute("download", back_data.message);
    ele.click();
  }
};
let handleDeleteClick = (val: any) => {
  ElMessageBox.confirm("确定要删除这个文件吗？删除后无法恢复哦。", "确认消息", {
    cancelButtonText: "取消",
    confirmButtonText: "确认",
    type: "warning",
  })
    .then(async () => {
      let back_data = await deleteFile({
        file_id: val.file_id,
      });
      console.log(back_data);
      if (back_data.status) {
        getDatumData();
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      } else {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消删除",
      });
    });
};
let getPower = async () => {

let getPower=async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中",
    background: "rgba(0,0,0,7)"
  });
  let back_data = await getUserPower({
    course_id: Number(route.query.course_id)
  });
  console.log(back_data);
  if (back_data.status){
    page.value.user_identity = back_data.message;
    loading.close();
  }else{
    loading.close();
  }
}
}
onMounted(() => {
  getDatumData();
  getPower();
});
</script>

<style lang="scss" scoped>
.datum {
  max-width: 1100px;
  width: 1100px;
  margin: 10px auto;
  .datum-header {
    height: 40px;
    margin-top: 20px;
  }
}
</style>
