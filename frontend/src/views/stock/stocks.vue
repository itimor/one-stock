<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
      >{{ "搜索" }}</el-button>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column label="股票简称" prop="name"></el-table-column>
      <el-table-column label="股票代码" prop="code"></el-table-column>
      <el-table-column label="所属地区" prop="area"></el-table-column>
      <el-table-column label="所属行业" prop="industry"></el-table-column>
      <el-table-column label="市场类型" prop="market"></el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > listQuery.limit"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>
<script>
import { stocks } from "@/api/all";
import Pagination from "@/components/Pagination";

export default {
  name: "stocks",
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 30,
        search: undefined,
        ordering: undefined
      }
    };
  },
  computed: {},
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      stocks.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    }
  }
};
</script>
