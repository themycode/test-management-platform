import axios from "../../axios";

// 获取项目 table列表数据
export const getProjects = params => {
  return axios.request({
    url: "/api/v1/api-projects",
    method: "get",
    params
  });
};


// 新增项目
export const addProject = data => {
  return axios.request({
    url: "/api/v1/api-project",
    method: "post",
    data
  });
};

// 修改项目
export const updateProject = data => {
  return axios.request({
    url: "/api/v1/api-project/{id}",
    method: "patch",
    data
  });
};

// 添加项目到个人收藏夹
export const addProjectToFavorites = data => {
  return axios.request({
    url: "/api/v1/favourites/api-project/{projectId}",
    method: "post",
    data
  });
};

// 把项目从个人收藏夹中移除
export const removeProjectFromFavorites = data => {
  return axios.request({
    url: "/api/v1/favourites/api-project/{projectId}",
    method: "delete",
    data
  });
};

// 逐条删除项目
export const deleteProject = data => {
  return axios.request({
    url: "/api/v1/api-project/{id}",
    method: "delete",
    data
  });
};

// 批量删除项目
export const deleteProjects = data => {
  return axios.request({
    url: "/api/v1/api-projects",
    method: "delete",
    data
  });
};
