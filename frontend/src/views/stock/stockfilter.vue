<template>
  <div class="app-container">
    <el-row :gutter="10">
      <el-col :span="8">
        <sticky :sticky-top="16">
          <template>
            <stock-calendar :title="title" :total="list.length" :selectDate="selectDate"></stock-calendar>
            <el-divider><i class="el-icon-cold-drink"></i></el-divider>
            <stock-daily-empty :image="image" content1="定势 预期 超预期 弱转强 强转弱" content2="只操作强势的股票" content3="注意板块共振"
              content4="拉直线的不接,有冲高回落风险"></stock-daily-empty>
          </template>
        </sticky>
      </el-col>
      <el-col :span="16" v-loading="loading" element-loading-text="冰冰说不要着急"
        element-loading-background="rgba(0, 0, 0, 0.8)">
        <el-card>
          <div style="margin: 10px 0;">
            <el-button type="success" plain @click="Handlegao">高高高</el-button>
            <el-button type="danger" plain @click="Handlehuo">火火火</el-button>
            <el-button type="primary" plain @click="Handlemai">买买买</el-button>
            <el-button type="primary" plain @click="Handlesix">六六六</el-button>
            <el-divider direction="vertical"></el-divider>

            <el-radio-group v-if="listQuery.tm == '09:25:00'" v-model="listQuery.tm" @change="HandleCheck">
              <el-radio label="09:25:00">09:25</el-radio>
            </el-radio-group>

            <el-radio-group v-else v-model="listQuery.tm" @change="HandleCheck">
              <el-radio label="09:30:00">09:30</el-radio>
              <el-radio label="09:34:00">09:34</el-radio>
              <el-radio label="09:38:00">09:38</el-radio>
              <el-radio label="09:42:00">09:42</el-radio>
            </el-radio-group>
          </div>
          <el-table :data="list" v-loading="listLoading" border style="width: 100%" @row-click="handleStock"
            @sort-change="handleSortChange">
            <el-table-column label="星级" prop="c" align="center" sortable="custom" width="80">
              <template slot-scope="{ row }">
                <span>{{ row.c }}
                  <svg-icon icon-class="star" />
                </span>
              </template>
            </el-table-column>
            <el-table-column label="时间" prop="time" align="center" sortable="custom" width="80">
              <template slot-scope="{ row }">
                <span>{{ row.time | parseTimeZ }}</span>
              </template>
            </el-table-column>
            <el-table-column label="简称" prop="name" align="center" width="80"></el-table-column>
            <el-table-column label="代码" prop="code" align="center" width="80"></el-table-column>
            <el-table-column label="价格" prop="close" align="center" width="80"></el-table-column>
            <el-table-column label="实际涨幅" prop="return_0" align="center" sortable="custom">
              <template slot-scope="{ row }">
                <el-tag v-if="row.return_0 > 0" type="danger">{{
                    row.return_0 | VolumeFilter
                }}</el-tag>
                <el-tag v-else type="success">{{
                    row.return_0 | VolumeFilter
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="涨跌幅" prop="return_0" align="center" sortable="custom">
              <template slot-scope="{ row }">
                <el-tag v-if="row.pct_chg > 5" type="danger">{{
                    row.pct_chg | VolumeFilter
                }}</el-tag>
                <el-tag v-else type="success">{{
                    row.pct_chg | VolumeFilter
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="行业" prop="industry" align="center"></el-table-column>
            <el-table-column label="市值(亿)" prop="market" align="center" sortable="custom">
              <template slot-scope="{ row }">
                <el-tag v-if="row.market > 60" type="danger">{{
                    row.market | VolumeFilter
                }}</el-tag>
                <el-tag v-else type="success">{{
                    row.market | VolumeFilter
                }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-drawer title="上榜记录" :visible.sync="drawer" :with-header="false">
      <el-table :data="history_list" border style="width: 100%">
        <el-table-column label="时间" prop="time" sortable="custom"></el-table-column>
        <el-table-column label="简称" prop="name"> </el-table-column>
        <el-table-column label="类型" prop="type">
          <template slot-scope="{ row }">
            <span>{{ symbol_map[row.type] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="幅度(%)" prop="pct_chg"></el-table-column>
        <el-table-column label="手数" prop="hand"></el-table-column>
      </el-table>
    </el-drawer>
  </div>
</template>
<script>
import { stockchangefilter, stockchange } from "@/api/all";
import Sticky from "@/components/Sticky";
import Mallki from "@/components/TextHoverEffect/Mallki";
import clip from "@/utils/clipboard";
import { parseTime } from "@/utils/index";
import StockCalendar from "./pages/stockcalendar";
import StockDailyEmpty from "./pages/stockdailyempty";

export default {
  name: "stockfilter",
  components: {
    Sticky,
    Mallki,
    StockCalendar,
    StockDailyEmpty,
  },
  data() {
    return {
      title: "冰冰选股票",
      image: require("@/assets/bingbing2.jpeg"),
      listQuery: {
        date: "",
        type: "",
        tm: "09:25:00",
        ordering: "-c",
      },
      list: [],
      listLoading: false,
      loading: false,
      symbol_map: {
        666: '六六大顺',
        8201: "火箭发射",
        8193: "大笔买入",
        8207: "竞价上涨",
        8209: "高开5日线",
        8215: "60日大幅上涨",
      },
      history_listQuery: {
        date: "",
        type: "",
        code: "",
        ordering: "time",
      },
      history_list: [],
      drawer: false,
    };
  },
  computed: {},
  created() { },
  methods: {
    selectDate(date, $event) {
      this.listQuery.date = date.join("-");
      this.getList();
    },
    Handlegao() {
      this.listQuery.type = "";
      this.listQuery.tm = "09:25:00";
      this.getList();
    },
    Handlehuo() {
      this.listQuery.type = '8201';
      this.listQuery.tm = "09:30:00";
      this.getList();
    },
    Handlemai() {
      this.listQuery.type = '8193';
      this.listQuery.tm = "09:30:00";
      this.getList();
    },
    Handlesix() {
      this.listQuery.type = '666';
      this.listQuery.tm = "09:30:00";
      this.getList();
    },
    HandleCheck(val) {
      this.getList();
    },
    getList() {
      this.listLoading = true;
      if (this.listQuery.date == "") {
        const d = new Date();
        this.listQuery.date = parseTime(d, "{y}-{m}-{d}");
      }
      stockchangefilter.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.listLoading = false;
      });
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
    getHistoryList() {
      stockchange.requestGet(this.history_listQuery).then((response) => {
        this.history_list = response.results;
      });
    },
    handleStock(row, column, event) {
      clip(row.code, event);
      this.drawer = true;
      this.history_listQuery.code = row.code;
      this.history_listQuery.date = row.date;
      this.history_listQuery.type = row.type;
      this.getHistoryList();
    },
  },
};
</script>
