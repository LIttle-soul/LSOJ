<template>
  <div class="team-list">
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
        <TeamList :Data="Data" :is_delete_power="true" />
      </div>
    </el-card>
  </div>
</template>

<script>
import TeamList from "@/components/User/TeamList.vue";
import { mapState } from "vuex";

export default {
  components: {
    TeamList: TeamList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("user", {
      temp_data: (state) => state.team_list,
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data();
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
          team_id: 1,
          team_nick: "nick_1",
          team_creator: "201910101600040",
          team_user_list: [
            {
              add_time: "2021-08-16T13:47:57Z",
              user_id: "201910101600063",
              user_nick: "sdsa",
              user_status: true,
              user_type: 0,
            },
            {
              add_time: "1900-01-20T08:05:43Z",
              user_id: "201910101600068",
              user_nick: "201910101600068",
              user_status: true,
              user_type: 1,
            },
          ],
          team_school: "金华职业技术学院",
          team_type: "临时团队",
          team_status: true,
          registration_time: "2020-02-03 12:00:00",
          team_introduce: "Hello Team",
        },
      ],
    };
  },
  methods: {
    search_all_data() {
      console.log(this.search_data);
    },
    formatData(val) {
      return val.map((item) => ({
        team_id: item.class_id,
        team_nick: item.class_name,
        team_creator: item.class_creator,
        team_user_list: item.user_list,
        team_school: item.class_college,
        team_type: item.class_type,
        registration_time: this.$dayJS(item.create_time).format(
          "YYYY-MM-DD HH:mm:ss"
        ),
        team_introduce: item.class_introduce,
      }));
    },
  },
};
</script>

<style>
.team-list .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.team-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
.team-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.team-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 1000px) {
  .solution-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .team-list-child .input-with-select {
    display: none;
  }
}
</style>
