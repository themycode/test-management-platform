export default {
    state: {
        navMenuData: undefined // 导航菜单树
    },
    mutations: {
        setNavMenu(state, navMenuData) {
            // 设置导航菜单list数据（元素为json格式的数据）
            state.navMenuData = navMenuData
        }
    }
}
