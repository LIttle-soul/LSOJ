<template>
  <div class="contest-user">
    <el-card>
      <template #header>
        <div class="header">
          <div class="table-header">
            <i class="el-icon-notebook-2"></i>
            竞赛用户
            <el-select
              size="mini"
              :filterable="true"
              v-model="cur_contest"
              placeholder="请选择你要管理的竞赛"
              class="contest-choice"
              @change="setContestUser(cur_contest)"
            >
              <el-option
                v-for="item in contest_list"
                :key="item.contest_id"
                :label="item.contest_title"
                :value="item.contest_id"
              ></el-option>
            </el-select>
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
        </div>
      </template>
      <div>
        <ContestUserList
          :Data="Data"
          :admin="true"
          :contest_id="cur_contest"
          @success="setContestUser(cur_contest)"
        />
        <div class="bottom-button">
          <el-select
            v-model="select_user"
            multiple
            filterable
            placeholder="请选择要添加的用户"
            size="mini"
          >
            <el-option
              v-for="item in user_list"
              :key="item.user_id"
              :label="item.user_id"
              :value="item.user_id"
            >
              <span style="float: left">{{ item.user_id }}</span>
              <span
                style="
          float: right;
          color: var(--el-text-color-secondary);
          font-size: 13px;
        "
                >{{ item.user_name }}</span
              >
            </el-option>
          </el-select>
          <el-button type="primary" size="mini" @click="addUser"
            >添加用户</el-button
          >
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { mapGetters, mapState } from "vuex";
import { getContestUser, addContestUser } from "@/api/contest";
import { ElLoading } from "element-plus";

export default {
  components: {
    ContestUserList: defineAsyncComponent(() =>
      import("@/components/Contest/ContestUser.vue")
    ),
  },
  computed: {
    ...mapState("contest", {
      temp_data: (state) => state.contest_list,
    }),
    ...mapState("user", {
      user_list: (state) => state.user_list,
    }),
    ...mapGetters("contest", {
      getContestList: "filterContestByTime",
    }),
  },
  watch: {
    temp_data() {
      this.contest_list = this.formatContestList(this.getContestList());
    },
  },
  created() {
    this.contest_list = this.formatContestList(this.getContestList());
  },
  data() {
    return {
      search_data: "",
      cur_contest: null,
      select_user: [],
      contest_list: [
        {
          contest_id: 0,
          contest_title: "竞赛一",
        },
        {
          contest_id: 1,
          contest_title: "竞赛二",
        },
        {
          contest_id: 2,
          contest_title: "竞赛三",
        },
      ],
      Data: [
        {
          user_id: "201910101600040",
          user_name: "任成辉",
          user_school: "金华职业技术学院",
          student_id: "201910101600040",
          apply_time: "2020-01-01 08:00:00",
          apply_status: false,
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      console.log(val);
    },
    async setContestUser(val) {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      let back_data = await getContestUser({
        contest_id: val,
      });
      if (back_data.status) {
        // console.log(back_data.message);
        this.Data = this.formatContestUser(back_data.message);
        loading.close();
      } else {
        this.Data = [];
        loading.close();
      }
    },
    async addUser() {
      let back_data = await addContestUser({
        contest_id: this.cur_contest,
        user_list: this.select_user,
      });
      if (back_data.status) {
        this.setContestUser(this.cur_contest);
        this.$message({
          type: "success",
          message: back_data.message,
        });
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    formatContestList(val) {
      return val.map((item) => ({
        contest_id: item.contest_id,
        contest_title: item.contest_title,
      }));
    },
    formatContestUser(val) {
      return val.map((item) => ({
        user_id: item.contest_user,
        user_name: item.user_name,
        user_school: item.user_school,
        student_id: item.student_id,
        apply_time: this.$dayJS(item.apply_time).format("YYYY-MM-DD HH:mm:ss"),
        apply_status: item.contest_auditing,
      }));
    },
  },
};
</script>

<style lang="css">
.contest-user .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.contest-user {
  width: 90%;
  max-width: 1200px;
  margin: 70px auto;
}
.contest-user .header {
  display: flex;
  justify-content: space-between;
}
.contest-user .contest-choice {
  width: 180px;
  margin-left: 20px;
}
.contest-user .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 28px;
  min-width: 210px;
  display: flex;
}
.contest-user .input-with-select {
  width: 205px;
  margin-right: 10px;
}

.contest-user .bottom-button {
  margin: 20px 40px;
  float: right;
}

@media screen and (max-width: 1000px) {
  .contest-user {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .contest-user .input-with-select {
    display: none;
  }
}
</style>
