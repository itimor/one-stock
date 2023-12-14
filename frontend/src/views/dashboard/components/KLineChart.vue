<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
require("echarts/theme/macarons"); // echarts theme

export default {
  props: {
    className: {
      type: String,
      default: "chart",
    },
    width: {
      type: String,
      default: "100%",
    },
    height: {
      type: String,
      default: "300px",
    },
    chartData: {
      type: Array,
      default: () => [
        [10, 34, 8, 38],
        [45, 20, 15, 58],
        [50, 54, 6, 58],
      ],
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
    });
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      const echarts = require('echarts');
      this.chart = echarts.init(this.$el, "macarons");
      this.chart.setOption({
        xAxis: {
          show: true,
          data: ["2", "1", "0"],
        },
        yAxis: {
          show: true,
        },
        series: [
          {
            type: "candlestick",
            data: this.chartData,
          },
        ],
      });
    },
  },
};
</script>
