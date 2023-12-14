<template>
  <el-card class="stock-card">
    <div class="seal-content">
      <div class="seal-result">
        <span v-if="stockinfo.return_0 > 0">
          <svg-icon icon-class="stock-up" />
        </span>
        <span v-else> <svg-icon icon-class="stock-down" /></span>
      </div>
      <div class="stockinfo">
        <div class="stock-card-header">
          <el-button size="mini" circle icon="el-icon-s-promotion"></el-button>
          <span>{{ stockinfo.date }}|{{ stockinfo.name }} {{ stockinfo.code }}</span>
          <el-tag type="warning" size="mini">{{ stockinfo.close }}</el-tag>
          <el-tag style="float: right" type="danger" size="mini">{{
            stockinfo.industry
          }}</el-tag>
        </div>
        <div class="stocktag">
          <el-tag v-show="stockinfo.is_suo" size="mini" color="#4169E1"
            >缩量</el-tag
          >
          <el-tag v-show="stockinfo.is_fang" size="mini" color="#FF69B4"
            >放量</el-tag
          >
          <el-tag v-show="stockinfo.is_bei" size="mini" color="#3CB371"
            >倍量</el-tag
          >
          <el-tag v-show="stockinfo.is_ma10_x" size="mini" color="#20B2AA"
            >上穿10日</el-tag
          >
          <el-tag v-show="stockinfo.is_ma20_x" size="mini" color="#FFD700"
            >上穿20日</el-tag
          >
          <el-tag v-show="stockinfo.is_ma30_x" size="mini" color="#EE82EE"
            >上穿30日</el-tag
          >
          <el-tag v-show="stockinfo.is_zt" size="mini" color="#DC143C"
            >涨停</el-tag
          >
        </div>
        <div class="stockdetail">
          <el-descriptions :column="2" size="mini">
            <el-descriptions-item label="涨跌幅(%)">
              <el-tag v-if="stockinfo.pct_chg >= 0" size="mini" type="danger">{{
                stockinfo.pct_chg
              }}</el-tag>
              <el-tag v-else size="mini" type="success">{{
                stockinfo.pct_chg
              }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="实际涨跌幅(%)">
              <el-tag
                v-if="stockinfo.return_0 >= 0"
                size="mini"
                type="danger"
                >{{ stockinfo.return_0 }}</el-tag
              >
              <el-tag v-else size="mini" type="success">{{
                stockinfo.return_0
              }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="成交额">
              <el-tag v-if="stockinfo.amount > 100000000" size="mini" type="danger">{{
                stockinfo.amount | VolumeFilter
              }}</el-tag>
              <el-tag v-else size="mini" type="success">{{
                stockinfo.amount | VolumeFilter
              }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="流通市值(亿)">
              <el-tag
                v-if="stockinfo.market >= 100"
                size="mini"
                type="danger"
                >{{ stockinfo.market }}</el-tag
              >
              <el-tag v-else size="mini" type="success">{{
                stockinfo.market
              }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </div>
  </el-card>
</template>
<script>
export default {
  name: "stockdetail",
  props: {
    stockinfo: {
      type: Object,
      default: () => {},
    },
  },
  components: {},
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>