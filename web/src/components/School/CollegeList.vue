<template>
  <div class="college-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column prop="college_id" label="学院编号"> </el-table-column>
      <el-table-column prop="college_name" label="学院名称"> </el-table-column>
      <el-table-column prop="college_school" label="学院所在学校">
      </el-table-column>
      <el-table-column fixed="right" width="125px" label="操作">
        <template #default="scope">
          <el-button
            size="mini"
            type="primary"
            circle
            icon="el-icon-edit"
            @click="handleEditClick()"
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
  name: "collegeListChild",
  data() {
    return {
      current_page: 1,
      page_sizes: 50,
      edit: true,
    };
  },
  methods: {
    handleEditClick() {
      this.$router.push({
        name: "AdminAddCollege",
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
    search_all_data() {
      this.Data = this.$store.getters
        .filtercollegeData(this.search_data)
        .map((item) => ({
          college_id: item.college_id,
          user_nick: item.user_nick,
          user_name: item.user_name,
          user_college: item.user_college
            ? item.user_college.college_name
            : null,
          college_municipality: item.college_municipality,
          user_status: true,
          registration_time: this.$dayJS(item.registration_time).format(
            "YYYY-MM-DD HH:mm:ss"
          ),
          centerDialogVisible: false,
        }));
    },
  },
};
</script>

<style scope>
.college-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.college-list-child .el-card__header {
  height: 60px;
}
.college-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.college-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.college-list-child .pagination-2 {
  display: none;
}
.edit {
  margin-bottom: 2%;
}
@media screen and (max-width: 600px) {
  .college-list-child .input-with-select {
    display: none;
  }
  .college-list-child .pagination-2 {
    display: block;
  }
  .college-list-child .pagination-1 {
    display: none;
  }
}
</style>
