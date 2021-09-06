<template>
  <div class="rank-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-guide"></i>
          排名列表
          <span class="sort-button">
            <el-button size="mini" @click="sort_by_year">按年排序</el-button>
            <el-button size="mini" @click="sort_by_month">按月排序</el-button>
            <el-button size="mini" @click="sort_by_week">按周排序</el-button>
            <el-button size="mini" @click="sort_by_day">按日排序</el-button>
          </span>
        </div>
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
          <el-table-column prop="user_rank" sortable label="名次">
          </el-table-column>
          <el-table-column prop="user_id" label="用户"> </el-table-column>
          <el-table-column prop="user_nick" label="昵称"> </el-table-column>
          <el-table-column prop="true_submit" sortable label="正确">
          </el-table-column>
          <el-table-column prop="all_submit" sortable label="提交">
          </el-table-column>
          <el-table-column prop="percentage" sortable label="比率">
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
  name: "UserRankList",
  mounted() {
    this.Data = this.sort_data(this.listenDataMsg);
  },
  computed: {
    listenSoreMsg() {
      return this.$store.state.search_data;
    },
    listenDataMsg() {
      return this.$store.state.user_data.map(item => ({
        user_id: item.user_id,
          user_nick: item.user_nick,
          true_submit: item.user_solution_data.user_solved.length,
          all_submit: item.user_solution_data.user_submit,
          percentage: item.user_solution_data.user_submit===0?'0.00%':(item.user_solution_data.user_solved.length*100/item.user_solution_data.user_submit).toFixed(2)+"%",
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
      this.Data = this.sort_data(this.listenDataMsg);
    }
  },
  data() {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      Data: [
        {
          user_rank: 1,
          user_id: "user_1",
          user_nick: "nick_1",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
        {
          user_rank: 2,
          user_id: "user_2",
          user_nick: "nick_2",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
        {
          user_rank: 3,
          user_id: "user_3",
          user_nick: "nick_3",
          true_submit: 0,
          all_submit: 0,
          percentage: "39.2%",
        },
      ],
      listQuery: {
        page: 1,
        limit: 10,
      },
    };
  },
  methods: {
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
    filterDegree(value, row) {
      return row.degree === value;
    },
    sort_data(val) {
      val.sort(function (x, y) {
        return y.true_submit - x.true_submit;
      });
      let rank = 0;
      val.forEach(element => {
        element['user_rank'] = ++rank;
        // console.log(element);
      });
      return val;
    },
    sort_by_year() {},
    sort_by_month() {},
    sort_by_week() {},
    sort_by_day() {},
    search_all_data() {
      this.Data = this.sort_data(this.$store.getters.filterUserDataByUserId(this.search_data).map(item => ({
        user_id: item.user_id,
          user_nick: item.user_nick,
          true_submit: item.user_solution_data.user_solved.length,
          all_submit: item.user_solution_data.user_submit,
          percentage: item.user_solution_data.user_submit===0?'0.00%':(item.user_solution_data.user_solved.length*100/item.user_solution_data.user_submit).toFixed(2)+"%",
      })));
    },
  },
};
</script>

<style scoped>
.table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
}
.sort-button {
  width: 400px;
  float: right;
  transform: translateY(-1px);
}
.sort-button button {
  margin: 0 5px;
}
.pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .sort-button {
    display: none;
  }
  .pagination-2 {
    display: block;
  }
  .pagination-1 {
    display: none;
  }
}
</style>
