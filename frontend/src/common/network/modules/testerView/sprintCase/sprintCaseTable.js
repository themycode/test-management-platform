import axios from "../../../axios";

// 获取迭代测试集下的测试用例
export const getSuiteCases = params => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcases",
    method: "get",
    params
  });
};

// 批量导入测试用例
export const importTestCases = data => {
  return axios.request({
    url: "/api/v1/product/{productId}/testcases",
    method: "post",
    data: data,
    headers: { "Content-type": "multipart/form-data" }
  });
};

//批量修改测试用例
export const batachUpdateTestCases = data => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcases",
    method: "patch",
    data
  })
}

// 导出用例(Excel)
export const exportTestCases = params => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcases/export/excel",
    method: "get",
    params,
    responseType: "blob"
  });
};

// 导出用例(XMind)
export const exportXmindTestCases = params => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcases/export/xmind",
    method: "get",
    params,
    responseType: "blob"
  });
};

// 批量删除测试用例
export const deleteTestCases = data => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcases",
    method: "delete",
    data
  });
};

// 逐条删除测试用例
export const deleteTestCase = data => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcase/{caseId}",
    method: "delete",
    data
  });
};

// 复制用例到迭代
export const copyCaseToSprintDlg = data => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testcases/bycopy",
    method: "post",
    data
  });
};
