import axios from "../../../axios";

/*
 * 迭代测试报告
 */

// 获取迭代测试统计数据
export const generateSprintTestReportStatistics = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport/statistics",
    method: "post",
    data,
    headers: { "Cache-Control": "no-cache" }
  });
};

// 生成迭代测试报告
export const createSprintTestReport = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testreport",
    method: "post",
    data,
    headers: { "Cache-Control": "no-cache" }
  });
};

// 查看迭代测试报告
export const getSprintTestReport = params => {
  return axios.request({
    url: "/api/v1/sprint/testreport/{reportId}",
    method: "get",
    params,
    headers: { "Cache-Control": "no-cache" }
  });
};

// 修改测试报告
export const updateSprintTestReport = data => {
  return axios.request({
    url: "/api/v1/sprint/testreport/{reportId}",
    method: "patch",
    data
  });
};

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
    url: "/api/v1/sprint/testreport/{reportId}/pdf",
    method: "post",
    data,
    responseType: "blob"
  })
}
