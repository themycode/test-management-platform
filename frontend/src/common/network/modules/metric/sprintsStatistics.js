import axios from "../../axios"

/*
 * 项目迭代统计
 */

// 查询项目迭代统计数据
// 迭代测试报告
export const getSprintsStatistics = params => {
  return axios.request({
    url: "/api/v1/sprints/statistics",
    method: "get",
    params
  })
}

// 生成迭代测试报告
export const addSprintTestReport = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport",
    method: "post",
    data
  })
}

// 查看迭代测试报告
export const getSprintTestReport = params => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport/{reportId}",
    method: "get",
    params
  })
}

// 修改测试报告
export const updateSprintTestReport = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport/{reportId}",
    method: "patch",
    data
  })
}

// 获取迭代关联的测试报告列表
export const getSprintTestReportsDetails = params => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreports/details",
    method: "get",
    params
  })
}

// 下载PDF格式测试报告
export const downloadSprintTestReport = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport/{reportId}/pdf",
    method: "post",
    data,
    responseType: "blob"
  })
}
