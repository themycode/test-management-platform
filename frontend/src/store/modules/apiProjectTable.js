export default {
  state: {
    projectsCut: [] // 存放剪切的用例
  },
  mutations: {
    setApiProjectsCut(state, projectsCut) {
      state.projectsCut = projectsCut;
    }
  }
};
