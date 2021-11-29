<template>
  <div class="team-list-child">
    <el-table :data="Data" size="mini" :stripe="true" :fit="true" style="width: 100%">
      <el-table-column type="expand" width="20px">
        <template #default="props">
          <div class="team-list-introduce">
            <p>团队编号: {{ props.row.team_id }}</p>
            <p>团队名称: {{ props.row.team_nick }}</p>
            <p>团队介绍: {{ props.row.team_introduce }}</p>
            <p>团队创建者: {{ props.row.team_creator }}</p>
            <p>所在学校: {{ props.row.team_school }}</p>
            <p>注册时间: {{ props.row.registration_time }}</p>
            <p>指导老师: {{ props.row.team_teacher }}</p>
            <div>
              <p v-for="(item, index) in props.row.team_user_list" :key="item">
                <span
                  >团队成员{{ index + 1 }}: {{ item.user_nick }} ({{ item.user_id }})
                  <el-button
                    v-show="is_delete_power"
                    @click="deleteUser(props.row.team_id, item.user_id)"
                    class="delete-user-button"
                    size="mini"
                    >删除用户</el-button
                  ></span
                >
              </p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="team_id" label="团队编号"> </el-table-column>
      <el-table-column prop="team_nick" label="团队名称"> </el-table-column>
      <el-table-column prop="team_creator" label="团队创建者"></el-table-column>
      <el-table-column prop="team_user_list.length" label="团队人数"></el-table-column>
      <el-table-column prop="team_school" label="所在学校"></el-table-column>
      <el-table-column prop="registration_time" label="注册时间"></el-table-column>
      <el-table-column prop="invitation_code" label="邀请码"> </el-table-column>
      <el-table-column fixed="right" width="80px" label="操作">
        <template #default="scope">
          <div class="button-box">
            <el-button
              v-if="is_delete_power"
              size="mini"
              type="success"
              circle
              @click="handleShareClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-share"></i></el-icon>
            </el-button>
            <el-button
              size="mini"
              type="danger"
              circle
              @click="handleDeleteClick(scope.row)"
            >
              <el-icon :size="16"><i class="bi bi-trash"></i></el-icon>
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page.page"
      :page-sizes="[20, 50, 100, 200]"
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
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page.page_size"
      layout="prev, pager, next"
      :total="page.total"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { deleteTeamData, deleteTeamUser } from "@/api/user";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { getInvitationCode } from "@/api/user";
import dayJS from "dayjs";

let store = useStore();
let router = useRouter();

let props = defineProps({
  Data: {
    type: undefined,
    default: [],
  },
  is_delete_power: {
    type: Boolean,
    default: false,
  },
  page: {
    type: undefined,
    default: {
      page: 1,
      page_size: 50,
      total: 0,
    },
  },
});

// 向父组件传送事件
let emit = defineEmits(["handleSizeChange", "handlePageChange", "reload"]);

// 页面跳转
let handleSizeChange = (val: number) => {
  emit("handleSizeChange", val);
};

let handleCurrentChange = (val: number) => {
  emit("handlePageChange", val);
};

// 事件操作函数
let handleShareClick = async (row: any) => {
  let back_data = await getInvitationCode({
    team_id: row.team_id,
  });
  if (back_data.status) {
    ElMessageBox.alert(
      `<p style="color: #DD0000;"><span style="display: inline-block;width: 70px;color: #000000;">邀请码:</span>${
        back_data.message.code
      }</p>
      <p style="color: #DD0000;"><span style="display: inline-block;width: 70px;color: #000000;">到期时间:</span>${dayJS(
        back_data.message.time
      ).format("YYYY-MM-DD HH:mm:ss")}</p>`,
      "邀请码",
      {
        dangerouslyUseHTMLString: true,
      }
    )
      .then()
      .catch(() => {
        console.log("close");
      });
    emit("reload");
  }
};

let handleDeleteClick = async (row: any) => {
  let back_data = props.is_delete_power
    ? await deleteTeamData({
        team_id: row.team_id,
      })
    : await deleteTeamUser({
        team_id: row.team_id,
        user_id: "",
      });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    emit("reload");
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
let deleteUser = async (team_id: any, user_id: any) => {
  let back_data = await deleteTeamUser({
    team_id: team_id,
    user_id: user_id,
  });
  if (back_data.status) {
    ElMessage({
      type: "success",
      message: back_data.message,
    });
    emit("reload");
  } else {
    ElMessage({
      type: "error",
      message: back_data.message,
    });
  }
};
</script>

<style scoped lang="scss">
.team-list-child {
  .button-box {
    display: flex;
    justify-content: space-around;
  }
  .team-list-introduce {
    line-height: 23px;
    font-size: 1.2em;
    font-family: "宋体";
    font-weight: bold;
    letter-spacing: 2px;
  }
  .delete-user-button {
    width: 80px;
    background-color: rgba(241, 103, 10, 0.521);
    border-radius: 20px;
    margin: 1px 0;
    padding: 0;
  }
  .pagination-2 {
    display: none;
  }

  @media screen and (max-width: 600px) {
    .pagination-2 {
      display: block;
    }
    .pagination-1 {
      display: none;
    }
  }
}
</style>
