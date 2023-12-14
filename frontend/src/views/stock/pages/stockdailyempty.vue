<template>
  <div class="stock-empty">
    <!-- <img :src="image" /> -->
    <el-image :src="image" />
    <div v-if="no_content" class="description">
      <p>
        <mallki class-name="mallki-text" :text="content1" />
      </p>
      <p>
        <mallki class-name="mallki-text" :text="content2" />
      </p>
      <p>
        <mallki class-name="mallki-text" :text="content3" />
      </p>
      <p>
        <mallki class-name="mallki-text" :text="content4" />
      </p>
    </div>
  </div>
</template>
<script>
import Mallki from "@/components/TextHoverEffect/Mallki";

export default {
  name: "stockdaily",
  props: {
    image: {
      type: String,
      default: require("@/assets/bingbing.jpg"),
    },
    content1: {
      type: String,
      default: "冰冰说没有东西",
    },
    content2: {
      type: String,
      default: "冰冰说没有东西",
    },
    content3: {
      type: String,
      default: "",
    },
    content4: {
      type: String,
      default: "",
    },
    no_content: {
      type: Boolean,
      default: true,
    },
  },

  components: { Mallki },
  data() {
    return {};
  },
  computed: {},
  created() { },
  methods: {},
};
</script>
<style  lang="scss" scoped>
.stock-empty {
  margin: 15px 0;
  width: 100%;
  height: 600px;
  position: relative;

  .el-image {
    width: 100%;
    border-radius: 16px;
    position: absolute;
    opacity: 0.8;
  }

  .description {
    width: 100%;
    height: 300px;
    text-align: center;

    .mallki-text {
      top: 38%;
      font-size: 1.5rem;
      position: relative;
    }
  }
}
</style>
