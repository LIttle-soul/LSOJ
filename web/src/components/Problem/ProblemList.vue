<template>
  <div class="problem-list-child">
    <el-table
      :data="Data"
      size="mini"
      @cell-click="show_problem"
      @filter-change="handleFilterChange"
      :row-class-name="tableRowClassName"
      :default-sort="{ prop: 'problem_id', order: 'aescending' }"
    >
      <el-table-column v-if="contest" prop="problem_num" label="编号"> </el-table-column>
      <el-table-column v-else prop="problem_id" label="编号"> </el-table-column>
      <el-table-column prop="problem_title" label="题目"> </el-table-column>
      <el-table-column
        prop="problem_tag"
        label="类型"
        v-if="!props.admin && !props.contest"
      >
        <template #default="scope">
          <el-tag
            v-for="item in scope.row.problem_tag"
            :key="item"
            size="mini"
            :color="color16()"
            >{{ item }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column
        prop="problem_degree"
        width="150"
        label="难度"
        filter-placement="bottom-end"
        :filters="filter_degree_data"
        :filter-multiple="false"
        :column-key="'sStatus'"
        v-if="!props.contest"
      >
        <template #default="scope">
          <!-- {{ scope.row.problem_degree }} -->
          <el-rate
            v-model="scope.row.problem_degree"
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            :disabled="!props.admin"
          ></el-rate>
        </template>
      </el-table-column>
      <el-table-column prop="problem_solved" sortable width="70" label="正确">
      </el-table-column>
      <el-table-column prop="problem_submit" sortable width="70" label="提交">
      </el-table-column>
      <el-table-column prop="problem_source" label="题目来源" v-if="!props.contest">
      </el-table-column>
      <el-table-column prop="creation_time" label="创建时间" v-if="props.admin">
      </el-table-column>
      <el-table-column
        prop="problem_status"
        fixed="right"
        width="50px"
        label="状态"
        v-if="props.admin"
      >
        <template #default="scope">
          <el-switch
            v-model="scope.row.problem_status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="165px" label="操作" v-if="props.admin">
        <template #default="scope">
          <div class="button-box">
            <el-button
              size="mini"
              type="primary"
              circle
              @click="handleEditClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-pencil-square"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="success"
              circle
              @click="handleCheckClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-check-lg"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="warning"
              circle
              @click="handleDataClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-archive"></i></el-icon>
            </el-button>
            <el-dialog
              title="测试数据"
              v-model="scope.row.centerDialogVisible"
              width="90%"
              :destroy-on-close="true"
            >
              <ProblemDataList :problem_id="scope.row.problem_id" />
            </el-dialog>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[30, 50, 100, 200]"
      :page-size="page.page_size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[30, 50, 100, 200]"
      :page-size="page.page_size"
      layout="prev, pager, next"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script lang="ts" setup>
import ProblemDataList from "@/components/Problem/ProblemDataList.vue";
import { changeProblemData, deleteProblemData } from "@/api/problem";
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

let router = useRouter();
let store = useStore();

let props = defineProps({
  admin: {
    type: Boolean,
    default: false,
  },
  contest: {
    type: Boolean,
    default: false,
  },
  contest_id: {
    type: Number,
    default: -1,
  },
  Data: {
    type: undefined,
    default: [],
  },
  page: {
    type: undefined,
    default: {
      page: 1,
      total: 0,
      page_size: 30,
    },
  },
});

let emits = defineEmits([
  "onLoading",
  "filterProblemByDegree",
  "handleSizeChange",
  "handleCurrentChange",
  "reloadData",
]);

onMounted(() => {
  emits("onLoading");
});

let handleFilterChange = (val: any) => {
  emits("filterProblemByDegree", val);
};
let handleSizeChange = (val: number) => {
  emits("handleSizeChange", val);
};
let handleCurrentChange = (val: number) => {
  emits("handleCurrentChange", val);
};

let filter_degree_data = ref([
  { text: "零星", value: 0 },
  { text: "一星", value: 1 },
  { text: "二星", value: 2 },
  { text: "三星", value: 3 },
  { text: "四星", value: 4 },
  { text: "五星", value: 5 },
]);

let tableRowClassName = ({ row }: any) => {
  if (props.admin) {
    return "";
  }
  if (+row.submit_status === 1) {
    return "success-row";
  } else if (+row.submit_status === -1) {
    return "warning-row";
  } else {
    return "";
  }
};
let filterProblemBYDegree = (value: any) => {
  emits("filterProblemByDegree", value.sStatus);
};
let show_problem = (row: any) => {
  if (!props.admin) {
    router.push({
      path: "/showproblem",
      query: {
        problem_id: row.problem_id,
        contest_id: props.contest_id,
        problem_title: escape(row.problem_title),
        problem_description: escape(row.problem_description),
        time_limit: row.time_limit,
        memory_limit: row.memory_limit,
      },
    });
  }
};
let handleEditClick = (row: any) => {
  router.push("/admin/addproblem/" + row.problem_id);
};
let handleCheckClick = async (row: any) => {
  let back_data = await changeProblemData({
    problem_id: row.problem_id,
    problem_title: "",
    problem_description: "",
    problem_spj: "",
    problem_course: "",
    time_limit: "",
    memory_limit: "",
    problem_tag: "",
    problem_difficult: row.problem_degree,
    problem_status: row.problem_status,
  });
  if (back_data.status) {
    emits("reloadData");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleDeleteClick = async (row: any) => {
  let back_data = await deleteProblemData({
    problem_id: row.problem_id,
  });
  if (back_data.status) {
    emits("reloadData");
    ElMessage({
      type: "success",
      message: back_data.message,
    });
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let handleDataClick = (val: any) => {
  val.centerDialogVisible = true;
};
let color16 = () => {
  var r = Math.floor(Math.random() * 256);
  var g = Math.floor(Math.random() * 256);
  var b = Math.floor(Math.random() * 256);
  var a = Math.floor(Math.random() * 50);
  var color = "#" + r.toString(16) + g.toString(16) + b.toString(16) + a.toString(16);
  return color;
};
</script>

<style lang="scss">
.button-box {
  display: flex;
  justify-content: space-around;
}
.problem-list-child .warning-row {
  background: rgba(245, 127, 127, 0.5);
}
.problem-list-child .success-row {
  background: rgb(40, 211, 154, 0.5);
}
</style>

<style scoped lang="scss">
.problem-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .oblem-list-child .pagination-2 {
    display: block;
  }
  .problem-list-child .pagination-1 {
    display: none;
  }
}
</style>
