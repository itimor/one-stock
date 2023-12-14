<template>
  <div class="login-container">
    <div class="loader">
      <div class="load_base load1">
        <div class="load_base out_loader"></div>
      </div>
      <el-form
        ref="loginForm"
        :model="loginForm"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <el-form-item prop="username">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="账号"
            name="username"
            type="text"
            auto-complete="on"
          />
        </el-form-item>

        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            auto-complete="on"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>
      </el-form>
      <div class="load_base load2" @click="handleLogin">
        <div class="load_base in_loader in_loader1">风</div>
        <div class="load_base in_loader in_loader2">火</div>
        <div class="load_base in_loader in_loader3">雷</div>
        <div class="load_base in_loader in_loader4">电</div>
      </div>
    </div>

    <div class="background">
      <span>看股票</span>
      <div class="background_marge_title"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  components: {},
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      passwordType: "password",
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
    };
  },
  watch: {
    $route: {
      handler: function (route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true,
    },
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {
    if (this.loginForm.username === "") {
      this.$refs.username.focus();
    } else if (this.loginForm.password === "") {
      this.$refs.password.focus();
    }
  },
  methods: {
    checkCapslock({ shiftKey, key } = {}) {
      if (key && key.length === 1) {
        if (
          (shiftKey && key >= "a" && key <= "z") ||
          (!shiftKey && key >= "A" && key <= "Z")
        ) {
          this.capsTooltip = true;
        } else {
          this.capsTooltip = false;
        }
      }
      if (key === "CapsLock" && this.capsTooltip === true) {
        this.capsTooltip = false;
      }
    },
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    handleLogin() {
      this.loading = true;
      this.$store
        .dispatch("user/login", this.loginForm)
        .then(() => {
          this.$router.push({ path: this.redirect || "/" }).catch(() => {
            //如果不catch, 登录进去浏览器控制台会报错vue-router.esm.js:2051 Uncaught (in promise) undefined
            //https://juejin.im/post/5d80d961f265da03ca11a1d9
          });
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
  },
};
</script>
<style lang="scss" scoped>
.login-container {
  .login-form {
    position: relative;
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    overflow: hidden;
    left: calc(50% - 1.25vmin - 45vmin);
    top: -30vmin;
    .el-form-item {
      border-radius: 5px;
      color: #454545;
      .el-input {
        display: inline-block;
        border: 0px;
        height: 47px;

        input {
          border: 0;
          border-radius: 0;
          padding: 12px 5px 12px 15px;
        }
      }
    }
    svg {
      color: #0e93db;
    }
    .svg-container {
      padding: 6px 5px 6px 15px;
      vertical-align: middle;
      width: 20vmin;
      display: inline-block;
    }

    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      cursor: pointer;
      user-select: none;
    }
  }
  .background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #b3d7f8;
    z-index: 0;
    color: black;
    font-size: 5vmin;
    font-family: "Open Sans", sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 3vmin;
    transition: 0.5s;
    text-align: center;
    span {
      background: #b3d7f8;
      margin: 0 auto;
      width: 80vmin;
      display: block;
      margin-top: 18.6vmin;
      &:before {
        display: inline-block;
        content: "冰冰";
      }
    }

    .background_marge_title {
      position: absolute;
      background: #4a2701;
      width: 100vw;
      height: 0.5vh;
      top: 22.1vmin;
      z-index: -1;
    }
  }
  .loader:hover + .background span:before {
    content: "韭菜";
  }

  .loader:hover + .background {
    cursor: pointer;
    filter: invert(100%);
    transition: 0.5s;
  }
  .loader {
    z-index: 1;
    position: absolute;
    top: 60%;
    left: 50%;
    transition: 0.5s;
  }
  .load_base {
    position: absolute;
    background: black;
  }
  .load1,
  .load2 {
    width: 20vmin;
    height: 20vmin;
    left: calc(50% + 1.25vmin - 35vmin);
    top: calc(50% - 1.25vmin - 10vmin);
  }
  .load1 {
    animation: load1 2s ease infinite;
  }
  .load2 {
    background: transparent;
    animation: load2 2s ease infinite;
  }
  .out_loader {
    width: 18vmin;
    height: 18vmin;
    left: calc(50% - 9vmin);
    top: calc(50% - 9vmin);
    background: #ebefec;
    animation: load1 2s ease infinite;

    display: flex;
    align-items: center;
    justify-content: space-around;
    font-size: calc(18vmin * 0.65);
    font-weight: bold;

    &::after {
      color: #eb9e4c;
      content: "股";
      text-shadow: 0 0 10px #fff, 0 0 10px #fff, 0 0 20px #b3d7f8,
        0 0 30px #b3d7f8, 0 0 40px #b3d7f8, 0 0 50px #b3d7f8, 0 0 60px #b3d7f8;
    }
  }
  .loader:hover > .load_base .out_loader::after {
    color: #f890c9;
    content: "进";
  }
  .in_loader {
    width: 3vmin;
    height: 3vmin;
    border: 0.3vmin solid #f890c9;
    border-radius: 100vmin;
    background: #ebefec;
    text-align: center;
  }
  .in_loader1 {
    animation: in_load1 2s ease infinite;
  }
  .in_loader2 {
    animation: in_load2 2s ease infinite;
  }
  .in_loader3 {
    animation: in_load3 2s ease infinite;
  }
  .in_loader4 {
    animation: in_load4 2s ease infinite;
  }
  @keyframes load1 {
    0% {
      transform: rotate(0deg);
      border-radius: 2vmin;
    }
    60% {
      transform: rotate(360deg);
      border-radius: 10vmin;
    }
    80% {
      transform: rotate(360deg);
      border-radius: 7vmin;
    }
    90% {
      transform: rotate(360deg);
      border-radius: 3.5vmin;
    }
    100% {
      transform: rotate(360deg);
      border-radius: 2vmin;
    }
  }
  @keyframes load2 {
    0% {
      transform: rotate(0deg);
    }
    60% {
      transform: rotate(-360deg);
    }
    100% {
      transform: rotate(-360deg);
    }
  }
  @keyframes in_load1 {
    0% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    25% {
      opacity: 0;
    }
    35% {
      opacity: 1;
    }
    60% {
      top: calc(-50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    68% {
      opacity: 1;
    }
    72% {
      opacity: 0;
    }
    100% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
  }
  @keyframes in_load2 {
    0% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    25% {
      opacity: 0;
    }
    35% {
      opacity: 1;
    }
    70% {
      top: calc(50% - 1.25vmin);
      left: calc(150% - 1.25vmin);
    }
    76% {
      opacity: 1;
    }
    80% {
      opacity: 0;
    }
    100% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
  }
  @keyframes in_load3 {
    0% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    25% {
      opacity: 0;
    }
    35% {
      opacity: 1;
    }
    80% {
      top: calc(150% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    84% {
      opacity: 1;
    }
    88% {
      opacity: 0;
    }
    100% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
  }
  @keyframes in_load4 {
    0% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
    25% {
      opacity: 0;
    }
    35% {
      opacity: 1;
    }
    90% {
      top: calc(50% - 1.25vmin);
      left: calc(-50% - 1.25vmin);
    }
    91% {
      opacity: 1;
    }
    95% {
      opacity: 0;
    }
    100% {
      opacity: 0;
      top: calc(50% - 1.25vmin);
      left: calc(50% - 1.25vmin);
    }
  }
}
</style>