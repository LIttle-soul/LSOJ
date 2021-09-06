<template>
  <div class="team-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          团队管理
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
              (current_page - 1) * page_sizes,
              current_page * page_sizes
            )
          "
          size="mini"
          :stripe="true"
          :fit="true"
          style="width: 100%;"
        >
          <el-table-column prop="team_id" label="团队编号"> </el-table-column>
          <el-table-column prop="team_nick" label="团队名称"> </el-table-column>
          <el-table-column prop="team_user_1" label="团队成员1"></el-table-column>
          <el-table-column prop="team_user_2" label="团队成员2"></el-table-column>
          <el-table-column prop="team_user_3" label="团队成员3"></el-table-column>
          <el-table-column prop="team_school" label="所在学校"></el-table-column>
          <el-table-column prop="registration_time" label="注册时间"></el-table-column>
          <el-table-column prop="team_type" label="团队类型"></el-table-column>
          <el-table-column
            prop="team_status"
            fixed="right"
            width="50px"
            label="状态"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.team_status"
                active-color="#13ce66"
                inactive-color="#ff4949"
              ></el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="87px" label="操作">
            <template #default="scope">
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
      </div>
      <el-pagination
        class="pagination-1"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="current_page"
        :page-sizes="[20, 50, 100, 200]"
        :page-size="page_sizes"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
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
        :total="total"
        :hide-on-single-page="true"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "UserListChild",
  mounted() {},
  computed: {
    listenSoreMsg() {
      return this.$store.state.search_data;
    },
  },
  watch: {
    listenSoreMsg() {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
  },
  data() {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      Data: [
        {
          team_id: 1,
          team_nick: "nick_1",
          team_user_1: "user_1",
          team_user_2: "user_2",
          team_user_3: "user_3",
          team_school: "金华职业技术学院",
          team_type: "临时团队",
          team_status: true,
          registration_time: "2020-02-03 12:00:00"
        },
      ],
      total: 0,
      listQuery: {
        page: 1,
        limit: 10,
      },
    };
  },
  methods: {
    handleCheckClick(val) {
      console.log(val);
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
      console.log(this.search_data);
    },
  },
};
</script>

<style>
.team-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.team-list-child .el-card__header {
  height: 60px;
}
.team-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.team-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.team-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .team-list-child .input-with-select {
    display: none;
  }
  .team-list-child .pagination-2 {
    display: block;
  }
  .team-list-child .pagination-1 {
    display: none;
  }
}
</style>
