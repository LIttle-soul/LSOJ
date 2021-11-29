<template>
  <div class="class-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          班级管理
        </div>
        <el-input
          placeholder="请输入内容"
          size="mini"
          v-model="search_data"
          class="input-with-select"
        >
          <template #append>
            <el-button
              icon="el-icon-search"
              @click="search_all_data"
            ></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <el-table
          :data="
            Data.slice(
              (page.cur - 1) * page.page_size,
              page.cur * page.page_size
            )
          "
          size="mini"
          :stripe="true"
          :fit="true"
          style="width: 100%"
        >
          <el-table-column prop="class_id" label="班级编号"> </el-table-column>
          <el-table-column prop="class_name" label="班级名称">
          </el-table-column>
          <el-table-column prop="class_introduce" label="班级介绍">
          </el-table-column>
          <el-table-column prop="class_type" label="班级类型">
          </el-table-column>
          <el-table-column prop="class_creator" label="创建者">
          </el-table-column>
          <el-table-column prop="class_college" label="班级所在学院">
          </el-table-column>
          <el-table-column fixed="right" width="125px" label="操作">
            <template #default="scope">
              <el-button
                size="mini"
                type="primary"
                circle
                icon="el-icon-edit"
                @click="handleEditClick(scope.row)"
              >
              </el-button>
              <el-button
                size="mini"
                type="danger"
                circle
                icon="el-icon-delete"
                @click="handleDeleteClick(scope.row)"
              >
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        class="pagination-1"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page.cur"
        :page-sizes="[20, 50, 100, 200]"
        :page-size="page.page_size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="Data.length"
        :hide-on-single-page="true"
      >
      </el-pagination>
      <el-pagination
        class="pagination-2"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page.cur"
        :page-sizes="[20, 50, 100, 200]"
        :page-size="page.page_size"
        layout="prev, pager, next"
        :total="Data.length"
        :hide-on-single-page="true"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
let search_data = ref("");
let search_all_data = ref("");

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  Data: {
    type: undefined,
    default: [],
  },
});
let page = ref({
  cur: 1,
  page_size: 50,
});
let handleSizeChange = (val: number) => {
  page.value.page_size = val;
};

let handleCurrentChange = (val: number) => {
  page.value.cur = val;
};
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

<style scope>
.class-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.class-list-child .el-card__header {
  height: 60px;
}
.class-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.class-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.class-list-child .pagination-2 {
  display: none;
}
.edit {
  margin-bottom: 2%;
}
@media screen and (max-width: 600px) {
  .class-list-child .input-with-select {
    display: none;
  }
  .class-list-child .pagination-2 {
    display: block;
  }
  .class-list-child .pagination-1 {
    display: none;
  }
}
</style>
