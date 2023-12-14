<template>
  <div class="app-container">
    <el-row>
      <el-card class="box-card">
        <div slot="header" class="card-title">
          <mallki class-name="mallki-text" text="checkstock" />
        </div>
        <div style="margin-bottom: 10px">
          <el-col
            v-for="(v, k, index) in zt_list"
            :key="k"
            :span="3"
            class="text-center"
          >
            <router-link
              :class="`pan-btn ${color_list[index % 10]}-btn`"
              :to="{ name: 'stockcheck', params: { t: k } }"
              target="_blank"
            >
              {{ v }}
            </router-link>
          </el-col>
        </div>
      </el-card>
    </el-row>
    <stock-daily-empty
      content="一只专注看盘的韭菜"
      :image="image1"
    ></stock-daily-empty>
    <stock-daily-empty
      content="一只亏到自闭的韭菜"
      :image="image2"
    ></stock-daily-empty>
  </div>
</template>
<script>
import PanThumb from "@/components/PanThumb";
import Mallki from "@/components/TextHoverEffect/Mallki";
import StockDailyEmpty from "./pages/stockdailyempty";

export default {
  name: "checkstocks",
  components: {
    PanThumb,
    Mallki,
    StockDailyEmpty,
  },
  data() {
    return {
      image1:
        "https://pica.zhimg.com/80/v2-4559cb3824cb9a556e08232dda42b244_1440w.jpg",
      image2:
        "https://pic1.zhimg.com/80/v2-110d5a6ba50176fc56cb594f6c9e7e01_1440w.jpg",
      color_list: [
        "blue",
        "blueviolet",
        "green",
        "lightblue",
        "pink",
        "tiffany",
        "violet",
        "lightsalmon",
        "red",
        "yellow",
      ],
      zt_list: {
        is_ma10_x: "上穿10日",
        is_ma20_x: "上穿20日",
        is_ma30_x: "上穿30日",
        is_zt: "涨停",
        is_fang: "放量",
        is_suo: "缩量",
        is_bei: "倍量",
      },
    };
  },
};
</script>
