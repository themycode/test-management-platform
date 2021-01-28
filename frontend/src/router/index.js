import Vue from "vue";
import Router from "vue-router";

import store from "@/store";
import Index from "@/views/Index";
import { getIFramePath, getIFrameUrl } from "@/common/utils/iframe";
import api from "@/common/network/api";
import Login from "@/views/Login";
import NotFound from "@/views/Error/404";
// import planCaseDetail from "@/common/components/TesterView/sprintTestPlan/planCaseDetail";

import { Message } from "element-ui";

import Cookies from "js-cookie";

Vue.use(Router);

// 静态路由
const staticRoute = [
  {
    path: "/",
    name: "Index",
    component: Index
  },

  {
    path: "/login",
    name: "登录",
    component: Login
  },
//   {
//     path: "/view/plan/testCase/detail",
//     name: "计划用例详情",
//     component: planCaseDetail
//   },
  {
    path: "/error/404",
    name: "notFound",
    component: NotFound
  }
];

const router = new Router({
  mode: "history", //  去掉 http://localhost:8080/#的#
  routes: staticRoute
});

router.beforeEach((to, from, next) => {
  //   let userId = sessionStorage.getItem("userId") // 登录界面登录成功之后，会把用户信息保存在会话 // 关闭浏览器tab标签页，重新打开一个tab页，重新访问该站点，这时会开启一个新的会话，原先登录后保存的userId丢失
  let token = Cookies.get("token"); // 仅登录情况才存在token

  if (to.path === "/login") {
    // 如果是访问登录界面，如果token存在，代表已登录过，跳转到主页
    if (token) {
      next({ path: "/" });
    } else {
      // 否则，跳转到登录页面
      next();
    }
  } else {
    if (to.meta.requireAuth) {
      // 如果访问非登录界面,且路由需要登录
      if (!token) {
        // 用户token不存在，代表未登录，跳转登录
        next({
          path: "/login",
          query: { redirect: to.fullPath } // 把要跳转的路由path作为参数，登录成功后跳转到该路由
        });
      } else {
        // 用户已登录，添加动态菜单和路由后直接跳转
        addDynamicMenuAndRoutes(to, from, next);
      }
    } else {
      // 不需要登录，添加动态菜单和路由后，直接跳转
      addDynamicMenuAndRoutes(to, from, next);
    }
  }
});

/**
 * 加载动态菜单和路由
 */
function addDynamicMenuAndRoutes(to, from, next) {
  // 设置IFrame view视图组件即将访问的url
  // 因为IFrame组件公用，只有一个，但是访问url有多个，所以需要先设置IFrame组件的访问url，不然页面跳转
  // 时，可能跳到错误的页面，调用getDynamicRoutes获取动态路由时，也会设置iframe组件的url访问，但是
  // 动态菜单和路由已经加载的情况下，不会执行getDynamicRoutes函数，所以getMenu前需要优先进行处理

  let path = getIFramePath(to.path);
  if (path) {
    // 如果是iframe页面
    let url = getIFrameUrl(menuList[i].url);
    store.commit("setIFrameUrl", url);
  }

  if (store.state.app.menuRouteLoaded) {
    console.log("动态菜单和路由已经存在.");
    next();
    return;
  }

  //优先从vuex读取
  let navMenuData = store.state.menu.navMenuData;
  if (navMenuData != undefined) {
    // 获取动态路由
    let dynamicRoutes = getDynamicRoutes(navMenuData);

    // 设置获取的路由全部为根路由(path值为 "/")下的子路由
    // 这里，根据静态路由配置可知router.options.routes[0]为根路由
   
    router.options.routes[0].children = [].concat(dynamicRoutes);
    if (router.options.routes[router.options.routes.length - 1].path != "*") {
      router.options.routes = router.options.routes.concat([
        {
          path: "*",
          name: "notFound",
          component: NotFound
        }
      ]);
      }

    // 添加路由，让路由生效
    router.addRoutes(router.options.routes);

    // 存储导航菜单list数据
    store.commit("setNavMenu", navMenuData);

    // 设置菜单为已加载状态
    store.commit("setMenuRouteLoadStatus", true);

    next();
    if (to.matched.length == 0) {
      router.push(to.path);
    }
  } else {
    // vuex获取不到，从服务器端读取
    api.sysUser
      .getUserMenus()
      .then(res => {
        // 获取动态路由
          let dynamicRoutes = getDynamicRoutes(res.data);

        // 添加路由
          router.options.routes[0].children = [].concat(dynamicRoutes);

        if (
          router.options.routes[router.options.routes.length - 1].path != "*"
        ) {
          router.options.routes = router.options.routes.concat([
            {
              path: "*",
              name: "notFound",
              component: NotFound
            }
          ]);
          }

        router.addRoutes(router.options.routes);

        // 存储导航菜单list数据
        store.commit("setNavMenu", res.data);

        // 设置菜单为已加载状态
        store.commit("setMenuRouteLoadStatus", true);

        next();

        if (to.matched.length == 0) {
          router.push(to.path);
        }
      })
      .catch(res => {
        Message.error(res.msg||res.message);
      });
  }
}

