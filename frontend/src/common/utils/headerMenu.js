/**
 * 加载当前顶部导航菜单对应的组件时的初始化函数
 */

import store from "@/store"
import router from "@/router"

export const initMenuComponent = () => {
  const isTopNav = router.history.current.meta.isTopNav
  const index = "" + router.history.current.meta.topNavIndex

  // 获取当前页面归属的顶部导航菜单索引和url
    const menuUrl = router.history.current.meta.topNavUrl

  // 获取访问该页面前的顶部导航菜单索引
  const oldTopNavIndex = sessionStorage.getItem("indexOfTopNavMenuActive")

  if (oldTopNavIndex != index) {
    // 切换页面
    store.commit("updateMainTabs", []) // 关闭所有tab页
    sessionStorage.removeItem("indexOfLeftNavMenuActive") // 移除左侧导航当前选中菜单的索引
    sessionStorage.removeItem("urlOfLeftNavMenuActive") // 移除左侧导航当前选中菜单的url

    // 存储当前顶部导航菜单索引，URL
    store.commit("onSelectTopNavMenu", index)

    sessionStorage.setItem("indexOfTopNavMenuActive", index)
    sessionStorage.setItem("urlOfTopNavMenuActive", menuUrl)

    /* 设置侧边导航栏是否展开还是折叠(如果不添加以下代码，会导致切换顶部导航菜单时，
            不同顶部导航菜单的侧边栏折叠/展开状态不一致，因为需要重新加载的组件)*/
    let navBarCollapsed = JSON.parse(sessionStorage.getItem("navBarCollapsed"))
    if (navBarCollapsed != null && navBarCollapsed != store.state.app.isCollapsed) {
      store.commit("onCollapse")
    }
  }
}
