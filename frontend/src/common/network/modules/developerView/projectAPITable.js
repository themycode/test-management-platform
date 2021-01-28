import axios from "../../axios";

// 获取指定接口分类下的项目接口
export const getProjectAPIs = params => {
  return axios.request({
    url: "api/v1/api-group/{groupId}/project-apis",
    method: "get",
    params
  });
};

// 在指定项目的指定接口分类下新增接口
export const addProjectAPI = data => {
  return axios.request({
    url: "/api/v1/project/{projectId}/group/{groupId}/api",
    method: "post",
    data: data
  });
};

// 更新指定项目的指定接口分类下新增接口
export const updateProjectAPI = data => {
  return axios.request({
    url: "/api/v1/project/{projectId}/group/{groupId}/api",
    method: "patch",
    data: data
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
