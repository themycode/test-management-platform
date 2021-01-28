export default {
  state: {
    appName: "开思测试管理平台", // 应用名称
    isCollapsed: false, // 导航栏收缩状态//默认展开
    indexOfTopNavMenuActive: "", // 当前顶部导航选中菜单索引，同时也是导航菜单ID
    indexOfLeftNavMenuActive: "", // 当前左侧导航选中菜单索引，同时也是导航菜单ID
    menuRouteLoaded: false // 菜单和路由是否已经加载
  },
  mutations: {
    onCollapse(state) {
      // 改变收缩状态
      state.isCollapsed = !state.isCollapsed;
    },
    onSelectTopNavMenu(state, index) {
      state.indexOfTopNavMenuActive = index;
    },
    onSelectLeftNavMenu(state, index) {
      state.indexOfLeftNavMenuActive = index;
    },
    setMenuRouteLoadStatus(state, menuRouteLoaded) {
      // 改变菜单和路由的加载状态
      state.menuRouteLoaded = menuRouteLoaded;
    },
    setIndexOfTopNavMenuActive(state, index) {
      state.indexOfTopNavMenuActive = index;
    }
  }
};
