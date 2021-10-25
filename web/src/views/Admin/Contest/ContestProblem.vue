<template>
  <div class="contest-problem">
    <el-card>
      <template #header>
        <div class="header">
          <div class="table-header">
            <i class="el-icon-notebook-2"></i>
            竞赛问题
            <el-select
              size="mini"
              :filterable="true"
              v-model="cur_contest"
              placeholder="请选择你要管理的竞赛"
              class="contest-choice"
              @change="setContestProblem(cur_contest)"
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
        <ContestProblemList
          :Data="Data"
          :admin="true"
          @handleContestProblemUpClick="upButtonClick"
          @handleContestProblemDownClick="downButtonClick"
          @handleContestProblemDeleteClick="deleteButtonClick"
        />
      </div>
      <div class="bottom-button">
        <el-button type="primary" size="mini" @click="addProblem"
          >添加问题</el-button
        >
        <el-button type="success" size="mini" @click="submitProblem"
          >提交</el-button
        >
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineAsyncComponent } from "@vue/runtime-core";
import { mapGetters, mapState } from "vuex";
import {
  getContestProblem,
  changeProblemList,
  deleteProblem,
  addProblem,
} from "@/api/contest";
import { ElLoading, ElMessageBox } from "element-plus";

export default {
  components: {
    ContestProblemList: defineAsyncComponent(() =>
      import("@/components/Contest/ContestProblem.vue")
    ),
  },
  computed: {
    ...mapState("contest", {
      temp_data: (state) => state.contest_list,
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
      problem_list: [],
      Data: [
        {
          problem_num: "A",
          problem_id: 1000,
          problem_title: "Hello, World",
          up_button: true,
          down_button: true,
        },
      ],
    };
  },
  methods: {
    search_all_data(val) {
      console.log(val);
    },
    addProblem() {
      ElMessageBox.prompt("请输入你要添加的问题编号", "添加问题", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
      }).then(async ({ value }) => {
        let back_data = await addProblem({
          contest_id: this.cur_contest,
          problem_id: value,
        });
        if (back_data.status) {
          this.setContestProblem(this.cur_contest);
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
      });
    },
    async submitProblem() {
      let back_data = await changeProblemList({
        contest_id: this.cur_contest,
        problem_list: this.problem_list.join(","),
      });
      if (back_data.status) {
        this.setContestProblem(this.cur_contest);
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
    upButtonClick({ index }) {
      if (index === 0) {
        this.$message({
          type: "error",
          message: "抱歉，这是第一个",
        });
      } else {
        [this.problem_list[index], this.problem_list[index - 1]] = [
          this.problem_list[index - 1],
          this.problem_list[index],
        ];
        [this.Data[index], this.Data[index - 1]] = [
          this.Data[index - 1],
          this.Data[index],
        ];
      }
    },
    downButtonClick({ index }) {
      if (index === this.Data.length - 1) {
        this.$message({
          type: "error",
          message: "抱歉，这是最后一个",
        });
      } else {
        [this.problem_list[index], this.problem_list[index + 1]] = [
          this.problem_list[index + 1],
          this.problem_list[index],
        ];
        [this.Data[index], this.Data[index + 1]] = [
          this.Data[index + 1],
          this.Data[index],
        ];
      }
    },
    async deleteButtonClick(row) {
      let back_data = await deleteProblem({
        contest_id: this.cur_contest,
        problem_id: row.problem_id,
      });
      if (back_data.status) {
        this.setContestProblem(this.cur_contest);
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
    async setContestProblem(val) {
      const loading = ElLoading.service({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      let back_data = await getContestProblem({
        contest_id: val,
      });
      if (back_data.status) {
        this.Data = this.formatContestProblem(back_data.message);
        this.problem_list = back_data.message.map((item) => {
          return item.problem_id;
        });
        loading.close();
      } else {
        this.Data = [];
        loading.close();
      }
    },
    formatContestList(val) {
      return val.map((item) => ({
        contest_id: item.contest_id,
        contest_title: item.contest_title,
      }));
    },
    formatContestProblem(val) {
      return val.map((item) => ({
        problem_num: item.problem_num,
        problem_id: item.problem_id,
        problem_title: item.problem_title,
      }));
    },
  },
};
</script>

<style lang="css">
.contest-problem .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.contest-problem {
  width: 90%;
  max-width: 1200px;
  margin: 70px auto;
}
.contest-problem .header {
  display: flex;
  justify-content: space-between;
}
.contest-problem .contest-choice {
  width: 180px;
  margin-left: 20px;
}
.contest-problem .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 28px;
  min-width: 210px;
  display: flex;
}
.contest-problem .input-with-select {
  width: 205px;
  margin-right: 10px;
}
.contest-problem .bottom-button {
  margin: 20px 40px;
  float: right;
}

@media screen and (max-width: 1000px) {
  .contest-problem {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .contest-problem .input-with-select {
    display: none;
  }
}
</style>
