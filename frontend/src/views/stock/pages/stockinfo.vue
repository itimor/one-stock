<template>
  <div v-if="stockinfo.id">
    <stock-detail :stockinfo="stockinfo"></stock-detail>
  </div>
  <div v-else>
    <stock-daily-empty :image="image" content1="交易一定要杀伐果断,去弱留强" ></stock-daily-empty>
  </div>
</template>
<script>
import StockDailyEmpty from "./stockdailyempty";
import StockDetail from "./stockdetail";

export default {
  name: "stockinfo",
  props: {
    stockinfo: {
      type: Object,
      default: {},
    },
    getList: {
      type: Function,
      default: null,
    },
  },
  components: { StockDetail, StockDailyEmpty },
  data() {
    return {
      change_tag: false,
      color_list: ["nan", "xxoo", "primary", "success", "warning", "danger"],
      image: require("@/assets/bingbing2.jpeg"),
    };
  },
  computed: {},
  created() { },
  methods: {},
};
</script>