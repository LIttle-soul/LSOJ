<template>
  <div class="code-header">
    <el-select v-model="temp_language" size="mini" @change="changeLanguage">
      <el-option
        v-for="item in language"
        :key="item.value"
        :label="item.text"
        :value="item"
      ></el-option>
    </el-select>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue";
import { useStore, mapState } from "vuex";

let store = useStore();

let emit = defineEmits(["changeLanguage"]);

let language = computed(
  mapState("code", ["language_data"]).language_data.bind({
    $store: store,
  })
);

let temp_language = ref({
  value: 0,
  text: "C",
  code: "c",
});

let changeLanguage = (val: any) => {
  emit("changeLanguage", val);
};
</script>

<style scoped lang="scss">
.code-header {
  width: 100%;
  height: 100%;
  position: relative;
  .el-select {
    float: left;
    max-width: 120px;
    height: 25px;
    position: absolute;
    left: 10px;
    top: 8px;
  }
}
</style>
