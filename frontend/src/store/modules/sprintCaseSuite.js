export default {
  state: {
    sprintID: "", // 用户选取的、当前同测试用例套件关联的sprint版本ID
    suiteType: "", //用户点选的、当前测试用例套件类型
    suiteID: -1, // 用户点选的、当前测试用例套件ID
    productID: -1, // 用户点选的、当前测试用例套件关联的产品ID
    parentID: -2, // 用户点选的、当前测试用例套件的父级套件ID
    suitePath: "" // 当前测试用例套件所在路径
  },
  mutations: {
    updateSprintID(state, sprintID) {
      state.sprintID = sprintID;
    },
    updateCurrentSuite(state, suiteInfo) {
      state.suiteType = suiteInfo.suiteType;
      state.suitePath = suiteInfo.suitePath;
      state.suiteID = suiteInfo.suiteID;
      state.productID = suiteInfo.productID;
      state.parentID = suiteInfo.parentID;
    }
  }
};
