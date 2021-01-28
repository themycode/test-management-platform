import axios from "../../axios"

/*
 * 系统管理-系统配置-菜单管理
 */

// 获取系统菜单树
export const getSysMenuTree = params => {
  return axios.request({
    url: "/api/v1/sys-menu-tree",
    method: "get",
    params
  })
}


// 添加系统菜单
export const addSysMenu = data => {
  return axios.request({
    url: "/api/v1/sys-menu",
    method: "post",
    data
  })
}

// 修改系统菜单
export const updateSysMenu = data => {
  return axios.request({
    url: "/api/v1/sys-menu/{id}",
    method: "patch",
    data
  })
}

// 删除系统菜单
export const deleteSysMenu = data => {
  return axios.request({
    url: "/api/v1/sys-menu/{id}",
    method: "delete",
    data
  })
}
