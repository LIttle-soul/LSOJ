<template>
  <div class="rank-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <div class="header-left">
            <el-icon :size="25" class="icon"><Guide /></el-icon>排名列表
          </div>
          <span class="sort-button">
            <el-button size="mini" @click="sort_by('year')">按年排序</el-button>
            <el-button size="mini" @click="sort_by('month')">按月排序</el-button>
            <el-button size="mini" @click="sort_by('week')">按周排序</el-button>
            <el-button size="mini" @click="sort_by('day')">按日排序</el-button>
          </span>
        </div>
      </template>
      <div>
        <RankList
          :Data="Data"
          :page="page_data"
          @handleSizeChange="pageSizeChange"
          @handleCurrentChange="pageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { watch, ref } from "vue";
import { computed, onMounted, reactive } from "@vue/runtime-core";
import { getRankList } from "@/api/rank";
import { useStore, mapGetters, mapState } from "vuex";
import RankList from "@/components/Rank/RankList.vue";
import { ElLoading, ElMessage } from "element-plus";
import { Guide } from "@element-plus/icons";

let store = useStore();

let temp_search_data = computed(
  mapState(["search_data"]).search_data.bind({ $store: store })
);

watch(
  () => temp_search_data.value,
  (value: string) => {
    // console.log(value);
    page_data.value.search_text = value;
    getRank();
  }
);
let Data = ref([]);
let page_data = ref({
  page: 1,
  page_size: 50,
  total: 0,
  search_text: "",
  sort_by: "",
});
let sort_by = (val: string) => {
  page_data.value.sort_by = val;
  getRank();
};

let pageSizeChange = (val: number) => {
  page_data.value.page_size = val;
  getRank();
};

let pageChange = (val: number) => {
  page_data.value.page = val;
  getRank();
};

let formatData = (val: any) => {
  return val.map((item: any, index: number) => ({
    user_rank: item.rank,
    user_id: item.user_id,
    user_nick: item.user_nick,
    true_submit: item.solved,
    all_submit: item.submit,
    percentage: ((item.solved / item.submit) * 100).toFixed(2).toString() + "%",
  }));
};
let getRank = async () => {
  let loading = ElLoading.service({
    lock: true,
    text: "加载中....",
    background: "rgba(0,0,0,0.7)",
  });
  let temp = await getRankList({
    page: page_data.value.page,
    total: page_data.value.page_size,
    sort_by: page_data.value.sort_by || "",
    text: page_data.value.search_text || "",
  });
  // console.log(temp);
  if (temp.status) {
    loading.close();
    Data.value = formatData(temp.message);
    page_data.value.total = temp.total;
  } else {
    loading.close();
    ElMessage({
      type: "error",
      message: "数据请求出错，请稍后请求",
    });
  }
};

onMounted(() => {
  getRank();
});
</script>

<style scoped lang="scss">
.rank-list {
  width: 80%;
  max-width: 1200px;
  margin: 70px auto;
  .table-header {
    display: flex;
    justify-content: space-between;
    .header-left {
      font: 1.2em "楷体";
      letter-spacing: 3px;
      .icon {
        transform: translateY(5px);
      }
    }
    .sort-button {
      width: 400px;
      transform: translateY(-1px);
      button {
        margin: 0 5px;
      }
    }
    @media screen and (max-width: 600px) {
      .sort-button {
        display: none;
      }
    }
  }
}
@media screen and (max-width: 1000px) {
  .rank-list {
    width: 100%;
  }
}
</style>
