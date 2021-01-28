// 登录接口
// 说明：如果用户属于超级管理组，则需要返回所有组别
export function login() {
  const result = {
    msg: "登录成功",
    success: true,
    data: {
      userId: 1,
      userGroup: [
        { id: 1, group: "订单" },
        { id: 2, group: "结算" },
        { id: 3, group: "询价" },
        { id: 4, group: "App" },
        { id: 5, group: "微信" },
        { id: 6, group: "商家" },
        { id: 7, group: "商品" }
      ],
      perms: ["sys:user:delete"], // 用户权限标识集合，形如 ["sys:user:delete", "sys:user:edit"]
      token: "77ae89be36504adfb5c09ef71409ea0e",
      expireTime: "2018-09-01T16:24:50.473+0000",
      creater: null,
      createTime: null,
      updater: null,
      updateTime: "2018-09-01T04:24:50.473+0000"
    }
  }
  return {
    url: "/api/v1/login",
    method: "post",
    data: result
  }
}

// 登出接口
export function logout() {
  const result = {
    success: true,
    msg: "退出成功"
  }
  return {
    url: "/api/v1/logout",
    type: "post",
    data: result
  }
}
