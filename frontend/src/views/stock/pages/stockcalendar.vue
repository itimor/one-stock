<template>
  <div class="calendar-body">
    <mallki class-name="mallki-text" :text="title" />
    (<span style="color: red">{{ total }}</span
    >)
     加自选观察三分钟在下手
    <el-tooltip class="item" effect="dark" content="回到今天" placement="top">
      <el-button
        style="float: right"
        size="mini"
        circle
        @click="$refs.calendar.setToday()"
        >to</el-button
      >
    </el-tooltip>
      

    <el-divider><i class="el-icon-cold-drink"></i></el-divider>
    <calendar ref="calendar" :lunar="lunar" @select="selectDate"></calendar>
  </div>
</template>
<script>
import Calendar from "@/components/Calendar";
import Mallki from "@/components/TextHoverEffect/Mallki";

export default {
  name: "stockcalendar",
  props: {
    title: {
      type: String,
      default: "冰冰看股票",
    },
    total: {
      type: Number,
      default: 0,
    },
    selectDate: {
      type: Function,
      default: null,
    },
  },
  components: {
    Calendar,
    Mallki,
  },
  data() {
    return {
      multi: true, // 多选模式
      range: true, // 范围模式
      lunar: true, // 显示农历
    };
  },
};
</script>
<style lang="scss" scoped>
.mallki-text {
  top: 3px;
}
</style>