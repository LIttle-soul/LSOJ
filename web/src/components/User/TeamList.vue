<template>
  <div class="team-list-child">
    <el-table
      :data="
        Data.slice((current_page - 1) * page_sizes, current_page * page_sizes)
      "
      size="mini"
      :stripe="true"
      :fit="true"
      style="width: 100%;"
    >
      <el-table-column type="expand">
        <template #default="props">
          <div class="team-list-introduce">
            <p>团队编号: {{ props.row.team_id }}</p>
            <p>团队名称: {{ props.row.team_nick }}</p>
            <p>团队介绍: {{ props.row.team_introduce }}</p>
            <p>团队创建者: {{ props.row.team_creator }}</p>
            <p>所在学校: {{ props.row.team_school }}</p>
            <p>注册时间: {{ props.row.registration_time }}</p>
            <div>
              <p v-for="(item, index) in props.row.team_user_list" :key="item">
                <span v-if="+item.user_type === 0"
                  >团队成员{{ index + 1 }}: {{ item.user_nick }} ({{
                    item.user_id
                  }})
                  <el-button
                    v-show="is_delete_power"
                    @click="deleteUser(props.row.team_id, item.user_id)"
                    class="delete-user-button"
                    size="mini"
                    >删除用户</el-button
                  ></span
                >
                <span v-else>指导老师: {{ item.user_nick }}</span>
              </p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="team_id" label="团队编号"> </el-table-column>
      <el-table-column prop="team_nick" label="团队名称"> </el-table-column>
      <el-table-column prop="team_creator" label="团队创建者"></el-table-column>
      <el-table-column
        prop="team_user_list.length"
        label="团队人数"
      ></el-table-column>
      <el-table-column prop="team_school" label="所在学校"></el-table-column>
      <el-table-column
        prop="registration_time"
        label="注册时间"
      ></el-table-column>
      <el-table-column prop="team_type" label="团队类型">
        <template #default="scope">
          {{ team_type_list[+scope.row.team_type] }}
        </template>
      </el-table-column>
      <el-table-column fixed="right" width="50px" label="操作">
        <template #default="scope">
          <el-button
            size="mini"
            type="danger"
            circle
            icon="el-icon-delete"
            @click="handleDeleteClick(scope.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination-1"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="total, sizes, prev, pager, next, jumper"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
    <el-pagination
      class="pagination-2"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="current_page"
      :page-sizes="[20, 50, 100, 200]"
      :page-size="page_sizes"
      layout="prev, pager, next"
      :total="Data.length"
      :hide-on-single-page="true"
    >
    </el-pagination>
  </div>
</template>

<script>
import { deleteTeamData, deleteTeamUser } from "@/api/user";

export default {
  name: "UserListChild",
  props: {
    Data: {
      type: undefined,
      default: [],
    },
    is_delete_power: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      team_type_list: [
        "行政班级",
        "注册团队",
        "课程班级",
        "默认班级",
        "临时团队",
      ],
      current_page: 1,
      page_sizes: 50,
    };
  },
  methods: {
    async handleDeleteClick(row) {
      let back_data = this.is_delete_power
        ? await deleteTeamData({
            class_id: row.team_id,
          })
        : await deleteTeamUser({
            class_id: row.team_id,
          });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getTeamList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    async deleteUser(team_id, user_id) {
      let back_data = await deleteTeamUser({
        class_id: team_id,
        user_id: user_id,
      });
      if (back_data.status) {
        this.$message({
          type: "success",
          message: back_data.message,
        });
        this.$store.dispatch("user/getTeamList");
      } else {
        this.$message({
          type: "error",
          message: back_data.message,
        });
      }
    },
    handleSizeChange(val) {
      this.page_sizes = val;
    },
    handleCurrentChange(val) {
      this.current_page = val;
    },
  },
};
</script>

<style scoped>
.team-list-child .pagination-2 {
  display: none;
}
.team-list-child .team-list-introduce {
  line-height: 23px;
  font-size: 1.2em;
  font-family: "宋体";
  font-weight: bold;
  letter-spacing: 2px;
}
.team-list-child .delete-user-button {
  width: 80px;
  background-color: rgba(241, 103, 10, 0.521);
  border-radius: 20px;
  margin: 1px 0;
  padding: 0;
}
@media screen and (max-width: 600px) {
  .team-list-child .pagination-2 {
    display: block;
  }
  .team-list-child .pagination-1 {
    display: none;
  }
}
</style>