/**
 * 获取动态(菜单)路由配置
 * @param {*} menuList 菜单列表
 * @param {*} routes 递归创建的动态(菜单)路由
 */
function getDynamicRoutes(menuList = [], parentRoute = []) {
  for (var i = 0; i < menuList.length; i++) {
    var route = {}; // 存放路由配置
    if (menuList[i].url && /\S/.test(menuList[i].url)) {
      // url不为空，且包含任何非空白字符
      route = {
        path: menuList[i].url,
        component: null,
        name: menuList[i].name,
        children: [],
        meta: {
          icon: menuList[i].icon,
          index: menuList[i].id,
          requireAuth: menuList[i].requireAuth, // 可选值true、false 添加该字段，表示进入这个路由是需要登录的
          isTopNav: menuList[i].isTopNav, // 标记是否顶部菜单
          topNavIndex: menuList[i].topNavId, // 当前菜单归属的顶部菜单
          topNavUrl: menuList[i].topNavUrl, // 当前菜单归属的顶部菜单
          keepAlive: false,  //标记是否缓存路由对应的页面 false-缓存 true-不缓存
          ifCached:false,   // 标记路由对应页面是否已缓存 
        }
      };

      let path = getIFramePath(menuList[i].url);
      if (path) {
        // 如果是嵌套页面, 通过iframe展示
        route["path"] = path;
        route["component"] = resolve =>
          require([`@/views/IFrame/IFrame`], resolve);
        let url = getIFrameUrl(menuList[i].url);
        // 设置嵌套页面的访问URL
        store.commit("setIFrameUrl", url);
      } else {
        try {
          // 根据菜单URL动态加载vue组件，这里要求vue组件须按照url路径存储
          // 如url="sys/user"，则组件路径应是"@/views/sys/user.vue",否则组件加载不到
          let array = [];
          if (menuList[i].url.startsWith("/")) {
            // 如果url 以 "/"打头，所以要先去掉左侧的 "/"，否则组件路径会出现 @/views//sys/user的情况
            array = menuList[i].url.substring(1).split("/");
          } else {
            array = menuList[i].url.split("/");
          }

          let url = ""; // 存放url对应的组件路径

          // 组件所在目录及组件名称第一个字母大写，所以需要替换
          for (let i = 0; i < array.length; i++) {
            url +=
              array[i].substring(0, 1).toUpperCase() +
              array[i].substring(1) +
              "/";
          }
          url = url.substring(0, url.length - 1); // 去掉最右侧的 '/'
          route["component"] = resolve => require([`@/views/${url}`], resolve);
        } catch (e) {
          console.log("根据菜单URL动态加载vue组件失败：" + e);
        }
      }
      if (menuList[i].children && menuList[i].children.length >= 1) {
        getDynamicRoutes(menuList[i].children, route["children"]);
      }
    } else {
      if (menuList[i].children && menuList[i].children.length >= 1) {
        getDynamicRoutes(menuList[i].children, parentRoute);
      }
    }
    if (JSON.stringify(route) != "{}") {
      parentRoute.push(route);
    }
    }
  return parentRoute;
}


export default router;
