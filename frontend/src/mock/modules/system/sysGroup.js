export function sysGroups() {
  const result = {
    msg: null,
    success: true,
    data: {
      total: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      rows: [
        {
          id: 1, // 数据库自增ID
          name: "订单",
          desc: "订单组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updaterTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          name: "商家",
          desc: "商家组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updaterTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          name: "终端",
          desc: "终端组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "",
          updaterTime: ""
        },
        {
          id: 4,
          name: "终端",
          desc: "终端组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "",
          updaterTime: ""
        },
        {
          id: 5,
          name: "商家",
          desc: "商家组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updaterTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          name: "商家",
          desc: "商家组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updaterTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          name: "商家",
          desc: "商家组描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updaterTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/sys-groups",
    method: "get",
    data: result
  }
}

// 新增系统用户组
export function addSysGroup() {
  const result = {
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      name: "新增组",
      desc: "商家组描述",
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      updater: "",
      updaterTime: ""
    }
  }
  return {
    url: "/api/v1/sys-group",
    method: "post",
    data: result
  }
}

// 修改系统用户组
export function updateSysGroup() {
  const result = {
    msg: "修改成功",
    success: true,
    data: {
      name: "修改后的组",
      desc: "商家组描述",
      updater: "上官晓晓",
      updaterTime: "2019-06-04 09:15:59"
    }
  }
  return {
    url: "/api/v1/sys-group",
    method: "patch",
    data: result
  }
}

// 删除系统用户组
export function deleteSysGroup() {
  const result = {
    success: true,
    msg: "删除成功"
  }
  return {
    url: "/api/v1/sys-group",
    type: "delete",
    data: result
  }
}
