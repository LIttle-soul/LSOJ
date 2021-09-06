<template>
  <div class="problem-data-list">
    <el-table :data="problem_data">
      <el-table-column prop="data_title" label="文件名称"></el-table-column>
      <el-table-column prop="data_size" label="文件名称"></el-table-column>
      <el-table-column prop="creator_time" label="创建日期"></el-table-column>
      <el-table-column prop="data_type" label="文件类型"></el-table-column>
      <el-table-column fixed="right" width="162px" label="操作">
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
            icon="el-icon-check"
            @click="handleCheckClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            circle
            icon="el-icon-delete"
            @click="handleDeleteClick(scope.row)"
          ></el-button>
          <el-button
            size="mini"
            type="warning"
            circle
            icon="el-icon-box"
            @click="handleDataClick(scope.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  setup() {},
  data() {
    return {
      problem_data: [
        {
          data_title: "test1.in",
          data_size: "1176bytes",
          creator_time: "2020-01-01 08:06:00",
          data_type: "in",
        },
      ],
    };
  },
  methods: {
    handleEditClick(val) {
      console.log(val);
    },
    handleCheckClick(val) {
      console.log(val);
    },
    handleDeleteClick(val) {
      console.log(val);
    },
    handleDataClick(val) {
      console.log(val);
    },
  },
};
</script>
