export default {
  state: {
    mainTabs: [], // 主入口标签页
    currTabName: "", // 当前标签页名
    allTabsClosed: true // 标记是否所有tab页都关闭了
  },
  mutations: {
    updateMainTabs(state, tabs) {
      state.mainTabs = tabs;
    },
    updateCurrTabName(state, name) {
      state.currTabName = name;
    },
    onAllTabsClosed(state, status) {
      state.allTabsClosed = status;
    }
  }
};
