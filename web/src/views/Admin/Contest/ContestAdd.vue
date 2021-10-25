<template>
  <div class="contest-add">
    <el-card class="card">
      <el-form label-position="left" label-width="80px" :model="contest_form">
        <el-form-item label="竞赛编号">
          <el-input-number
            v-model="contest_form.contest_id"
            disabled
            controls-position="right"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="竞赛标题">
          <el-input v-model="contest_form.contest_title"></el-input>
        </el-form-item>
        <el-form-item label="竞赛类型">
          <el-select v-model="contest_form.contest_type" placeholder="请选择">
            <el-option
              v-for="item in type_options"
              :key="item.value"
              :label="item.title"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="竞赛密码">
          <el-input v-model="contest_form.contest_password"></el-input>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker
            v-model="contest_form.start_time"
            type="datetime"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择日期时间"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="contest_form.end_time"
            type="datetime"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择日期时间"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="竞赛状态">
          <el-switch
            v-model="contest_form.contest_status"
            active-color="#13ce66"
            inactive-color="#00000033"
          ></el-switch>
        </el-form-item>
        <el-form-item label="竞赛语言">
          <el-select
            v-model="contest_form.contest_language"
            multiple
            filterable
            placeholder="请选择"
          >
            <el-option
              v-for="item in language_list"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="竞赛问题">
          <el-select
            v-model="contest_form.contest_problem"
            multiple
            filterable
            placeholder="请选择"
          >
            <el-option
              v-for="item in problem_list"
              :key="item.problem_id"
              :label="item.problem_id"
              :value="item.problem_id"
            >
              <span style="float: left">{{ item.problem_id }}</span>
              <span
                style="
          float: right;
          color: var(--el-text-color-secondary);
          font-size: 13px;
        "
                >{{ item.problem_title }}</span
              >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-button
        type="primary"
        style="float: right; margin-bottom: 15px;"
        @click="submit"
        >提交</el-button
      >
    </el-card>
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <span class="title">竞赛介绍</span>
          <el-button class="button" type="text" @click="change = !change"
            >修改内容</el-button
          >
        </div>
      </template>
      <ContestChild
        mode="preview"
        :content="contest_form.contest_content"
        :key="new Date().getTime()"
      />
    </el-card>
    <el-dialog title="内容编辑" v-model="change" width="90%" top="60px" center>
      <ContestChild
        height="800px"
        :content="contest_form.contest_content"
        @getContent="getContent"
      />
    </el-dialog>
  </div>
</template>

<script lang="js">
import ContestChild from "@/components/Editor/MarkdownEditor.vue";
import { submitContestData, changeContestData } from "@/api/contest";
import { mapState, mapGetters } from 'vuex';

export default {
  components: {
    ContestChild
  },
  computed: {
    ...mapState('code', {
      language_list: state => state.filter_language_data
    }),
    ...mapState('problem', {
      problem_list: state => state.problem_list
    }),
    ...mapGetters('contest', {
      getContestData: "getContestData"
    })
  },
  created() {
    this.setData(this.$route.params.contest_id);
  },
  data() {
    return {
      change: false,
      type_options: [
          {value: 0, title: '公开'},
          {value: 1, title: '私有'},
          {value: 2, title: '作业'},
      ],
      contest_form: {
        contest_id: 0,
        contest_title: "",
        contest_content: require("@/assets/markdown/新闻模板.md"),
        contest_type: 0,
        contest_password: '',
        start_time: '2020-01-01 08:00:00',
        end_time: '2020-01-01 16:00:00',
        contest_status: false,
        contest_language: [],
        contest_problem: []
      },
    };
  },
  methods: {
      getContent(text){
        this.contest_form.contest_content = text;
      },
      async submit(){
        let back_data = this.$route.params.contest_id == ""
          ? await submitContestData(this.contest_form)
          : await changeContestData(this.contest_form);
        if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch('contest/getContestList');
        } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });

        }
      },
      setData(data) {
      if (data != "") {
        let val = this.getContestData(data);
        console.log(val);
        this.contest_form = {
          contest_id: val.contest_id,
          contest_title: val.contest_title,
          contest_content: val.contest_introduce == null ? "" : val.contest_introduce,
          contest_type: val.contest_province,
          contest_password: val.contest_password,
          start_time: this.$dayJS(val.start_time).format("YYYY-MM-DD HH:mm:ss"),
          end_time: this.$dayJS(val.end_time).format("YYYY-MM-DD HH:mm:ss"),
          contest_status: val.contest_defunct,
          contest_language: val.contest_language,
          contest_problem: val.problem_list.map((item) => {
            return item.problem_id
          })
        };
      }
    },
  }
};
</script>

<style>
.contest-add {
  width: 90%;
  margin: 40px auto;
}
.contest-add .el-input {
  max-width: 500px;
}
.contest-add .el-card {
  margin: 20px 0;
}
.contest-span {
  font-size: 18px;
  font-weight: 800;
  margin-left: 20px;
}
.contest-add .el-card__header {
  height: 60px;
  padding: 0 40px;
}
.contest-add .card-header {
  justify-content: space-between;
  align-items: center;
}
.contest-add .title {
  float: left;
  /* background-color: rgba(15, 105, 214, 0.2); */
  width: 100px;
  height: 60px;
  line-height: 60px;
  font-size: 20px;
  font-weight: 800;
  font-family: "宋体";
}
.contest-add .button {
  float: right;
  width: 60px;
  height: 60px;
}
</style>
