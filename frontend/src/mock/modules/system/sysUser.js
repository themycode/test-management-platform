export function sysUsers() {
  const result = {
    msg: null,
    success: true,
    data: {
      total: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      rows: [
        {
          id: 1, // 数据库自增ID
          account: "fuyu.lai@casstime.com",
          name: "赖小小", // 真实姓名
          email: "fuyu.lai@casstime.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          account: "account2",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          account: "account3",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [], // 所属角色
          groups: [], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 4,
          account: "account4",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 5,
          account: "account5",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          account: "account6",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          account: "account7",
          name: "赖晓晓", // 真实姓名
          email: "103351@qq.com",
          mobile: "17817733125",
          roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          desc: "用户描述1",
          isActive: true, // 是否启用
          lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/sys-users",
    method: "get",
    data: result
  }
}

// 新增系统用户
export function addSysUser() {
  const result = {
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      account: "account10",
      name: "赖晓晓", // 真实姓名
      email: "103351@qq.com",
      mobile: "17817733125",
      roles: [{ id: 1, name: "角色1" }, { id: 2, name: "角色2" }, { id: 3, name: "角色2" }], // 所属角色
      groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
      desc: "用户描述1",
      isActive: true, // 是否启用
      lastLoginTime: "2019-05-28 09:14:59", // 上次登陆时间
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      updater: "上官晓晓",
      updateTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/sys-user",
    method: "post",
    data: result
  }
}

// 修改系统用户
export function updateSysUser() {
  const result = {
    msg: "修改成功",
    success: true,
    data: {
      account: "xiugaihou",
      name: "修改后的", // 真实姓名
      email: "103351@qq.com",
      mobile: "17817733125",
      desc: "用户描述1",
      isActive: true, // 是否启用
      updater: "上官晓晓",
      updateTime: "2019-06-04 09:15:59"
    }
  }
  return {
    url: "/api/v1/sys-user/{userId}",
    method: "patch",
    data: result
  }
}

// 删除系统用户
export function deleteSysUser() {
  const result = {
    success: true,
    msg: "删除成功",
  }
  return {
    url: "/api/v1/sys-user/{userId}",
    type: "delete",
    data: result
  }
}

// 获取用户未关联的组别
export function unRelatedGroups() {
  const result = {
    success: true,
    msg: "获取成功",
    data: [{ id: 4, name: "组别4" }, { id: 5, name: "组别5" }, { id: 6, name: "组别6" }]
  }
  return {
    url: "/api/v1/sys-user/unrelated-groups",
    type: "get",
    data: result
  }
}

// 批量关联组别
export function bindGroups() {
  const result = {
    success: true,
    msg: "绑定成功",
  }
  return {
    url: "/api/v1/sys-user/{userId}/groups",
    type: "post",
    data: result
  }
}

// 取消关联组别
export function deleteRelatedGroup() {
  const result = {
    success: true,
    msg: "操作成功",
  }
  return {
    url: "/api/v1/sys-user/{userId}/group",
    method: "delete",
    data: result
  }
}

// 获取用户未关联的角色
export function unRelatedRoles() {
  const result = {
    success: true,
    msg: "获取成功",
    data: [{ id: 4, name: "角色4" }, { id: 5, name: "角色5" }, { id: 6, name: "角色6" }]
  }
  return {
    url: "/api/v1/sys-user/{userId}/unrelated-roles",
    type: "get",
    data: result
  }
}

// 批量关联角色
export function bindRoles() {
  const result = {
    success: true,
    msg: "绑定成功",
  }
  return {
    url: "/api/v1/sys-user/{userId}/roles",
    type: "post",
    data: result
  }
}

// 取消关联角色
export function deleteRelatedRole() {
  const result = {
    success: true,
    msg: "操作成功",
  }
  return {
    url: "/api/v1/sys-user/{userId}/role",
    method: "delete",
    data: result
  }
}

// // 启用/禁用用户
// export function toggleUserStatus() {
//   const result = {
//     success: true,
//     msg: "操作成功",
//   }
//   return {
//     url: "/api/v1/sys-user/{id}",
//     type: "patch",
//     data: result
//   }
// }

// 获取用户关联账号
export function relatedAccounts() {
  const result = {
    msg: null,
    success: true,
    data: [
      {
        id: 1, // 数据库自增ID
        account: "fuyu.lai@casstime.com",
        platform: "tapd",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 2,
        account: "fuyu.lai@casstime.com",
        platform: "禅道",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 3,
        account: "fuyu.lai@casstime.com",
        platform: "禅道",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 4,
        account: "fuyu.lai@casstime.com",
        platform: "禅道",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 5,
        account: "account5",
        account: "fuyu.lai@casstime.com",
        platform: "禅道",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 6,
        account: "fuyu.lai@casstime.com",
        platform: "禅道",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      },
      {
        id: 7,
        account: "fuyu.lai@casstime.com",
        platform: "禅道1234567890125555",
        creater: "赖某人",
        createTime: "2019-05-28 09:14:59",
        updater: "上官晓晓",
        updateTime: "2019-06-04 09:14:59"
      }
    ]
  }
  return {
    url: "/api/v1/sys-user/relatedAccounts",
    method: "get",
    data: result
  }
}

// 新增关联账号
export function addRelatedAccount() {
  const result = {
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      account: "新增的账号",
      platform: "禅道", // 真实姓名
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      updater: "",
      updateTime: ""
    }
  }
  return {
    url: "/api/v1/sys-user/relatedAccount/add",
    method: "post",
    data: result
  }
}

// 修改关联账号
export function updateRelatedAccount() {
  const result = {
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sys-user/relatedAccount/update",
    method: "post",
    data: result
  }
}

// 删除关联账号
export function deleteRelatedAccount() {
  const result = {
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/sys-user/relatedAccount/delete",
    type: "post",
    data: result
  }
}
