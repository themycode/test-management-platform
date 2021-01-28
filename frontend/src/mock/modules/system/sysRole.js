export function sysRoles() {
  const result = {
    msg: null,
    success: true,
    data: {
      total: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      rows: [
        {
          id: 1, // 数据库自增ID
          name: "角色名称1",
          desc: "角色描述1",
          isActive: true, // 是否启用
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          name: "角色名称2",
          desc: "角色描述2",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 4,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 5,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: 0,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 8,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        },
        {
          id: 9,
          name: "角色名称3",
          desc: "角色描述3",
          isActive: true,
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          updater: "上官晓晓",
          updateTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/sys-roles",
    method: "get",
    data: result
  }
}

// 新增系统角色
export function addSysRole() {
  const result = {
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      name: "角色名称3",
      desc: "角色描述3",
      isActive: true,
      creater: "上官晓晓",
      createTime: "2019-05-28 09:14:59",
      updater: "上官晓晓",
      updateTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/sys-role",
    method: "post",
    data: result
  }
}

// 修改系统角色
export function updateSysRole() {
  const result = {
    msg: "操作成功",
    success: true,
    data: {
      name: "修改后的角色名称",
      desc: "修改后的角色描述",
      isActive: true,
      updater: "上官晓晓",
      updateTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/sys-role/{roleId}",
    method: "patch",
    data: result
  }
}


// 逐条删除角色
export function deleteSysRole() {
  const result = {
    success: true,
    msg: "删除成功"
  }
  return {
    url: "/api/v1/sys-role/{roleId}",
    type: "delete",
    data: result
  }
}

// 批量删除角色
export function batchDeleteSysRole() {
  const result = {
    success: true,
    msg: "删除成功"
  }
  return {
    url: "/api/v1/sys-roles",
    type: "delete",
    data: result
  }
}

// 获取角色关联的菜单(id)
export function roleRelatedMenus() {
  const result = {
    success: true,
    msg: "获取成功",
    data: [1, 4]
  }
  return {
    url: "/api/v1/sys-role/{roleId}/related-menus",
    type: "get",
    data: result
  }
}

// 关联菜单资源
export function bindMenu() {
  const result = {
    success: true,
    msg: "关联成功"
  }
  return {
    url: "/api/v1/sys-role/{roleId}/related-menus",
    type: "post",
    data: result
  }
}
