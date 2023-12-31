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
      <el-select
        class="filter-item"
        clearable
        v-model="listQuery.method"
        @change="handleFilter"
        placeholder="请选择请求方式"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :disabled="item.disabled"
        >
        </el-option>
      </el-select>
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
      @sort-change="handleSortChange"
    >
      <el-table-column
        label="请求方法"
        prop="method"
        width="100"
      ></el-table-column>
      <el-table-column label="请求路径" prop="uri"></el-table-column>
      <el-table-column label="请求参数" prop="query_string">
        <template slot-scope="{ row }">
          <el-tag size="mini">request.params</el-tag>
          : {{ JSON.parse(row.query_string).query_params }}
          <br />
          <el-tag size="mini">request.body</el-tag>
          : {{ JSON.parse(row.query_string).json }}
        </template>
      </el-table-column>
      <el-table-column
        label="请求用户"
        prop="user"
        width="100"
      ></el-table-column>
      <el-table-column
        label="请求ip"
        prop="remote_ip"
        width="100"
      ></el-table-column>
      <el-table-column
        label="请求时间"
        prop="create_time"
        width="200"
      ></el-table-column>
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
import { audit, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "audit",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      options: [
        {
          value: "GET",
          label: "GET",
          disabled: true,
        },
        {
          value: "POST",
          label: "POST",
        },
        {
          value: "PUT",
          label: "PUT",
        },
        {
          value: "DELETE",
          label: "DELETE",
        },
      ],
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
      },
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("audit")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      audit.requestGet(this.listQuery).then((response) => {
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
    },
  },
};
</script>
