<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-date-picker
        v-model="listQuery.date"
        class="filter-item"
        align="right"
        type="date"
        placeholder="选择日期"
        format="yyyy-MM-dd"
        value-format="yyyy-MM-dd"
        @change="handleFilter"
      />
      <el-button
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
        >{{ "搜索" }}</el-button
      >
    </div>
    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      @row-click="handleStock"
      @sort-change="handleSortChange"
    >
      <el-table-column label="日期" prop="date" width="100"></el-table-column>
      <el-table-column label="时间" prop="time" width="100"></el-table-column>
      <el-table-column label="简称" prop="name" width="110"> </el-table-column>
      <el-table-column label="代码" prop="code" width="100"></el-table-column>
      <el-table-column
        label="行业"
        prop="industry"
        width="100"
      ></el-table-column>
      <el-table-column label="价格" prop="close"></el-table-column>
      <el-table-column label="市值(亿)" prop="market"></el-table-column>
      <el-table-column label="类型" prop="type">
        <template slot-scope="{ row }">
          <span>{{ symbol_map[row.type] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="幅度(%)" prop="pct_chg"></el-table-column>
      <el-table-column label="手数" prop="hand"></el-table-column>
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
import { stockchange } from "@/api/all";
import Pagination from "@/components/Pagination";
import clip from "@/utils/clipboard";
import { parseTime } from "@/utils/index";

export default {
  name: "stockdaily",
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 30,
        date: "",
        search: undefined,
        ordering: undefined,
      },
      symbol_map: {
        8201: "火箭发射",
        8193: "大笔买入",
        8207: "竞价上涨",
        8209: "高开5日线",
        8215: "60日大幅上涨",
      },
    };
  },
  computed: {},
  created() {
    const d = new Date();
    this.listQuery.date = parseTime(d, "{y}-{m}-{d}");
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      stockchange.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleStock(row, column, event) {
      clip(row.code, event);
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
    },
  },
};
</script>
