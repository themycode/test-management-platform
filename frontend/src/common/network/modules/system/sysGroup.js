import axios from "../../axios"

// 获取用户组组
export const getSysGroups = params => {
  return axios.request({
    url: "/api/v1/sys-groups",
    method: "get",
    params
  })
}

// 新增用户组
export const addSysGroup = data => {
  return axios.request({
    url: "/api/v1/sys-group",
    method: "post",
    data
  })
}

// 修改用户组
export const updateSysGroup = data => {
  return axios.request({
    url: "/api/v1/sys-group/{id}",
    method: "patch",
    data
  })
}

// 逐条删除用户组
export const deleteSysGroup = data => {
  return axios.request({
    url: "/api/v1/sys-group/{id}",
    method: "delete",
    data
  })
}

// 批量删除用户组
export const deleteSysGroups = data => {
  return axios.request({
    url: "/api/v1/sys-groups",
    method: "delete",
    data
  })
}

