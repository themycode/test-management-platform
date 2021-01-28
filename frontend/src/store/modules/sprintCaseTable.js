export default {
  state: {
    testcasesCopied: [], // 存放拷贝的用例
    testcasesCut: [] // 存放剪切的用例
  },
  mutations: {
    setTestcasesCopied(state, testcasesCopied) {
      state.testcasesCopied = testcasesCopied
    },
    setTestcasesCut(state, testcasesCut) {
      state.testcasesCut = testcasesCut
    }
  }
}
