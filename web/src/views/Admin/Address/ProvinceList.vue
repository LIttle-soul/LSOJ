<template>
  <div class="province-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          省份列表
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
        <ProvinceList :admin="true" :Data="Data" />
      </div>
    </el-card>
  </div>
</template>

<script>
import ProvinceList from "@/components/Address/ProvinceList.vue";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    ProvinceList: ProvinceList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("address", {
      temp_data: (state) => state.province_list,
    }),
    ...mapGetters("address", {
      filterProvince: "filterProvinceData",
    }),
  },
  watch: {
    temp_search_data() {
      this.search_data = this.temp_search_data;
      this.search_all_data();
    },
    temp_data() {
      this.Data = this.temp_data;
    },
  },
  created() {
    this.Data = this.temp_data;
  },
  data() {
    return {
      search_data: "",
      Data: [
        {
          province_id: 11,
          province_name: "北京市",
        },
      ],
    };
  },
  methods: {
    search_all_data() {
      this.Data = this.filterProvince(this.search_data);
    },
  },
};
</script>

<style>
.province-list .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.province-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
.province-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.province-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 1000px) {
  .province-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .province-list .input-with-select {
    display: none;
  }
}
</style>
