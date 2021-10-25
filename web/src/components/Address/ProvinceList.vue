<template>
  <div class="province-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
      :default-sort="{ prop: 'province_id', order: 'descending' }"
    >
      <el-table-column prop="province_id" label="省份编号"> </el-table-column>
      <el-table-column prop="province_name" label="省份名称"> </el-table-column>
      <el-table-column fixed="right" width="130px" label="操作" v-if="admin">
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
  name: "ProvinceListChild",
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
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
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },

    handleEditClick(val) {
      console.log(val);
    },
    handleCheckClick(val) {
      console.log(val);
    },
    handleDeleteClick(val) {
      console.log(val);
    },
  },
};
</script>

<style scoped>
.province-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .province-list-child .pagination-2 {
    display: block;
  }
  .province-list-child .pagination-1 {
    display: none;
  }
}
</style>
