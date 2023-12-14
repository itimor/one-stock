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
      <el-table-column label="简称" prop="name" width="110"> </el-table-column>
      <el-table-column label="代码" prop="code" width="100"></el-table-column>
      <el-table-column label="开盘价" prop="open">
        <template slot-scope="{ row }">
          <el-tag v-if="row.open >= row.pre_close" type="danger">{{
            row.open
          }}</el-tag>
          <el-tag v-else type="success">{{ row.open }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="收盘价" prop="close"></el-table-column>
      <el-table-column label="最高价" prop="high"></el-table-column>
      <el-table-column label="最低价" prop="low"></el-table-column>
      <el-table-column
        label="涨跌幅"
        prop="pct_chg"
        sortable="custom"
        width="100"
      >
        <template slot-scope="{ row }">
          <el-tag v-if="row.pct_chg >= 0" type="danger"
            >{{ row.pct_chg }}%</el-tag
          >
          <el-tag v-else type="success">{{ row.pct_chg }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="实际涨跌幅"
        prop=" return_0"
        sortable="custom"
        width="120"
      >
        <template slot-scope="{ row }">
          <el-tag v-if="row.return_0 >= 0" type="danger"
            >{{ row.return_0 }}%</el-tag
          >
          <el-tag v-else type="success">{{ row.return_0 }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="成交量" prop="volume" sortable="custom">
        <template slot-scope="{ row }">
          <el-tooltip
            class="item"
            effect="dark"
            :content="row.volume.toString()"
            placement="left"
          >
            <el-tag v-if="row.volume > 100000000" type="danger">{{
              row.volume | VolumeFilter
            }}</el-tag>
            <el-tag v-else type="success">{{
              row.volume | VolumeFilter
            }}</el-tag>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column label="成交额" prop="amount" sortable="custom">
        <template slot-scope="{ row }">
          <el-tooltip
            class="item"
            effect="dark"
            :content="row.amount.toString()"
            placement="left"
          >
            <el-tag v-if="row.amount > 100000000" type="danger">{{
              row.amount | VolumeFilter
            }}</el-tag>
            <el-tag v-else type="success">{{
              row.amount | VolumeFilter
            }}</el-tag>
          </el-tooltip>
        </template>
      </el-table-column>
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
import { stockdaily } from "@/api/all";
import Pagination from "@/components/Pagination";
import clip from "@/utils/clipboard";

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
    };
  },
  computed: {},
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      stockdaily.requestGet(this.listQuery).then((response) => {
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
