<template>
  <div>
    <el-table :data="props.Data" style="width: 100%">
      <el-table-column label="敏感词" prop="word" />
      <el-table-column label="操作" width="100px">
        <template #default="scope">
          <div>
            <el-button
              type="danger"
              size="mini"
              circle
              @click="deleteTheWord(scope.row.word)"
              ><el-icon><Delete /></el-icon
            ></el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import { Delete } from "@element-plus/icons";
import { deleteWord } from "@/api/forum";
import { ElMessage } from "element-plus";

let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
});
let emits = defineEmits(["deleteWord"]);
let deleteTheWord = async (val: string) => {
  let data = {
    text: val,
  };
  let word = await deleteWord(data);
  if (word.status) {
    ElMessage({
      message: word.message,
      type: "success",
    });
    emits("deleteWord");
  } else {
    ElMessage.error(word.message);
  }
};
</script>

<style scoped lang="scss"></style>
