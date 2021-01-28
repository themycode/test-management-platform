import axios from "../../axios"

// 获取账号
export const getAccounts = params => {
  return axios.request({
    url: "/api/v1/msg-push-accounts",
    method: "get",
    params
  })
}

// 新增账号
export const addAccount = data => {
  return axios.request({
    url: "/api/v1/msg-push-account",
    method: "post",
    data
  })
}

// 修改账号
export const updateAccount = data => {
  return axios.request({
    url: "/api/v1/msg-push-account/{id}",
    method: "patch",
    data
  })
}

// 禁用、启用账号
export const toggleAccountStatus = data => {
  return axios.request({
    url: "/api/v1/msg-push-account/{id}",
    method: "patch",
    data
  })
}

// 删除账号
export const deleteAccount = data => {
  return axios.request({
    url: "/api/v1/msg-push-account/{id}",
    method: "delete",
    data
  })
}

// 批量删除账号
export const deleteAccounts = data => {
  return axios.request({
    url: "/api/v1/msg-push-accounts",
    method: "delete",
    data
  })
}

// 获取账号未关联的组别
export const getUnRelatedGroups = params => {
  return axios.request({
    url: "/api/v1/msg-push-account/{accountId}/unrelated-groups",
    method: "get",
    params
  })
}

// 关联组别
export const bindGroups = data => {
  return axios.request({
    url: "/api/v1/msg-push-account/{accountId}/groups",
    method: "post",
    data
  })
}

// 取消关联组别
export const deleteRelatedGroup = data => {
  return axios.request({
    url: "/api/v1/msg-push-account/{accountId}/group/{groupId}",
    method: "delete",
    data
  })
}
