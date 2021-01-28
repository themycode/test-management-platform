import axios from "../../axios"

// 获取某个产的迭代列表数据
export const getSprints = params => {
  return axios.request({
    url: "/api/v1/product/{productId}/sprints",
    method: "get",
    params
  })
}


// 为某个产品新增Sprint
export const addSprint = data => {
  return axios.request({
    url: "/api/v1/product/{productId}/sprint",
    method: "post",
    data
  });
}

// 修改某个产品的某个Sprint
export const updateSprint = data => {
  return axios.request({
    url: "/api/v1/product/{productId}/sprint/{id}",
    method: "patch",
    data
  });
}

// 逐条删除某个产品迭代
export const deleteSprint = data => {
  return axios.request({
    url: "/api/v1/sprint/{id}",
    method: "delete",
    data
  });
}

// 批量删除某些产品迭代
export const deleteSprints = data => {
  return axios.request({
    url: "/api/v1/sprints",
    method: "delete",
    data
  });
}


// 获取某个迭代关联的测试计划
export const getSprintTestPlans = params => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/testplans",
    method: "get",
    params
  });
};


// 获取某个迭代关联的项目及项目版本
export const getRelatedProjectsWithVersions = params => {
  return axios.request({
    url: "/api/v1/sprint/{sprintId}/projectsWithVersions",
    method: "get",
    params
  });
};