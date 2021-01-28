import axios from "../../axios"

// 获取用户
export const getSysUsers = params => {
  return axios.request({
    url: "/api/v1/sys-users",
    method: "get",
    params
  })
}

// 新增用户
// 参数: 用户相关信息
export const addSysUser = data => {
  return axios.request({
    url: "/api/v1/sys-user",
    method: "post",
    data
  })
}

// 修改用户
// 参数: 用户相关信息
export const updateSysUser = data => {
  return axios.request({
    url: "/api/v1/sys-user/{id}",
    method: "patch",
    data
  })
}

// 查询指定用户的信息
export const getSysUserInfo = params => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}",
    method: "get",
    params
  })
}

// 查询当前登录用户个人信息
export const getCurrentUserInfo = params => {
  return axios.request({
    url: "/api/v1/sys-user/userinfo",
    method: "get",
    params
  })
}

// 禁用、启用用户
// 参数：用户ID，用户目标状态
export const toggleUserStatus = data => {
  return axios.request({
    url: "/api/v1/sys-user/{id}",
    method: "patch",
    data
  })
}

// 逐个删除用户
export const deleteSysUser = data => {
  return axios.request({
    url: "/api/v1/sys-user/{id}",
    method: "delete",
    data
  })
}

// 批量删除用户
export const deleteSysUsers = data => {
  return axios.request({
    url: "/api/v1/sys-users",
    method: "delete",
    data
  })
}

// 获取用户未关联的组别
export const getUnRelatedGroups = params => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/unrelated-groups",
    method: "get",
    params
  })
}

// 关联组别
export const bindGroups = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/groups",
    method: "post",
    data
  })
}

// 取消关联组别
export const deleteRelatedGroup = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/group/{groupId}",
    method: "delete",
    data
  })
}

// 获取用户未关联的角色
export const getUnRelatedRoles = params => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/unrelated-roles",
    method: "get",
    params
  })
}

// 批量关联角色
export const bindRoles = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/roles",
    method: "post",
    data
  })
}

// 取消关联角色
export const deleteRelatedRole = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/role/{roleId}",
    method: "delete",
    data
  })
}

// 获取用户关联账号
export const getRelatedAccounts = params => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/accounts",
    method: "get",
    params
  })
}

// 新增关联账号
export const addRelatedAccount = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/account",
    method: "post",
    data
  })
}

// 修改关联账号
export const updateRelatedAccount = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/account/{accountId}",
    method: "patch",
    data
  })
}

// 删除关联账号
export const deleteRelatedAccount = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/account/{accountId}",
    method: "delete",
    data
  })
}

// 获取用户关联的菜单资源
export const getUserMenus = async params => {
  return await axios.request({
    url: "/api/v1/user/menus",
    method: "get",
    params
  })
}

// 获取用户关联的组别
export const getUserGroupsDetails = params => {
  return axios.request({
    url: "/api/v1/user/groups/details",
    method: "get",
    params
  })
}

// 修改系统用户密码
export const modifyPasswd = data => {
  return axios.request({
    url: "/api/v1/sys-user/passwd",
    method: "put",
    data
  })
}

// 重置密码
export const resetPasswd = data => {
  return axios.request({
    url: "/api/v1/sys-user/{userId}/passwd",
    method: "post",
    data
  })
}

// 批量获取用户指定字段信息
export const getUsersDetails = params => {
  return axios.request({
    url: "/api/v1/users/details",
    method: "get",
    params
  })
}
