import axios from "../../axios";

// 获取项目版本 table列表数据
export const getProjectVersions = params => {
  return axios.request({
    url: "/api/v1/project/{projectId}/versions",
    method: "get",
    params
  });
};

// 按指定字段获取某个项目关联的项目版本信息
export const getVersionsDetailsForProject = params => {
  return axios.request({
    url: "/api/v1/project/{projectId}/versions/details",
    method: "get",
    params
  })
}

// 新增项目版本
export const addProjectVersion = data => {
  return axios.request({
    url: "/api/v1/project/{projectId}/version",
    method: "post",
    data
  });
};

// 修改项目版本
export const updateProjectVersion = data => {
  return axios.request({
    url: "/api/v1/project/version/{id}",
    method: "patch",
    data
  });
};

// 逐条删除项目版本
export const deleteProjectVersion = data => {
  return axios.request({
    url: "/api/v1/project/version/{id}",
    method: "delete",
    data
  })
};

// 批量删除项目版本
export const deleteProjectVersions = data => {
  return axios.request({
    url: "/api/v1/project/versions",
    method: "delete",
    data
  });
};

// 获取某个项目关联的平台项目版本列表
export const getPlatformProjectVersions = params => {
  return axios.request({
    url: "/api/v1/project/{projectId}/project-versions",
    method: "get",
    params
  });
};

// 为某个项目版本关联某个平台项目版本
export const bindPlatformProjectVersion = data => {
  return axios.request({
    url:
      "/api/v1/project-version/{projectVersionId}/platform-project-version/{platformProjectVersionId}",
    method: "post",
    data
  });
};

// 为某个项目版本解除绑定已关联的平台项目版本
export const unbindPlatformProjectVersion = data => {
  return axios.request({
    url: "/api/v1/project-version/{projectVersionId}/platform-project-version",
    method: "delete",
    data
  });
};
