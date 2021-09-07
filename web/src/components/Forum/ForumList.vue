<template>
  <div class="forum-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          论坛列表
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
          :default-sort="{ prop: 'forum_id', order: 'descending' }"
        >
          <el-table-column prop="forum_id" label="论坛编号"> </el-table-column>
          <el-table-column prop="forum_title" label="论坛标题">
          </el-table-column>
          <el-table-column prop="forum_time" label="创建时间"> </el-table-column>
          <el-table-column prop="forum_creator" label="创建者">
          </el-table-column>
          <el-table-column
            prop="forum_status"
            fixed="right"
            width="50px"
            label="状态"
            v-if="admin"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.forum_status"
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
                circle
                icon="el-icon-view"
                @click="handleShowClick(scope.row)"
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
  name: "ForumList",
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
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      Data: [
        {
          forum_id: 1,
          forum_title: "新闻一",
          forum_time: "2020-02-03 12:00:00",
          forum_creator: "Admin",
          forum_status: true,
        },
        {
          forum_id: 2,
          forum_title: "新闻二",
          forum_time: "2020-02-03 12:00:00",
          forum_creator: "Admin",
          forum_status: false,
        },
        {
          forum_id: 3,
          forum_title: "新闻三",
          forum_time: "2020-02-03 12:00:00",
          forum_creator: "Admin",
          forum_status: true,
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
    handleShowClick(val) {
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

<style>
.forum-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.forum-list-child .el-card__header {
  height: 60px;
}
.forum-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.forum-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.forum-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .forum-list-child .input-with-select {
    display: none;
  }
  .forum-list-child .pagination-2 {
    display: block;
  }
  .forum-list-child .pagination-1 {
    display: none;
  }
}
</style>
