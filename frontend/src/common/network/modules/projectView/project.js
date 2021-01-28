import axios from "../../axios";

// 获取项目 table列表数据
export const getProjects = params => {
  return axios.request({
    url: "/api/v1/projects",
    method: "get",
    params
  });
};

// 按指定字段批量获取项目详细信息
export const getProjectsDetails = params => {
  return axios.request({
    url: "/api/v1/projects/details",
    method: "get",
    params
  });
};

// 新增项目
export const addProject = data => {
  return axios.request({
    url: "/api/v1/project",
    method: "post",
    data
  });
};

// 修改项目
export const updateProject = data => {
  return axios.request({
    url: "/api/v1/project/{id}",
    method: "patch",
    data
  });
};

// 逐条删除项目
export const deleteProject = data => {
  return axios.request({
    url: "/api/v1/project/{id}",
    method: "delete",
    data
  });
};

// 批量删除项目
export const deleteProjects = data => {
  return axios.request({
    url: "/api/v1/projects",
    method: "delete",
    data
  });
};

// 按指定字段获取某个产品关联的项目信息
export const getProductProjectsDetails = params => {
  return axios.request({
    url: "/api/v1/product/{productId}/projects/details",
    method: "get",
    params
  });
};

// 获取某个平台关联的项目
export const getPlatformProjects = params => {
  return axios.request({
    url: "/api/v1/platform/{platform}/projects",
    method: "get",
    params
  });
};

// 获取项目系统自定义字段列表
export const getSystomFieldsOptions = () => {
  return axios.request({
    url: "/api/v1/project/system/fields",
    method: "get"
  });
};

// 获取jira问题类型列表
export const getJiraIssueTypes = params => {
  return axios.request({
    url: "/api/v1/jira/issue-types",
    method: "get",
    params
  });
};

// 获取jira问题自定义字段列表
export const getJiraIssueCustomFields = params => {
  return axios.request({
    url: "/api/v1/jira/issue-custom-fields",
    method: "get",
    params
  });
};

// 获取jira问题自定义字段列表
export const getZentaoDefectCustomFields = params => {
  return axios.request({
    url: "/api/v1/zentao/defect-custom-fields",
    method: "get",
    params
  });
};

// 为某个项目绑定某个平台的某个项目
export const bindPlatformProject = data => {
  return axios.request({
    url:
      "/api/v1/project/{projectId}/platform/{platform}/platform-project/{platformProjectId}",
    method: "post",
    data
  });
};

// 为某个项目解除绑定已关联的平台项目
export const unbindPlatformProject = data => {
  return axios.request({
    url: "/api/v1/project/{projectId}/platform-project",
    method: "delete",
    data
  });
};
