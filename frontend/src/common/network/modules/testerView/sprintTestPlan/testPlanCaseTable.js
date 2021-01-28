import axios from "../../../axios"

// 获取迭代测试集下的测试用例
export const getSuiteCases = params => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testsuite/{suiteId}/testcases",
    method: "get",
    params
  })
}

// 逐条修改用例测试结果
export const updateCaseTestResult = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcase/{id}/result",
    method: "patch",
    data
  })
}

// 批量修改测试用例结果
export const updateCaseTestResults = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcases/results",
    method: "patch",
    data
  })
}

// 修改测试用例(备注,指派给）
export const updateTestCase = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcase/{id}",
    method: "patch",
    data
  });
}

// 批量修改测试用例
export const updateTestCases = data => {
  return axios.request({
    url: "api/v1/testplan/{planId}/testcases",
    method: "patch",
    data
  })
}

// 逐条删除测试用例
export const deleteTestCase = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcase/{id}",
    method: "delete",
    data
  })
}

// 批量删除测试用例
export const deleteTestCases = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcases",
    method: "delete",
    data
  })
}


