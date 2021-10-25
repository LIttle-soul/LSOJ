<template>
  <div class="news-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          新闻列表
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
              @click="search_all_data(search_data)"
            ></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <NewsList :Data="Data" :admin="true" />
      </div>
    </el-card>
  </div>
</template>

<script>
import NewsList from "@/components/News/NewsList.vue";
import { mapState } from "vuex";

export default {
  components: {
    NewsList: NewsList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("news", {
      temp_data: (state) => state.news_list,
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data(this.search_data);
    },
    temp_data() {
      this.Data = this.formatData(this.temp_data);
    },
  },
  created() {
    this.Data = this.formatData(this.temp_data);
  },
  data() {
    return {
      search_data: "",
      Data: [
        {
          news_id: 1,
          news_title: "新闻一",
          news_time: "2020-02-03 12:00:00",
          news_creator: "Admin",
          news_importance: 0,
        },
        {
          news_id: 2,
          news_title: "新闻二",
          news_time: "2020-02-03 12:00:00",
          news_creator: "Admin",
          news_importance: 0,
        },
        {
          news_id: 3,
          news_title: "新闻三",
          news_time: "2020-02-03 12:00:00",
          news_creator: "Admin",
          news_importance: 1,
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      console.log(val);
    },
    formatData(val) {
      return val.map((item) => ({
        news_id: item.news_id,
        news_title: item.news_title,
        news_time: this.$dayJS(item.create_time).format("YYYY-MM-DD HH:mm:ss"),
        news_creator: item.news_creator,
        news_importance: item.news_importance,
      }));
    },
  },
};
</script>

<style lang="css">
.news-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.news-list .el-card__header {
  height: 60px;
}
.news-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
</style>

<style scoped>
.news-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .news-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .news-list-child .input-with-select {
    display: none;
  }
}
</style>
