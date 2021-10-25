<template>
  <div class="address-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          地址列表
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
        <AddressList :admin="true" :Data="Data" />
      </div>
    </el-card>
  </div>
</template>

<script>
import AddressList from "@/components/Address/AddressList.vue";
import { mapState, mapGetters } from "vuex";

export default {
  components: {
    AddressList: AddressList,
  },
  computed: {
    ...mapState({
      temp_search_data: (state) => state.search_data,
    }),
    ...mapState("address", {
      temp_data: (state) => state.address_list,
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
      Data: [],
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
.address-list .el-card__header {
  height: 60px;
}
</style>

<style scoped>
.address-list {
  width: 95%;
  max-width: 1200px;
  margin: 70px auto;
}
.address-list .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}

.address-list .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
@media screen and (max-width: 1000px) {
  .address-list {
    width: 100%;
  }
}
@media screen and (max-width: 600px) {
  .address-list .input-with-select {
    display: none;
  }
}
</style>
