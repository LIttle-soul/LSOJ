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
            placeholder="请输入你要添加的问题，以英文逗号分割"
            :multiple="true"
            :filterable="true"
            :remote="true"
            :loading="loading"
            :remote-method="filterProblem"
          >
            <el-option
              v-for="(item, index) in problem_list"
              :key="index"
              :label="item.problem_title"
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
      <el-button type="primary" style="float: right; margin-bottom: 15px" @click="submit"
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

<script lang="ts" setup>
import ContestChild from "@/components/Editor/MarkdownEditor.vue";
import { submitContestData, changeContestData, getContestList } from "@/api/contest";
import { useStore, mapState } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { ElMessage } from "element-plus";
import contest_mode from "@/assets/markdown/NewsTemplet.md?raw";
import dayJS from "dayjs";
import { getProblemDataList } from "@/api/problem";

let route = useRoute();
let router = useRouter();
let store = useStore();

let language_list = computed(
  mapState("code", ["language_data"]).language_data.bind({ $store: store })
);
let change = ref(false);
let type_options = [
  { value: 0, title: "公开" },
  { value: 1, title: "私有" },
  { value: 2, title: "作业" },
  { value: 3, title: "竞赛" },
];
let contest_form = ref({
  contest_id: 0,
  contest_title: "",
  contest_content: contest_mode,
  contest_type: 0,
  contest_password: "",
  start_time: "2020-01-01 08:00:00",
  end_time: "2020-01-01 16:00:00",
  contest_status: false,
  contest_language: [],
  contest_problem: [],
});
// 可搜索选择器
let problem_list = ref(<any>[]);
let loading = ref(false);
let filterProblem = async (val: string) => {
  if (val !== "") {
    loading.value = true;
    let back_data = await getProblemDataList({
      page: 1,
      total: 10,
      key: "search",
      text: val,
    });
    // console.log(back_data);
    if (back_data.status) {
      loading.value = false;
      problem_list.value = formatProblemData(back_data.message);
    } else {
      loading.value = false;
      problem_list.value = [];
    }
  } else {
    loading.value = false;
    problem_list.value = [];
  }
};
let formatProblemData = (val: any) => {
  return val.map((item: any) => ({
    problem_id: item.problem_id,
    problem_title: item.problem_title,
  }));
};
// 数据处理
let getContent = (text: string) => {
  contest_form.value.contest_content = text;
};
let submit = async () => {
  let back_data =
    route.params.contest_id == ""
      ? await submitContestData({
          contest_title: contest_form.value.contest_title,
          start_time: contest_form.value.start_time,
          end_time: contest_form.value.end_time,
          problem_id: contest_form.value.contest_problem,
          contest_language: contest_form.value.contest_language,
          contest_introduce: contest_form.value.contest_content,
          contest_province: contest_form.value.contest_type + "",
          contest_password: contest_form.value.contest_password,
          contest_status: contest_form.value.contest_status,
        })
      : await changeContestData({
          contest_id: contest_form.value.contest_id,
          contest_title: contest_form.value.contest_title,
          start_time: contest_form.value.start_time,
          end_time: contest_form.value.end_time,
          problem_id: contest_form.value.contest_problem,
          contest_language: contest_form.value.contest_language?.join(",") || "",
          contest_introduce: contest_form.value.contest_content,
          contest_province: contest_form.value.contest_type,
          contest_password: contest_form.value.contest_password,
          contest_status: contest_form.value.contest_status,
        });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    setTimeout(() => {
      router.push("/admin/contestlist");
    }, 2000);
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let formatData = (val: any) => {
  return {
    contest_id: val.contest_id,
    contest_title: val.contest_title,
    contest_content: val.contest_introduce || "",
    contest_type: val.contest_province,
    contest_password: val.contest_password,
    start_time: dayJS(val.start_time).format("YYYY-MM-DD HH:mm:ss"),
    end_time: dayJS(val.end_time).format("YYYY-MM-DD HH:mm:ss"),
    contest_status: val.contest_defunct,
    contest_language: val.contest_language,
    contest_problem: val.problem_list.map((item: any) => {
      return item.problem_id;
    }),
  };
};
let getContestData = async (val: number) => {
  let back_data = await getContestList({
    page: 1,
    total: 1,
    status: "",
    text: "",
    contest_id: val,
    me: "",
    time: "",
  });
  // console.log(back_data);
  if (back_data.status) {
    contest_form.value = formatData(back_data.message);
  }
};
onMounted(() => {
  // console.log(route.params);
  if (route.params.contest_id) {
    getContestData(Number(route.params.contest_id[0]));
  }
});
</script>

<style lang="scss" scoped>
.contest-add {
  width: 95%;
  margin: 40px auto;
  .card {
    margin: 30px 0;
    border-radius: 20px;
    .el-input {
      max-width: 400px;
    }
    .contest-span {
      font-size: 18px;
      font-weight: 800;
      margin-left: 20px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      .title {
        width: 100px;
        height: 20px;
        line-height: 20px;
        font-size: 20px;
        font-weight: 800;
        font-family: "宋体";
      }
      .button {
        width: 60px;
        height: 20px;
      }
    }
  }
}
</style>
