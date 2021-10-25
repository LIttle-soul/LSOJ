<template>
  <div class="school-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column prop="school_id" label="学校编号"> </el-table-column>
      <el-table-column prop="school_name" label="学校名称"> </el-table-column>
      <el-table-column prop="school_describe" label="学校描述">
      </el-table-column>
      <el-table-column prop="school_department" label="主管部门">
      </el-table-column>
      <el-table-column prop="school_rank" label="办学层次"> </el-table-column>
      <el-table-column prop="school_remark" label="学校备注"> </el-table-column>
      <el-table-column prop="school_municipality" label="学校所在城市">
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
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="total, sizes, prev, pager, next, jumper"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="prev, pager, next"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  name: "schoolListChild",
  props: {
    Data: {
      type: undefined,
      default: [],
    },
  },
  data() {
    return {
      current_page: 1,
      page_sizes: 50,
    };
  },
  methods: {
    handleEditClick() {
      this.$router.push({
        name: "AdminAddschool",
      });
    },
    handleCheckClick() {
      console.log(this.Data);
    },
    handleDeleteClick(val) {
      console.log(val);
    },
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
  },
};
</script>

<style scope>
.school-list-child .pagination-2 {
  display: none;
}
.edit {
  margin-bottom: 2%;
}
@media screen and (max-width: 600px) {
  .school-list-child .pagination-2 {
    display: block;
  }
  .school-list-child .pagination-1 {
    display: none;
  }
}
</style>
