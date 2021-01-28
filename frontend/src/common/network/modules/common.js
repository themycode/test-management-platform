import axios from "../axios"

/*
 * 公用模块
 */



/**
 * 获取用户权限标识
 */
 export const getUserPerms = () => {
  return axios.request({
    url: "/api/v1/user-perms",
    method: "get"
  })
}