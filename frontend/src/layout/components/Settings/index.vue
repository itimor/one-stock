<template>
  <div>
    <div class="drawer-container">
      <div>
        <h3 class="drawer-title">{{ $t("settings.title") }}</h3>

        <div class="drawer-item">
          <span>{{ $t("settings.theme") }}</span>
          <theme-picker
            style="float: right; height: 26px; margin: -3px 8px 0 0"
            @change="themeChange"
          />
        </div>

        <div class="drawer-item">
          <span>{{ $t("settings.tagsView") }}</span>
          <el-switch v-model="tagsView" class="drawer-switch" />
        </div>

        <div class="drawer-item">
          <span>{{ $t("settings.fixedHeader") }}</span>
          <el-switch v-model="fixedHeader" class="drawer-switch" />
        </div>

        <div class="drawer-item">
          <span>{{ $t("settings.sidebarLogo") }}</span>
          <el-switch v-model="sidebarLogo" class="drawer-switch" />
        </div>

        <div class="drawer-item">
          <span>{{ $t("settings.sidebarVideo") }}</span>
          <el-switch v-model="sidebarVideo" class="drawer-switch" />
        </div>
        <div v-if="sidebarVideo">
          <el-button
            type="success"
            size="mini"
            plain
            circle
            @click="changevideo"
          >换</el-button>
          <span style="color: red">
            {{ video_name }}
          </span>
        </div>
        <div class="drawer-item">
          <span>{{ $t("settings.sidebarMusic") }}</span>
          <!-- <el-radio-group v-if="sidebarMusic" v-model="player_type" size="mini">
            <el-radio-button label="aplayer">本地云</el-radio-button>
            <el-radio-button label="netsease">网易云</el-radio-button>
          </el-radio-group> -->
          <el-switch v-model="sidebarMusic" class="drawer-switch" />
        </div>
        <!-- <el-radio-group
          v-if="(player_type == 'netsease') & sidebarMusic"
          v-model="height"
          style="margin-left: 70px"
        >
          <el-radio :label="310">展示清单</el-radio>
          <el-radio :label="90">收回清单</el-radio>
        </el-radio-group> -->
      </div>
    </div>

    <div v-if="sidebarVideo" class="sider-video">
      <div v-for="(item, index) in video_list" :key="index">
        <vueMiniPlayer
          v-if="index == video_num"
          ref="vueMiniPlayer"
          :video="video"
          :mutex="true"
          :autoplay="true"
        />
      </div>
    </div>

    <div
      v-if="player_type == 'aplayer'"
      class="aplayer-music"
      :style="{ top: buttonTop - 5 + 'px' }"
    >
      <aplayer
        v-if="sidebarMusic"
        listMaxHeight="200px"
        :autoplay="false"
        :music="music"
        :list="music_list"
        :listFolded="true"
      />
    </div>

    <div
      v-if="player_type == 'netsease'"
      class="netsease-music"
      :style="{ top: buttonTop - 10 + 'px' }"
    >
      <iframe
        v-if="sidebarMusic"
        frameborder="no"
        border="0"
        marginwidth="0"
        marginheight="0"
        width="345"
        height="300"
        :src="`//music.163.com/outchain/player?type=0&id=7102521510&auto=1&height=${height}`"
      ></iframe>
    </div>
  </div>
</template>

<script>
import ThemePicker from "@/components/ThemePicker";
import Aplayer from "vue-aplayer";
import { c_tool } from "@/api/all";

