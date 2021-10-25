<template>
  <div class="college-list">
    <div class="echart">
      <!-- 此处用于添加图表信息 -->
    </div>
    <div class="list">
      <el-card>
        <template #header>
          <div class="table-header">
            <i class="el-icon-notebook-2"></i>
            学院管理
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
      </el-card>
      <div>
        <collegeList />
      </div>
    </div>
  </div>
</template>

<script>
import CollegeList from "@/components/School/CollegeList.vue";

export default {
  components: {
    CollegeList: CollegeList,
  },
  data() {
    return {
      search_data: "",
      Data: [
        {
          college_id: "4265051060",
          college_name: "新疆工业职业技术学院",
          college_school: "金华职业技术学院",
        },
        {
          college_id: "4262051378",
          college_name: "甘肃财贸职业学院",
          college_school: "金华职业技术学院",
        },
      ],
    };
  },
};
</script>

<style scoped>
.college-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
@media screen and (max-width: 1000px) {
  .college-list {
    width: 100%;
  }
}
</style>
