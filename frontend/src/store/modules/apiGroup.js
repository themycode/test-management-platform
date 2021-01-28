export default {
  state: {
    projectID: "", // 用户选取的、当前接口分类关联的项目ID
    groupName: "", // 用户选取的、当前接口分类名称
    groupID: -1, // 用户点选的、当前接口分类id
    parentID: -2 // 用户点选的、当前接口分类的父级分类ID
  },
  mutations: {
    updateProjectID(state, projectID) {
      state.projectID = projectID;
    },
    updateCurrentAPIGroup(state, groupInfo) {
      state.groupID = groupInfo.groupID;
      state.groupName = groupInfo.groupName;
      state.projectID = groupInfo.projectID;
      state.parentID = groupInfo.parentID;
    }
  }
};
