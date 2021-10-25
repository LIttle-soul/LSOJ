<template>
  <div class="municipality-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          城市列表
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
        <MunicipalityList :admin="true" :Data="Data" />
      </div>
    </el-card>
  </div>
</template>

<script>
import MunicipalityList from "@/components/Address/MunicipalityList.vue";
import { mapGetters, mapState } from "vuex";

export default {
  components: {
    MunicipalityList: MunicipalityList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("address", {
      temp_data: (state) => state.municipality_list,
    }),
    ...mapGetters("address", {
      filterMunicipality: "filterMunicipalityData",
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
  data() {
    return {
      search_data: "",
      Data: [
        {
          municipality_id: 1111,
          municipality_name: "北京市",
          municipality_province: "北京市",
        },
      ],
    };
  },
  methods: {
    search_all_data() {
      this.Data = this.filterMunicipality(this.search_data);
    },
    formatData(val) {
      return val.map((item) => ({
        municipality_id: item.municipality_id,
        municipality_name: item.municipality_name,
        municipality_province: item.municipality_province.name,
      }));
    },
  },
};
</script>

<style>
.municipality-list .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.municipality-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
.municipality-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.municipality-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 1000px) {
  .municipality-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .municipality-list-child .input-with-select {
    display: none;
  }
}
</style>
