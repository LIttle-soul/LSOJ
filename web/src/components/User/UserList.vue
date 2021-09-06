<template>
  <div class="user-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          用户管理
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
          <el-table-column prop="user_id" label="用户账号"> </el-table-column>
          <el-table-column prop="user_nick" label="用户昵称"> </el-table-column>
          <el-table-column prop="user_name" label="用户姓名"> </el-table-column>
          <el-table-column prop="user_school" label="用户学校">
          </el-table-column>
          <el-table-column prop="registration_time" label="注册时间">
          </el-table-column>
          <el-table-column prop="user_power" label="用户身份">
            <template #default="scope">
              <el-select v-model="scope.row.user_power" placeholder="请选择">
                <el-option
                  v-for="item in power_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column
            prop="user_status"
            fixed="right"
            width="50px"
            label="状态"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.user_status"
                active-color="#13ce66"
                inactive-color="#ff4949"
              ></el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="125px" label="操作">
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
              <el-dialog
    title="重置密码"
    v-model="scope.row.centerDialogVisible"
    width="30%"
    center
    >
    <el-input v-model="resetting_password" placeholder="请在这里输入新密码"></el-input>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="scope.row.centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="scope.row.centerDialogVisible = false">确 定</el-button>
      </span>
    </template>
    </el-dialog>
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
  mounted() {this.Data = this.listenDataMsg},
  computed: {
    listenSoreMsg() {
      return this.$store.state.search_data;
    },
    listenDataMsg() {
      return this.$store.state.user_data.map(item => ({
        user_id: item.user_id,
          user_nick: item.user_nick,
          user_name: item.user_name,
          user_school: item.user_school?item.user_school.school_name:null,
          user_power: item.user_power,
          user_status: true,
          registration_time: this.$dayJS(item.registration_time).format('YYYY-MM-DD HH:mm:ss'),
          centerDialogVisible: false
      }));
    }
  },
  watch: {
    listenSoreMsg() {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
    listenDataMsg() {
      // console.log(this.listenDataMsg);
      this.Data = this.listenDataMsg;
    }
  },
  data() {
    return {
      resetting_password: '',
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      power_options: [
        {
          value: 0,
          label: '超级管理员'
        },
        {
          value: 1,
          label: '管理员'
        },
        {
          value: 2,
          label: '教师'
        },
        {
          value: 3,
          label: '志愿者'
        },
        {
          value: 4,
          label: '普通用户'
        }
      ],
      Data: [
        {
          user_id: "201910101600040",
          user_nick: "nick_1",
          user_name: "name_1",
          user_school: {user_school_name: "金华职业技术学院"},
          user_power: 0,
          user_status: true,
          registration_time: "2020-02-03 12:00:00",
          centerDialogVisible: false
        },
        {
          user_id: "201910101600041",
          user_nick: "nick_2",
          user_name: "name_2",
          user_school: {user_school_name: "金华职业技术学院"},
          user_power: 1,
          user_status: false,
          registration_time: "2020-02-03 12:00:00",
          centerDialogVisible: false
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
    handleEditClick(val) {
      console.log(val);
      val.centerDialogVisible = true;
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
      this.Data = this.$store.getters.filterUserData(this.search_data).map(item => ({
        user_id: item.user_id,
          user_nick: item.user_nick,
          user_name: item.user_name,
          user_school: item.user_school?item.user_school.school_name:null,
          user_power: item.user_power,
          user_status: true,
          registration_time: this.$dayJS(item.registration_time).format('YYYY-MM-DD HH:mm:ss'),
          centerDialogVisible: false
      }));
    },
  },
};
</script>

<style>
.user-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.user-list-child .el-card__header {
  height: 60px;
}
.user-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.user-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.user-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .user-list-child .input-with-select {
    display: none;
  }
  .user-list-child .pagination-2 {
    display: block;
  }
  .user-list-child .pagination-1 {
    display: none;
  }
}
</style>
