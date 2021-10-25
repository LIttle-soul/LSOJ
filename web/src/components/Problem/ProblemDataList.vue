<template>
  <div class="problem-data-list">
    <el-table :data="problem_data">
      <el-table-column prop="data_title" label="文件名称"></el-table-column>
      <el-table-column prop="data_size" label="文件大小"></el-table-column>
      <el-table-column prop="creator_time" label="创建日期"></el-table-column>
      <el-table-column prop="data_type" label="文件类型"></el-table-column>
      <el-table-column fixed="right" width="148px" label="操作">
        <template #default="scope">
          <el-button
            size="mini"
            type="primary"
            circle
            icon="el-icon-edit"
            @click="handleEditClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="success"
            circle
            icon="el-icon-box"
            @click="handleBoxClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            icon="el-icon-delete"
            @click="handleDeleteClick(scope.row)"
          ></el-button>
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
        </template>
      </el-table-column>
    </el-table>
    <div class="dialog-footer">
      <el-upload
        action="/api/problem/problemsample/"
        name="files"
        :data="{ problem_id: problem_id }"
        :on-success="successUploadTestData"
        :show-file-list="false"
        :drag="true"
        :multiple="true"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将上传文件拖到此处或点击上传
        </div>
      </el-upload>
    </div>
  </div>
</template>

<script>
import {
  getProblemTestData,
  changeProblemTestData,
  changeProblemTestName,
  deleteProblemTestData,
} from "@/api/problem";
import { ElMessageBox } from "element-plus";

export default {
  props: {
    problem_id: {
      type: Number,
      default: 0,
    },
  },
  created() {
    this.getTestData(this.problem_id);
    // console.log("gua zai")
  },
  data() {
    return {
      problem_data: [
        {
          data_title: "test1.in",
          data_size: "1176bytes",
          creator_time: "2020-01-01 08:06:00",
          data_type: "in",
          data_text: "Hello",
          dialog: false,
        },
      ],
    };
  },
  methods: {
    successUploadTestData() {
      this.$message({
        type: "success",
        message: "上传成功",
      });
      this.getTestData(this.problem_id);
    },
    async getTestData(problem_id) {
      // console.log(problem_id);
      let val = await getProblemTestData(problem_id);
      if (val.status) {
        this.problem_data = this.formatData(val.message);
      }
      // console.log(val);
    },
    handleEditClick(val) {
      ElMessageBox.prompt("请输入文件名", "文件名", {
        confirmButtonText: "保存",
        cancelButtonText: "取消",
      })
        .then(async ({ value }) => {
          let back_data = await changeProblemTestName({
            problem_id: this.problem_id,
            data_title: val.data_title,
            new_title:
              value.split(".").length > 1 ? value : value + "." + val.data_type,
          });
          if (back_data.status) {
            this.$message({
              type: "sucess",
              message: back_data.message,
            });
            this.getTestData(this.problem_id);
          } else {
            this.$message({
              type: "error",
              message: back_data.message,
            });
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "未作修改",
          });
        });
    },
    async handleCheckClick(val) {
      let back_data = await changeProblemTestData({
        problem_id: this.problem_id,
        data_title: val.data_title,
        data_text: val.data_text,
      });
      if (back_data.status) {
        this.$message({
          type: "sucess",
          message: back_data.message,
        });
        this.getTestData(this.problem_id);
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async handleDeleteClick(val) {
      let back_data = await deleteProblemTestData({
        problem_id: this.problem_id,
        data_title: val.data_title,
      });
      if (back_data.status) {
        this.$message({
          type: "sucess",
          message: back_data.message,
        });
        this.getTestData(this.problem_id);
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    handleBoxClick(val) {
      val.dialog = true;
      // console.log(val)
    },
    formatData(val) {
      return val.map((item) => ({
        data_title: item.files_name,
        data_size: item.files_size + " bit",
        creator_time: this.$dayJS(item.creator_time).format("YYYY-MM-DD"),
        data_type: item.files_ext,
        data_text: item.files_text,
        dialog: false,
      }));
    },
  },
};
</script>

<style scoped>
.problem-data-list {
  width: 100%;
  min-height: 400px;
  max-height: calc(100vh - 500px);
  overflow: auto;
}
.dialog-footer {
  float: right;
  margin-top: 10px;
}
</style>
