// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import store from "./store";
import "font-awesome/css/font-awesome.css";
import globalConstant from "./common/constant";
import api from "./common/network/index";
import customUtils from "./common/utils";
import axios from "axios";

import jshint from "jshint";
window.JSHINT = jshint.JSHINT;

import { codemirror } from "vue-codemirror";
import "codemirror/lib/codemirror.css";

// echarts
let echarts = require("echarts/lib/echarts"); // 引入基本模板
require("echarts/lib/chart/pie"); // 引入饼图
require("echarts/lib/chart/bar"); // 引入柱状图
require("echarts/lib/chart/line"); // 引入曲线图

require("echarts/lib/component/title"); // 引入标题组件
require("echarts/lib/component/legend"); // 引入图例组件
require("echarts/lib/component/tooltip"); // 引入提示框组件
require("echarts/lib/component/graphic"); // 引入graphic组件


import App from "./app/App";
import router from "./router"; // 最后引入路由

// require("./mock/index.js") //不用的时候需要删除\注释掉
Vue.use(customUtils);

Vue.use(ElementUI);
Vue.use(api);
Vue.use(codemirror);

Vue.config.productionTip = false;
Vue.prototype.$globalConstant = globalConstant; // 挂载全局变量
Vue.prototype.$echarts = echarts; // 挂载echarts

Vue.directive("focus", {
  // 当被绑定的元素插入到 DOM 中时自动聚焦
  inserted: function(el) {
    // 聚焦元素
    el.focus();
  }
});

// 实时检测浏览器窗口大小变化
// 调用方式 v-resize="自定义处理函数"
Vue.directive("resize", {
  bind(el, binding) {
    let width = "", // 存放元素的width值
      height = ""; // 存放元素的height值
    let id_of_settimeout = null;
    function vueResizeElementHandler(e) {
      if (!binding.expression) {
        // 判断指令是否绑定了函数，如果没有则返回
        return;
      }

      if (id_of_settimeout) {
        // 如果为真，则说明被延迟的js代码还没被执行
        // 取消上次延时未执行的方法
        clearTimeout(id_of_settimeout);
      }

      id_of_settimeout = setTimeout(function() {
        const style = document.defaultView.getComputedStyle(el);
        if (width !== style.width || height !== style.height) {
          width = style.width;
          height = style.height;
          binding.value(width, height);
        }
      }, 300);
    }

    el.__vueResizeElement__ = vueResizeElementHandler;
    window.addEventListener("resize", vueResizeElementHandler);
  },
  unbind(el) {
    window.removeEventListener("onresize", el.__vueResizeElement__);
  }
});

let myConfigPath = "/static/config.js";

if (process.env.NODE_ENV === "development") {
  myConfigPath = "../static/config.js";
}

axios
  .get(myConfigPath, { headers: { "Cache-Control": "no-cache" } })
  .then(response => {
    response = eval(response.data);
    Vue.prototype.$appConfig = response;

    new Vue({
      el: "#app",
      router,
      store, // 注入 store
      components: { App },
      template: "<App/>"
    });
  });
