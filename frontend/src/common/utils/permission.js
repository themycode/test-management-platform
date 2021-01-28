import api from "@/common/network/api"
import store from "@/store"

import { Message } from "element-ui"

// 检查用户是否有操作权限
export const hasPermission = async params => {
  let userPerms = store.state.user.userPerms
  let match_result = false

  if (userPerms != undefined) {
    return userPerms.indexOf(params) > -1
  } else {
    await api.common
      .getUserPerms()
      .then(res => {
        if (res.success) {
          store.commit("setUserPerms", res.data)
          match_result = res.data.indexOf(params) > -1
        } else {
          Message.error(res.msg)
          match_result = false
        }
      })
      .catch(res => {
        Message.error(res.msg)
        match_result = false
      })
    return match_result
  }
}
