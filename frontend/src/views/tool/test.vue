<template>
  <div class="app-container">
    <h1>测试页面</h1>
    <div>
      <h3>
        这是按钮,测试你对这个页面的相关操作权限，如果没有权限，则不会显示相应的按钮
      </h3>
      <el-button v-if="permissionList.add" size="small" type="primary">
        {{ "增加" }}
      </el-button>

      <el-button v-if="permissionList.del" size="small" type="danger">
        {{ "删除" }}
      </el-button>

      <el-button v-if="permissionList.update" size="small" type="warning">
        {{ "编辑" }}
      </el-button>

      <el-button v-if="permissionList.view" size="small" type="success">
        {{ "查看" }}
      </el-button>
    </div>

    <div class="special-btn">
      <h3>特效按钮</h3>
      <button class="draw">draw</button>
      <button class="draw meet">draw meet</button>
      <button class="center">center</button>
      <button class="spin">spin</button>
      <button class="spin circle">spin circle</button>
      <button class="spin thick">spin thick</button>
    </div>

    <h3>改造</h3>
    <button class="super-cool-btn-1">淦</button>
    <div class="super-cool-btn-2">淦</div>
  </div>
</template>

<script>
import { auth, c_tool } from "@/api/all";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "test",
  components: {},
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("test")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
  },
};
</script>
<style lang="scss" scoped>
.special-btn {
  button {
    background: none;
    border: 0;
    box-sizing: border-box;
    box-shadow: inset 0 0 0 2px #f45e61;
    color: #f45e61;
    font-size: inherit;
    font-weight: 700;
    margin: 1em;
    padding: 1em 2em;
    text-align: center;
    text-transform: capitalize;
    position: relative;
    vertical-align: middle;
  }
  button::before,
  button::after {
    box-sizing: border-box;
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .draw {
    -webkit-transition: color 0.25s;
    transition: color 0.25s;
  }
  .draw::before,
  .draw::after {
    border: 2px solid transparent;
    width: 0;
    height: 0;
  }
  .draw::before {
    top: 0;
    left: 0;
  }
  .draw::after {
    bottom: 0;
    right: 0;
  }
  .draw:hover {
    color: #60daaa;
  }
  .draw:hover::before,
  .draw:hover::after {
    width: 100%;
    height: 100%;
  }
  .draw:hover::before {
    border-top-color: #60daaa;
    border-right-color: #60daaa;
    -webkit-transition: width 0.25s ease-out, height 0.25s ease-out 0.25s;
    transition: width 0.25s ease-out, height 0.25s ease-out 0.25s;
  }
  .draw:hover::after {
    border-bottom-color: #60daaa;
    border-left-color: #60daaa;
    -webkit-transition: border-color 0s ease-out 0.5s, width 0.25s ease-out 0.5s,
      height 0.25s ease-out 0.75s;
    transition: border-color 0s ease-out 0.5s, width 0.25s ease-out 0.5s,
      height 0.25s ease-out 0.75s;
  }

  .meet:hover {
    color: #fbca67;
  }
  .meet::after {
    top: 0;
    left: 0;
  }
  .meet:hover::before {
    border-top-color: #fbca67;
    border-right-color: #fbca67;
  }
  .meet:hover::after {
    border-bottom-color: #fbca67;
    border-left-color: #fbca67;
    -webkit-transition: height 0.25s ease-out, width 0.25s ease-out 0.25s;
    transition: height 0.25s ease-out, width 0.25s ease-out 0.25s;
  }

  .center:hover {
    color: #6477b9;
  }
  .center::before,
  .center::after {
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    -webkit-transform-origin: center;
    -ms-transform-origin: center;
    transform-origin: center;
  }
  .center::before {
    border-top: 2px solid #6477b9;
    border-bottom: 2px solid #6477b9;
    -webkit-transform: scale3d(0, 1, 1);
    transform: scale3d(0, 1, 1);
  }
  .center::after {
    border-left: 2px solid #6477b9;
    border-right: 2px solid #6477b9;
    -webkit-transform: scale3d(1, 0, 1);
    transform: scale3d(1, 0, 1);
  }
  .center:hover::before,
  .center:hover::after {
    -webkit-transform: scale3d(1, 1, 1);
    transform: scale3d(1, 1, 1);
    -webkit-transition: -webkit-transform 0.5s;
    transition: transform 0.5s;
  }

  .spin {
    width: 6em;
    height: 6em;
    padding: 0;
  }
  .spin:hover {
    color: #0eb7da;
  }
  .spin::before,
  .spin::after {
    top: 0;
    left: 0;
  }
  .spin::before {
    border: 2px solid transparent;
  }
  .spin:hover::before {
    border-top-color: #0eb7da;
    border-right-color: #0eb7da;
    border-bottom-color: #0eb7da;
    -webkit-transition: border-top-color 0.15s linear,
      border-right-color 0.15s linear 0.1s,
      border-bottom-color 0.15s linear 0.2s;
    transition: border-top-color 0.15s linear,
      border-right-color 0.15s linear 0.1s,
      border-bottom-color 0.15s linear 0.2s;
  }
  .spin::after {
    border: 0 solid transparent;
  }
  .spin:hover::after {
    border-top: 2px solid #0eb7da;
    border-left-width: 2px;
    border-right-width: 2px;
    -webkit-transform: rotate(270deg);
    -ms-transform: rotate(270deg);
    transform: rotate(270deg);
    -webkit-transition: -webkit-transform 0.4s linear 0s,
      border-left-width 0s linear 0.35s;
    transition: transform 0.4s linear 0s, border-left-width 0s linear 0.35s;
  }

  .circle {
    border-radius: 100%;
    box-shadow: none;
  }
  .circle::before,
  .circle::after {
    border-radius: 100%;
  }

  .thick {
    color: #f45e61;
  }
  .thick:hover {
    color: #fff;
    font-weight: 700;
  }
  .thick::before {
    border: 3em solid transparent;
    z-index: -1;
  }
  .thick::after {
    mix-blend-mode: color-dodge;
    z-index: -1;
  }
  .thick:hover::before {
    background: #f45e61;
    border-top-color: #f45e61;
    border-right-color: #f45e61;
    border-bottom-color: #f45e61;
    -webkit-transition: background 0s linear 0.4s, border-top-color 0.15s linear,
      border-right-color 0.15s linear 0.15s,
      border-bottom-color 0.15s linear 0.25s;
    transition: background 0s linear 0.4s, border-top-color 0.15s linear,
      border-right-color 0.15s linear 0.15s,
      border-bottom-color 0.15s linear 0.25s;
  }
  .thick:hover::after {
    border-top: 3em solid #f45e61;
    border-left-width: 3em;
    border-right-width: 3em;
  }
}
</style>