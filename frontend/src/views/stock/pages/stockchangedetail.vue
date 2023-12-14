<template>
  <el-card class="stock-card">
    <div class="stockinfo">
      <div class="stock-card-header">
        <el-button size="mini" circle icon="el-icon-s-promotion"></el-button>
        <span>{{ stockinfo.name }} {{ stockinfo.code }}</span>
        |
        <el-tag v-if="stockinfo.pct_chg >= 3" size="mini" type="danger"
          >{{ stockinfo.pct_chg }}%</el-tag
        >
        <el-tag v-else size="mini" type="success"
          >{{ stockinfo.pct_chg }}%</el-tag
        >
        <el-tag style="float: right" type="danger" size="mini">{{
          stockinfo.industry
        }}</el-tag>
      </div>
      <div class="stockdetail">
        <el-descriptions :column="2" size="mini" border>
          <el-descriptions-item label="时间">
            <span>{{ stockinfo.time }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="信息">
            <span>{{ stockinfo.info }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag size="mini" type="danger">{{
              symbol_map[stockinfo.type]
            }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="流通市值(亿)">
            <el-tag v-if="stockinfo.market >= 100" size="mini" type="danger">{{
              stockinfo.market
            }}</el-tag>
            <el-tag v-else size="mini" type="success">{{
              stockinfo.market
            }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
  </el-card>
</template>
<script>
export default {
  name: "stockchangedetail",
  props: {
    stockinfo: {
      type: Object,
      default: () => {},
    },
  },
  components: {},
  data() {
    return {
      symbol_map: {
        8201: "火箭发射",
        8202: "快速反弹",
        8193: "大笔买入",
        4: "封涨停板",
        32: "打开跌停板",
        64: "有大买盘",
        8207: "竞价上涨",
        8209: "高开5日线",
        8211: "向上缺口",
        8213: "60日新高",
        8215: "60日大幅上涨",
        8204: "加速下跌",
        8203: "高台跳水",
        8194: "大笔卖出",
        8: "封跌停板",
        16: "打开涨停板",
        128: "有大卖盘",
        8208: "竞价下跌",
        8210: "低开5日线",
        8212: "向下缺口",
        8214: "60日新低",
        8216: "60日大幅下跌",
      },
    };
  },
  created() {},
  methods: {},
};
</script>