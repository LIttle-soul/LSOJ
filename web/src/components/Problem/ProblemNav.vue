<template>
  <div class="problem-nav">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ title }}</span>
        </div>
      </template>
      <el-tag
        v-for="(item, index) in card_data"
        :key="index"
        :color="color16()"
        @click="filterData(item)"
      >
        {{ item }}
      </el-tag>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: "卡片标题",
    },
    card_data: {
      type: undefined,
      default: [],
    },
  },
  methods: {
    filterData(val) {
      this.$emit("filterData", val);
    },
    color16() {
      var r = Math.floor(Math.random()*256);
			var g = Math.floor(Math.random()*256);
			var b = Math.floor(Math.random()*256);
      var a = Math.floor(Math.random()*100);
			var color = '#'+r.toString(16)+g.toString(16)+b.toString(16)+a.toString(16);
			return color;
    }
  },
};
</script>

<style>
.problem-nav .box-card {
  min-height: 250px;
  text-align: center;
}

.problem-nav .box-card .el-card__header {
  font-size: 16px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  padding: 0;
  font-family: "楷体";
}
.problem-nav .box-card .el-card__body {
  padding: 10px;
}
.problem-nav .text {
  margin: 4px;
  background-color: rgba(243, 225, 166, 0.6);
  text-align: center;
  white-space: nowrap;
  font-size: 12px;
  line-height: 16px;
}
</style>
