<template>
  <el-table
    :data="
      Data.slice(
        (listQuery.page - 1) * listQuery.limit,
        listQuery.page * listQuery.limit
      )
    "
    size="mini"
    :stripe="true"
    :fit="true"
  >
    <el-table-column
      v-for="item in nav"
      :key="item.prop"
      :prop="item.prop"
      :sortable="item.sortable"
      :label="item.label"
    ></el-table-column>
  </el-table>
  <el-pagination
    class="pagination-1"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="listQuery.page"
    :page-sizes="[20, 50, 100, 200]"
    :page-size="listQuery.limit"
    layout="total, sizes, prev, pager, next, jumper"
    :total="Data.length"
    :hide-on-single-page="true"
  >
  </el-pagination>
  <el-pagination
    class="pagination-2"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="listQuery.page"
    :page-sizes="[20, 50, 100, 200]"
    :page-size="listQuery.limit"
    layout="prev, pager, next"
    :total="Data.length"
    :hide-on-single-page="true"
  >
  </el-pagination>
</template>

<script>
export default {
  props: {
    nav: {
      default: [
        {
          prop: "id",
          sortable: true,
          label: "编号",
        },
      ],
    },
  },
  setup() {},
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 20,
      },
    };
  },
  methods: {
    handleSizeChange(val) {
      this.listQuery.limit = val;
    },
    handleCurrentChange(val) {
      this.listQuery.page = val;
    },
  },
};
</script>
