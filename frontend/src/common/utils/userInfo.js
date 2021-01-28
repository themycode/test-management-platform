import api from "@/common/network/api"

// 获取当前登录用户个人信息
export const getCurrentUserInfo = (resolve, reject) => {
  api.sysUser
    .getCurrentUserInfo()
    .then(res => {
      if (res.success) {
        resolve(res)
      } else {
        reject(res)
      }
    })
    .catch(res => {
      reject(res)
    })
}
