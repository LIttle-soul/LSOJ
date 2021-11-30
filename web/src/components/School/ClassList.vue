<template>
  <div class="class-list-child">
    <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
      <el-table-column prop="class_id" label="班级编号"> </el-table-column>
      <el-table-column prop="class_name" label="班级名称"> </el-table-column>
      <el-table-column prop="class_introduce" label="班级介绍"> </el-table-column>
      <el-table-column prop="class_type" label="班级类型"> </el-table-column>
      <el-table-column prop="class_creator" label="创建者"> </el-table-column>
      <el-table-column prop="class_college" label="班级所在学院"> </el-table-column>
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
.class-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .class-list-child .pagination-2 {
    display: block;
  }
  .class-list-child .pagination-1 {
    display: none;
  }
}
</style>
