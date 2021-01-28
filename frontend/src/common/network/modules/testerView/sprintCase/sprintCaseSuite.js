import axios from "../../../axios"

// 获取测试用例套件树
export const getSprintCaseSuiteTree = params => {
  return axios.request({
    url: "/api/v1/testcase-suite-tree",
    method: "get",
    params
  })
}

// 新增测试用例套件
export const addSprintCaseSuite = data => {
  return axios.request({
    url: "/api/v1/testcase-suite",
    method: "post",
    data
  })
}

// 更新测试用例套件
export const updateSprintCaseSuite = data => {
  return axios.request({
    url: "/api/v1/testcase-suite/{suiteId}",
    method: "patch",
    data
  })
}

// 删除测试用例套件
export const deleteSprintCaseSuite = data => {
  return axios.request({
    url: "/api/v1/testcase-suite/{suiteId}",
    method: "delete",
    data
  })
}

// 黏贴拷贝的用例到测试集下
export const pasteTestcasesCopied = data => {
  return axios.request({
    url: "/api/v1/testcase-suite/{suiteId}/testcases-copied",
    method: "post",
    data
  })
}

// 黏贴剪切的用例到测试集下
export const pasteTestcasesCut = data => {
  return axios.request({
    url: "/api/v1/testcase-suite/{suiteId}/testcases-cut",
    method: "post",
    data
  })
}

// 黏贴剪切的测试集到目标测试集下
export const pasteSuiteCut = data => {
  return axios.request({
    url: "/api/v1/paste-suite-cut/{suiteId}",
    method: "post",
    data
  })
}

// 按结构黏贴复制的测试集
export const pasteSuiteByStructure = data => {
  return axios.request({
    url: "/api/v1/paste-suite-by-structure",
    method: "post",
    data
  })
}