export default {
  components: { ThemePicker, Aplayer },
  props: {
    buttonTop: {
      default: 520,
      type: Number,
    },
  },
  data() {
    return {
      player_type: "aplayer", // aplayer|netsease
      height: 90,
      music: {
        title: "蜜雪冰城（王冰冰版）",
        artist: "李慕白",
        src: "http://music.163.com/song/media/outer/url?id=1857872921.mp3",
        pic: "https://pic1.zhimg.com/80/v2-7e37b26e83f51f554b76fcfe81805e9c_s.jpg",
      },
      music_list: [],
      video_num: -1,
      video_list: ["【王冰冰】100秒不心动挑战.mp4"],
      video_name: "",
      video: {
        url: "https://s-sh-3147-itimor.oss.dogecdn.com/【王冰冰】100秒不心动挑战.mp4",
        cover:
          "https://pic3.zhimg.com/80/v2-28ea0f1638165f27cd6ba6e05b8a459e_640w.jpg",
        muted: false, // 是否静音播放
        loop: false, //视频是否循环播放
        preload: "auto", //视频预加载，可选值: 'none', 'metadata', 'auto'
        volume: 1, //	默认音量
        autoplay: false, //视频自动播放
      },
    };
  },
  computed: {
    fixedHeader: {
      get() {
        return this.$store.state.settings.fixedHeader;
      },
      set(val) {
        this.$store.dispatch("settings/changeSetting", {
          key: "fixedHeader",
          value: val,
        });
      },
    },
    tagsView: {
      get() {
        return this.$store.state.settings.tagsView;
      },
      set(val) {
        this.$store.dispatch("settings/changeSetting", {
          key: "tagsView",
          value: val,
        });
      },
    },
    sidebarLogo: {
      get() {
        return this.$store.state.settings.sidebarLogo;
      },
      set(val) {
        this.$store.dispatch("settings/changeSetting", {
          key: "sidebarLogo",
          value: val,
        });
      },
    },
    sidebarVideo: {
      get() {
        return this.$store.state.settings.sidebarVideo;
      },
      set(val) {
        if (this.video_name.length < 1) {
          this.changevideo();
        }
        this.$store.dispatch("settings/changeSetting", {
          key: "sidebarVideo",
          value: val,
        });
      },
    },
    sidebarMusic: {
      get() {
        return this.$store.state.settings.sidebarMusic;
      },
      set(val) {
        this.$store.dispatch("settings/changeSetting", {
          key: "sidebarMusic",
          value: val,
        });
      },
    },
  },
  created() {
    this.getMusicList();
    this.getVideoList();
  },
  methods: {
    getMusicList() {
      this.music_list = [];
      c_tool.netseasemusic().then((response) => {
        const data = response.results;
        data.map((x) =>
          this.music_list.push({
            title: x.name,
            artist: x.ar[0].name,
            src:
              "http://music.163.com/song/media/outer/url?id=" + x.id + ".mp3",
            pic: x.al.picUrl,
            pic: "https://pic1.zhimg.com/80/v2-7e37b26e83f51f554b76fcfe81805e9c_s.jpg",
          })
        );
      });
    },
    getVideoList() {
      this.video_list = [];
      const parms = {
        bucket: "itimor",
      };
      c_tool.dogecloud(parms).then((response) => {
        const data = response.results;
        data.map((x) => this.video_list.push(x.key));
      });
    },
    themeChange(val) {
      this.$store.dispatch("settings/changeSetting", {
        key: "theme",
        value: val,
      });
    },
    changevideo() {
      if (this.video_num < 6) {
        this.video_num += 1;
      } else {
        this.video_num = 0;
      }
      this.video_name = this.video_list[this.video_num].split(".mp4")[0];
      this.video.url =
        "https://s-sh-3147-itimor.oss.dogecdn.com/" +
        this.video_list[this.video_num];
      console.log(this.video.url);
    },
  },
};
</script>

<style lang="scss" scoped>
.drawer-container {
  padding: 10px 20px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  background-color: #e8f4ff94;

  .drawer-title {
    margin-bottom: 12px;
    color: #a030ed;
    font-size: 18px;
    line-height: 22px;
  }

  .drawer-item {
    color: #ed1c90;
    font-size: 14px;
    font-weight: bold;
    padding: 6px 0;
  }

  .drawer-switch {
    float: right;
  }
}
.aplayer-music {
  position: absolute;
  left: -5px;
  width: 330px;
}
.netsease-music {
  position: absolute;
  bottom: -10px;
  left: -10px;
}
</style>
