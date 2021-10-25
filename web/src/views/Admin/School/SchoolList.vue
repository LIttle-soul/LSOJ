<template>
  <div class="school-list">
    <div class="echart">
      <!-- 此处用于添加图表信息 -->
    </div>
    <div class="list">
      <el-card>
        <template #header>
          <div class="table-header">
            <i class="el-icon-notebook-2"></i>
            学校管理
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
          <SchoolList :Data="Data" />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import SchoolList from "@/components/School/SchoolList.vue";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("school", {
      temp_data: (state) => state.school_list,
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
  components: {
    SchoolList: SchoolList,
  },
  data() {
    return {
      search_data: "",
      Data: [
        {
          school_id: "4265051060",
          school_name: "新疆工业职业技术学院",
          school_describe: null,
          school_department: "",
          school_rank: "专科",
          school_remark: "",
          school_municipality: "新疆维吾尔自治区",
        },
        {
          school_id: "4262051378",
          school_name: "甘肃财贸职业学院",
          school_describe: null,
          school_department: "",
          school_rank: "专科",
          school_remark: "",
          school_municipality: "甘肃省",
        },
      ],
    };
  },
  methods: {
    search_all_data() {
      console.log("Hello");
    },
    formatData(val) {
      return val.map((item) => ({
        school_id: item.school_id,
        school_name: item.school_name,
        school_describe: item.school_describe,
        school_department: item.school_department,
        school_rank: item.school_rank,
        school_remark: item.school_remark,
        school_municipality: item.school_municipality.municipality_name,
      }));
    },
  },
};
</script>
<style>
.school-list .el-card__header {
  height: 60px;
}
</style>
<style scoped>
.school-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.school-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.school-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .school-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .school-list .input-with-select {
    display: none;
  }
}
</style>
