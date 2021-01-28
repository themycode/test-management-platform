export default {
  state: {
    userId: undefined, // 用户id
    userName: "", // 用户姓名
    userPerms: undefined, // 用户权限标识集合
    isSuperuser: undefined, // 是否超级用户标识
    userGroups: undefined // 用户所属组别
  },
  mutations: {
    setUserPerms(state, userPerms) {
      state.userPerms = userPerms
    },
    setIsSuperUser(state, isSuperuser) {
      state.isSuperuser = isSuperuser
    },
    setUserId(state, userId) {
      state.userId = userId
    },
    setUserName(state, userName) {
      state.userName = userName
    },
    setUserGroups(state, userGroups) {
      state.userGroups = userGroups
    }
  }
}
