<template>
  <div class="contest-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-notebook-2"></i>
          竞赛列表<div class="current-time">当前时间:{{current_time}}</div>
        </div>
          <el-input
            placeholder="请输入内容"
            size="mini"
            v-model="search_data"
            class="input-with-select"
          >
            <template #append>
              <el-button icon="el-icon-search" @click="search_all_data"></el-button>
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
          @cell-click="show_contest"
          :default-sort="{ prop: 'contest_id', order: 'descending' }"
        >
          <el-table-column prop="contest_id" label="竞赛编号">
          </el-table-column>
          <el-table-column prop="contest_title" label="竞赛标题">
          </el-table-column>
          <el-table-column prop="contest_time" label="竞赛时间">
          </el-table-column>
          <el-table-column 
          prop="contest_type" 
          :filters="filter_status_data"
          label="状态">
          <template #default="scope">
              <el-tag>{{ status_data[scope.row.contest_type] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="contest_creator" label="创建者">
          </el-table-column>
          <el-table-column
            prop="contest_status"
            fixed="right"
            width="50px"
            label="状态"
            v-if="admin"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.contest_status"
                active-color="#13ce66"
                inactive-color="#ff4949"
              ></el-switch>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            width="125px"
            label="操作"
            v-if="admin"
          >
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
      </div>
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
    </el-card>
  </div>
</template>

<script>
export default {
  name: "UserContestList",
  mounted() {},
  // computed: {
  //   listenSoreMsg() {
  //     return this.$store.state.search_data;
  //   }
  // },
  // watch: {
  //   listenSoreMsg() {
  //     this.search_data = this.listenSoreMsg;
  //     this.search_all_data();
  //   },
  // },
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    this.current_time = setInterval(()=>{
        this.current_time = this.$dayJS().format('YYYY-MM-DD HH:mm:ss');
    }, 1000);
    return {
      search_data: "",
      current_time: this.$dayJS().format('YYYY-MM-DD HH:mm:ss'),
      current_page: 1,
      page_sizes: 50,
      filter_status_data: [
          {text: '公开', value: 0}, 
          {text: '私有', value: 1},
          {text: '作业', value: 2},
          {text: '竞赛', value: 3}
      ],
      status_data: [
          '公开',
          '私有',
          '作业',
          '竞赛'
      ],
      Data: [
        {
          contest_id: 1,
          contest_title: '竞赛一',
          contest_time: '@已结束 2020-02-03 12:00:00',
          contest_type: 2,
          contest_creator: 'Admin',
          contest_status: true
        },
        {
          contest_id: 2,
          contest_title: '竞赛二',
          contest_time: '@进行中 2021-02-03 12:00:00',
          contest_type: 1,
          contest_creator: 'Admin',
          contest_status: true
        },
        {
          contest_id: 3,
          contest_title: '竞赛三',
          contest_time: '@未开始 2022-02-03 12:00:00',
          contest_type: 0,
          contest_creator: 'Admin',
          contest_status: true
        },
      ],
    };
  },
  methods: {
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
    search_all_data() {
      console.log(this.search_data);
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
    show_contest(row) {
      console.log(row);
      if (!this.admin) {
        this.$router.push("/contestshow/");
      }
    },
  },
};
</script>

<style>
.contest-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.contest-list-child .el-card__header {
    height: 60px;
}
.contest-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.contest-list-child .current-time {
    font-size: 10px;
    color: darkturquoise;
    letter-spacing: 1px;
}
.contest-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .contest-list-child .input-with-select {
    display: none;
  }
  .contest-list-child .pagination-2 {
    display: block;
  }
  .contest-list-child .pagination-1 {
    display: none;
  }
}
</style>
