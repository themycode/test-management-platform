import axios from "../../axios";

// 获取测试阶段 table list数据
export const getTestPhases = params => {
  return axios.request({
    url: "/api/v1/test-phases",
    method: "get",
    params
  });
};

// 批量获取测试阶段详情（部分、全部字段信息）
export const getTestPhasesDetails = params => {
  return axios.request({
    url: "/api/v1/test-phases/details",
    method: "get",
    params
  });
};

// 新增测试阶段
export const addTestPhase = data => {
  return axios.request({
    url: "/api/v1/test-phase",
    method: "post",
    data
  });
};

// 修改测试阶段
export const updateTestPhase = data => {
  return axios.request({
    url: "/api/v1/test-phase/{id}",
    method: "patch",
    data
  });
};

// 删除测试阶段
export const deleteTestPhase = data => {
  return axios.request({
    url: "/api/v1/test-phase/{id}",
    method: "delete",
    data
  });
};

// 批量删除测试阶段
// 参数：待删除测试阶段数组
export const deleteTestPhases = data => {
  return axios.request({
    url: "/api/v1/test-phases",
    method: "delete",
    data
  });
};
