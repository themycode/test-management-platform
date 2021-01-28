// 表格数据
export function accounts() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: {
      totalRows: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      accountList: [
        {
          id: 1, // 数据库自增ID
          account: "fuyu.lai@casstime.com",
          type: "邮箱号",
          desc: "fuyu.lai@casstime.com",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用", // 是否启用
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          account: "fuyulai@casstime.com",
          type: "邮箱号",
          desc: "fuyu.lai@casstime.com",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用", // 是否启用
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          account: "17817738178",
          type: "手机号",
          desc: "账号描述",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 4,
          account: "13817738118",
          type: "钉钉号",
          desc: "账号描述",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 5,
          account: "13817738118",
          type: "手机号",
          desc: "账号描述",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          account: "13817738118",
          type: "手机号",
          desc: "账号描述",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          account: "13817738118",
          type: "手机号",
          desc: "账号描述",
          groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
          status: "启用",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/system/msgPush/accounts",
    method: "get",
    data: result
  }
}

// 新增账号
export function addAccount() {
  const result = {
    code: 200,
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      account: "xinzengzhanghao",
      type: "手机号",
      desc: "账号描述",
      groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
      status: "启用",
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/msgPush/account/add",
    method: "post",
    data: result
  }
}

// 修改账号
export function updateAccount() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {
      account: "xiugaihou",
      type: "手机号",
      desc: "账号描述",
      groups: [{ id: 1, name: "组别1" }, { id: 2, name: "组别2" }, { id: 3, name: "组别3" }], // 所属组别
      status: "禁用",
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/msgPush/account/update",
    method: "post",
    data: result
  }
}

// 删除账号
export function deleteAccount() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/system/msgPush/account/delete",
    type: "post",
    data: result
  }
}

// 获取账号未关联的组别
export function unRelatedGroups() {
  const result = {
    code: 200,
    success: true,
    msg: "获取成功",
    data: [{ id: 4, name: "组别4" }, { id: 5, name: "组别5" }, { id: 6, name: "组别6" }]
  }
  return {
    url: "/api/v1/system/msgPush/account/unRelatedGroups",
    type: "get",
    data: result
  }
}

// 关联组别
export function bindGroups() {
  const result = {
    code: 200,
    success: true,
    msg: "绑定成功",
    data: {}
  }
  return {
    url: "/api/v1/system/msgPush/account/bindGroups",
    type: "post",
    data: result
  }
}

// 取消关联组别
export function deleteRelatedGroup() {
  const result = {
    code: 200,
    success: true,
    msg: "操作成功",
    data: {}
  }
  return {
    url: "/api/v1/system/msgPush/account/relatedGroup/delete",
    method: "post",
    data: result
  }
}


// 启用/禁用账号
export function toggleAccountStatus() {
  const result = {
    code: 200,
    success: true,
    msg: "操作成功",
    data: {}
  }
  return {
    url: "/api/v1/system/msgPush/account/status/toggle",
    type: "post",
    data: result
  }
}
