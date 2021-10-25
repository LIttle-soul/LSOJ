<template>
  <div class="level-list-child">
    <el-card>
      <template #header>
        <div class="table-header">
          <i class="el-icon-date"></i>
          关卡列表
        </div>
        <el-input placeholder="请输入内容" size="mini" v-model="search_data" class="input-with-select">
          <template #append>
            <el-button icon="el-icon-search" @click="search_all_data"></el-button>
          </template>
        </el-input>
      </template>
      <div>
        <el-table :data="
            Data.slice(
              (current_page - 1) * page_sizes,
              current_page * page_sizes
            )
          " size="mini" :stripe="false" :fit="true" row-key="id" style="width: 100%;"
          :default-sort="{ prop: 'id', order: 'descending' }"
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
          <el-table-column prop="id" label="关卡编号"> </el-table-column>
          <el-table-column prop="level_title" label="关卡标题"> </el-table-column>
          <el-table-column prop="level_description" label="关卡描述"> </el-table-column>
          <el-table-column prop="level_pre" label="前置关卡"> </el-table-column>
          <el-table-column prop="level_belong" label="属于"> </el-table-column>
          <el-table-column prop="level_creator" label="创建者"> </el-table-column>
          <el-table-column prop="level_status" fixed="right" width="50px" label="状态">
            <template #default="scope">
              <el-switch v-model="scope.row.level_status" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="125px" label="操作">
            <template #default="scope">
              <el-button size="mini" type="primary" circle icon="el-icon-edit" @click="handleEditClick(scope.row)">
              </el-button>
              <el-button size="mini" type="success" circle icon="el-icon-check" @click="handleCheckClick(scope.row)">
              </el-button>
              <el-button size="mini" type="danger" circle icon="el-icon-delete" @click="handleDeleteClick(scope.row)">
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination class="pagination-1" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes"
        layout="total, sizes, prev, pager, next, jumper" :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
      <el-pagination class="pagination-2" @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="current_page" :page-sizes="[20, 50, 100, 200]" :page-size="page_sizes" layout="prev, pager, next"
        :total="Data.length" :hide-on-single-page="true">
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

export default {
  name: "LevelListChild",
  mounted () { },
  computed: {
    listenSoreMsg () {
      return this.$store.state.search_data;
    },
    ...mapState('level', {
      Data: state => state.level_list
    }),
    ...mapGetters('level', {
      filterProvince: 'filterLevelData'
    })
  },
  watch: {
    listenSoreMsg () {
      this.search_data = this.listenSoreMsg;
      this.search_all_data();
    },
  },
  props: {
    admin: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return {
      search_data: "",
      current_page: 1,
      page_sizes: 50,
      Data: [
        {
          id: 1,
          level_title: "大关卡",
          level_description: "125",
          level_creator: "123",
          children: [
            {
              id: 2,
              level_title: "大关卡",
              level_description: "125",
              level_pre: 123,
              level_belong: "大关卡",
              level_creator: "123",
            }
          ]
        },
        {
          id: 3,
          level_title: "大关卡",
          level_description: "125",
          level_creator: "123",
          children: [
            {
              id: 4,
              level_title: "大关卡",
              level_description: "125",
              level_pre: 123,
              level_belong: "大关卡",
              level_creator: "123",
            }
          ]
        },
      ],
      total: 3,
      listQuery: {
        page: 1,
        limit: 10,
      },
    };
  },
  methods: {
    handleSizeChange (val) {
      this.page_sizes = val;
    },
    handleCurrentChange (val) {
      this.current_page = val;
    },
    search_all_data () {
      this.Data = this.filterProvince(this.search_data);
    },
    handleEditClick (val) {
      console.log(val);
    },
    handleCheckClick (val) {
      console.log(val);
    },
    handleDeleteClick (val) {
      console.log(val);
    },
  },
};
</script>

<style>
.level-list-child .table-header {
  font: 1.2em "楷体";
  letter-spacing: 3px;
  height: 30px;
  width: 50%;
  min-width: 210px;
  float: left;
}
.level-list-child .el-card__header {
  height: 60px;
}
.level-list-child .input-with-select {
  width: 205px;
  float: right;
  margin-right: 10px;
  transform: translateY(-1px);
}
.level-list-child .current-time {
  font-size: 10px;
  color: darkturquoise;
  letter-spacing: 1px;
}
.level-list-child .pagination-2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .level-list-child .input-with-select {
    display: none;
  }
  .level-list-child .pagination-2 {
    display: block;
  }
  .level-list-child .pagination-1 {
    display: none;
  }
}
</style>
