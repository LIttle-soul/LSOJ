<template>
  <div class="user-list">
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
              @click="search_all_data(search_data)"
            ></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <UserList :Data="Data" />
      </div>
    </el-card>
  </div>
</template>

<script>
import UserList from "@/components/User/UserList.vue";
import { mapState } from "vuex";

export default {
  components: {
    UserList: UserList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("user", {
      temp_data: (state) => state.user_list,
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
          user_id: "201910101600040",
          user_nick: "nick_1",
          user_name: "name_1",
          user_school: "金华职业技术学院",
          user_power: 0,
          user_status: true,
          registration_time: "2020-02-03 12:00:00",
          centerDialogVisible: false,
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
        user_id: item.user_id,
        user_nick: item.user_nick,
        user_name: item.user_name,
        user_school: item.school.school_name,
        user_power: item.user_power,
        user_status: item.user_status,
        registration_time: this.$dayJS(item.user_registration_time).format(
          "YYYY-MM-DD HH:mm:ss"
        ),
        centerDialogVisible: false,
      }));
    },
  },
};
</script>

<style lang="css">
.user-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.user-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 600px) {
  .user-list .input-with-select {
    display: none;
  }
}
</style>

<style scoped>
.user-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .user-list {
    width: 100%;
  }
}
</style>
