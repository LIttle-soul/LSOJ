<template>
  <div class="discussion-section">
    <el-row :gutter="10">
      <el-col :span="6" :key="section" v-for="section in sections">
        <div class="grid-content bg-purple" v-on:click="changeSection(section)">
          {{ section.forum_section_title }}
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  props: {
    /**
     * sections: (sectionKeys <-) 主数据中的板块数组
     */
    sections: Array,
  },
  methods: {
    /**
     * changeSection: (sectionValue <-) 改变当前板块
     */
    changeSection(section) {
      this.$emit("changeSection", section);
    },
  },
};
</script>

<style>
.discussion-section .bg-purple {
  background: #f1f8ff;
  border: 1px solid beige;
}
.discussion-section .bg-purple:hover {
  background: #c9e0fa;
}
.discussion-section .grid-content {
  margin: 10px 0;

  border-radius: 4px;
}
</style>
