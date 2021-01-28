import axios from "../../axios"

// 获取Env table list数据
export const getEnvs = params => {
  return axios.request({
    url: "/api/v1/envs",
    method: "get",
    params
  })
}

// 批量获取Env详情（部分、全部字段信息）
export const getEnvsDetails = params => {
  return axios.request({
    url: "/api/v1/envs/details",
    method: "get",
    params
  })
}



// 新增Env
export const addEnv = data => {
  return axios.request({
    url: "/api/v1/env",
    method: "post",
    data
  })
}

// 修改Env
export const updateEnv = data => {
  return axios.request({
    url: "/api/v1/env/{id}",
    method: "patch",
    data
  })
}

// 删除Env
export const deleteEnv = data => {
  return axios.request({
    url: "/api/v1/env/{id}",
    method: "delete",
    data
  })
}

// 批量删除Env
// 参数：待删除envId数组
export const deleteEnvs = data => {
  return axios.request({
    url: "/api/v1/envs",
    method: "delete",
    data
  })
}
