<template>
  <div class="problem-data-list">
    <el-table :data="problem_data">
      <el-table-column prop="data_title" label="文件名称"></el-table-column>
      <el-table-column prop="data_size" label="文件大小"></el-table-column>
      <el-table-column prop="creator_time" label="创建日期"></el-table-column>
      <el-table-column prop="data_type" label="文件类型"></el-table-column>
      <el-table-column fixed="right" width="148px" label="操作">
        <template #default="scope">
          <div class="button-box">
            <el-button
              size="mini"
              type="primary"
              circle
              @click="handleEditClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="warning"
              circle
              @click="handleBoxClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-archive"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
            <el-dialog
              :title="scope.row.data_title"
              v-model="scope.row.dialog"
              :destroy-on-close="true"
            >
              <el-input
                v-model="scope.row.data_text"
                :rows="10"
                type="textarea"
              ></el-input>
              <template #footer>
                <el-button type="success" @click="handleCheckClick(scope.row)"
                  >提交</el-button
                >
              </template>
            </el-dialog>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="dialog-footer">
      <el-upload
        action="/api/problem/problemsample/"
        name="files"
        :data="{ problem_id: props.problem_id }"
        :on-success="successUploadTestData"
        :show-file-list="false"
        :drag="true"
        :multiple="true"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将上传文件拖到此处或点击上传</div>
      </el-upload>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  getProblemTestData,
  changeProblemTestData,
  changeProblemTestName,
  deleteProblemTestData,
} from "@/api/problem";
import { ElMessageBox, ElMessage, ElLoading } from "element-plus";
import { ref, reactive, onMounted } from "vue";
import dayJS from "dayjs";

let props = defineProps({
  problem_id: {
    type: Number,
    default: 0,
  },
});

let problem_data = ref([
  {
    data_title: "test1.in",
    data_size: "1176bytes",
    creator_time: "2020-01-01 08:06:00",
    data_type: "in",
    data_text: "Hello",
    dialog: false,
  },
]);

let successUploadTestData = () => {
  ElMessage({
    type: "success",
    message: "上传成功",
  });
  getProblemTest();
};
let handleEditClick = (val: any) => {
  ElMessageBox.prompt("请输入文件名", "文件名", {
    confirmButtonText: "保存",
    cancelButtonText: "取消",
  })
    .then(async ({ value }) => {
      let back_data = await changeProblemTestName({
        problem_id: props.problem_id,
        files_name: val.data_title,
        new_name: value.split(".").length > 1 ? value : value + "." + val.data_type,
      });
      if (back_data.status) {
        ElMessage({
          type: "success",
          message: back_data.message,
        });
        getProblemTest();
      } else {
        ElMessage({
          type: "error",
          message: back_data.message,
        });
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "未作修改",
      });
    });
};
let handleCheckClick = async (val: any) => {
  let back_data = await changeProblemTestData({
    problem_id: props.problem_id,
    files_name: val.data_title,
    files_text: val.data_text,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    getProblemTest();
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleDeleteClick = async (val: any) => {
  let back_data = await deleteProblemTestData({
    problem_id: props.problem_id,
    files_name: val.data_title,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    getProblemTest();
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleBoxClick = (val: any) => {
  val.dialog = true;
};
let formatData = (val: any) => {
  return val.map((item: any) => ({
    data_title: item.files_name,
    data_size: item.files_size + " bit",
    creator_time: dayJS(item.creator_time).format("YYYY-MM-DD"),
    data_type: item.files_ext,
    data_text: item.files_text,
    dialog: false,
  }));
};
let getProblemTest = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中......",
    background: "rgba(0,0,0,0.7)",
  });
  let back_data = await getProblemTestData({
    problem_id: props.problem_id,
  });
  if (back_data.status) {
    problem_data.value = formatData(back_data.message);
    loading.close();
  } else {
    problem_data.value = <any>[];
    loading.close();
  }
};
onMounted(() => {
  getProblemTest();
});
</script>

<style scoped lang="scss">
.problem-data-list {
  width: 100%;
  min-height: 400px;
  max-height: calc(100vh - 500px);
  overflow: auto;
  .dialog-footer {
    float: right;
    margin-top: 10px;
  }
  .button-box {
    display: flex;
    justify-content: space-around;
  }
}
</style>
