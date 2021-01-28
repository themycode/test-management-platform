import axios from "../../axios";

// 获取API项目分类
export const getAPIProjectGroupTree = params => {
  return axios.request({
    url: "/api/v1/api-project-group-tree",
    method: "get",
    params
  });
};

// 新增项目分类
export const addAPIProjectGroup = data => {
  return axios.request({
    url: "/api/v1/api-project-group",
    method: "post",
    data
  });
};

// 更新项目分类
export const updateAPIProjectGroup = data => {
  return axios.request({
    url: "/api/v1/api-project-group/{groupId}",
    method: "patch",
    data
  });
};

// 删除项目分类
export const deleteAPIProjectGroup = data => {
  return axios.request({
    url: "api/v1/api-project-group/{id}",
    method: "delete",
    data
  });
}


// 黏贴剪切的项目到项目分类下
export const pasteProjectsCut = data => {
  return axios.request({
    url: "/api/v1/api-project-group/{groupId}/projects-cut",
    method: "post",
    data
  })
}


// 按字段批量获取API项目分类明细信息
export const getAPIProjectGroupsDetails = params => {
  return axios.request({
    url: "/api/v1/api-project-groups-details",
    method: "get",
    params
  });
};


// 按指定字段批量获取项目分类关联的API项目信息
export const getAPIProjectsDetails = params => {
  return axios.request({
    url: "/api/v1/api-project-group/{projectGroupId}/api-projects/details",
    method: "get",
    params
  });
}