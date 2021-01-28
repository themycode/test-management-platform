import axios from "../../../axios";

/*
 * 测试计划
 */

// 获取某个产品关联的测试计划
export const getTestPlans = params => {
  return axios.request({
    url: "/api/v1/product/{productId}/testplans",
    method: "get",
    params
  });
};


// 为某个产品新增测试计划
export const addTestPlan = data => {
  return axios.request({
    url: "/api/v1/product/{productId}/testplan",
    method: "post",
    data
  });
};

// 修改某个产品测试计划
export const updateTestPlan = data => {
  return axios.request({
    url: "/api/v1/product/testplan/{id}",
    method: "patch",
    data
  });
};

// 逐条删除某个产品测试计划
export const deleteTestPlan = data => {
  return axios.request({
    url: "/api/v1/product/testplan/{id}",
    method: "delete",
    data
  });
};


// 获取某个某个产品测试计划的详细信息
export const getTestPlanDetail = params => {
  return axios.request({
    url: "/api/v1/product/testplan/{id}",
    method: "get",
    params
  });
};

// 批量删除某些产品测试计划
export const deleteTestPlans = data => {
  return axios.request({
    url: "/api/v1/product/testplans",
    method: "delete",
    data
  });
};

// 获取测试计划关联的用例guid
export const getTestcasesGuids = params => {
  return axios.request({
    url: "/api/v1/sprintTestplan/{planId}/testcases/guids",
    method: "get",
    params
  });
};

// 为测试计划关联测试用例
export const bindTestCases = data => {
  return axios.request({
    url: "/api/v1/testplan/{planId}/testcases",
    method: "post",
    data
  });
};


