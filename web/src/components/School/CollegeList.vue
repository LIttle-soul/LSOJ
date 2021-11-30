<template>
  <div class="college-list-child">
    <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
      <el-table-column prop="college_id" label="学院编号"> </el-table-column>
      <el-table-column prop="college_name" label="学院名称"> </el-table-column>
      <el-table-column prop="college_school" label="学院所在学校"> </el-table-column>
      <el-table-column fixed="right" width="80px" label="操作">
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
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page.page_size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page.page_size"
      layout="prev, pager, next"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  Data: {
    type: undefined,
    default: [],
  },
  page: {
    type: undefined,
    default: {
      page: 1,
      page_size: 50,
      total: 0,
    },
  },
});

// 向父组件传送事件
let emit = defineEmits(["handleSizeChange", "handlePageChange", "reload"]);

// 页面跳转
let handleSizeChange = (val: number) => {
  emit("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emit("handlePageChange", val);
};

// 事件相关操作函数
let handleEditClick = (val: any) => {
  console.log(val);
};
let handleCheckClick = (val: any) => {
  console.log(val);
};
let handleDeleteClick = (val: any) => {
  console.log(val);
};
</script>

<style scope lang="scss">
.button-box {
  display: flex;
  justify-content: space-around;
}
.college-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .college-list-child .pagination-2 {
    display: block;
  }
  .college-list-child .pagination-1 {
    display: none;
  }
}
</style>
