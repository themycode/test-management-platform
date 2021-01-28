import axios from "../../axios";

// 获取项目环境配置数据
export const getProjectEnvs = params => {
  return axios.request({
    url: "/api/v1/project-envs",
    method: "get",
    params
  });
};

// 新增项目环境配置
export const addProjectEnv = data => {
  return axios.request({
    url: "/api/v1/project-env",
    method: "post",
    data
  });
};

// 修改项目环境配置
export const updateProjectEnv = data => {
  return axios.request({
    url: "/api/v1/project-env/{envId}",
    method: "patch",
    data
  });
};

// 删除项目环境配置
export const deleteProjectEnv = data => {
  return axios.request({
    url: "/api/v1/project-env/{envId}",
    method: "delete",
    data
  });
};
