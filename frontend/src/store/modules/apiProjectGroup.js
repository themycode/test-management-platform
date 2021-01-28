export default {
  state: {
    // groupID: "", // 用户选取的、当前同测试用例套件关联的sprint版本ID
    groupType: "", //用户点选的、当前API项目分组类型
    groupID: -1, // 用户点选的、当前API项目分组ID
    groupName: "我的收藏" // 用户点选的、当前API项目分组名称
    // productID: -1, // 用户点选的、当前测试用例套件关联的产品ID
    // parentID: -2, // 用户点选的、当前测试用例套件的父级套件ID
    // suitePath: "" // 当前测试用例套件所在路径
  },
  mutations: {
    // updateAPIProjectGroupID(state, groupID) {
    //   state.groupID = groupID;
    // },
    updateCurrentGroup(state, groupInfo) {
      state.groupType = groupInfo.groupType;
      state.groupID = groupInfo.groupID;
      state.groupName = groupInfo.groupName;
    }
  }
};
