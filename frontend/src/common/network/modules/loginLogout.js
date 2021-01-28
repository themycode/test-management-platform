import axios from "../axios"

// 登录
export const login = data => {
  return axios.request({
    url: "/api/v1/login",
    method: "post",
    data
  })
}

// 登出
export const logout = () => {
  return axios.request({
    url: "/api/v1/logout",
    method: "post"
  })
}
