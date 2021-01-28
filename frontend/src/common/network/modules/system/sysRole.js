import axios from "../../axios"

// 获取角色
export const getSysRoles = params => {
  return axios.request({
    url: "/api/v1/sys-roles",
    method: "get",
    params
  })
}

// 新增角色
export const addSysRole = data => {
  return axios.request({
    url: "/api/v1/sys-role",
    method: "post",
    data
  })
}

// 修改角色
export const updateSysRole = data => {
  return axios.request({
    url: "/api/v1/sys-role/{id}",
    method: "patch",
    data
  })
}


// 逐条删除角色
export const deleteSysRole = data => {
  return axios.request({
    url: "/api/v1/sys-role/{id}",
    method: "delete",
    data
  })
}

// 批量删除角色
export const batchDeleteSysRole = data => {
  return axios.request({
    url: "/api/v1/sys-roles",
    method: "delete",
    data
  })
}

// 获取系统角色关联的菜单id
export const getRoleRelatedMenus = params => {
  return axios.request({
    url: "/api/v1/sys-role/{roleId}/related-menus",
    method: "get",
    params
  })
}

// 关联菜单
export const bindMenu = data => {
  return axios.request({
    url: "/api/v1/sys-role/{roleId}/related-menus",
    method: "post",
    data
  })
}
