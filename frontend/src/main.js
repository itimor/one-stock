import Vue from 'vue'

import 'normalize.css/normalize.css' // a modern alternative to CSS resets

import Element from 'element-ui'
import './styles/element-variables.scss'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import i18n from './lang' // Internationalization
import './icons' // icon
import './permission' // permission control

import * as filters from './filters' // global filters

import watermark from 'vue-watermark-directive'
Vue.use(watermark)

// video播放器
import vueMiniPlayer from 'vue-mini-player'
import 'vue-mini-player/lib/vue-mini-player.css'
Vue.use(vueMiniPlayer)


// 添加原生熟悉 查找 index 和 remove, 需要使用放入 main.js
Array.prototype.indexItem = function (val) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] === val) return i
  }
  return -1
}

Array.prototype.remove = function (val) {
  const index = this.indexItem(val)
  if (index > -1) {
    this.splice(index, 1)
  }
}

Vue.use(Element, {
  i18n: (key, value) => i18n.t(key, value)
})

// register global utility filters
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: h => h(App)
})
