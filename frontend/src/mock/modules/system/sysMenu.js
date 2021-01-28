// 获取系统菜单
export function sysMenuTree() {
  const result = {
    success: true,
    msg: "获取成功",
    data: [
      {
        id: 0,
        creater: "admin", // 创建人
        createTime: "2019-07-02 11:53:53", // 创建时间
        updater: "", // 修改人
        updateTime: "", // 修改时间
        parentId: -1, // 上级ID，0表示上级ID为根节点， -1 表示不存在上级ID
        name: "根节点", // 资源名称
        url: "", // 资源URL
        perms: "", // 权限标识
        requireAuth: false, // 是否需要登录 flase-不需要 true 需要
        type: "菜单", // 资源类型 可选值 菜单 目录 按钮
        icon: "", // 图标
        order: 1, // 顺序
        desc: "", // 描述信息
        collapsed: true, // 是否展开
        show: true, // 是否显示
        children: [
          {
            id: 1,
            creater: "admin",
            createTime: "2019-07-02 11:53:53",
            updater: "",
            updateTime: "",
            parentId: 0,
            name: "首页",
            url: "/home",
            perms: "",
            requireAuth: false,
            type: "菜单",
            icon: "fa fa-home fa-lg", // 图标
            order: 1,
            desc: "描述",
            collapsed: false,
            show: true,
            children: []
          },
          {
            id: 2,
            creater: "admin",
            createTime: "2019-07-02 11:53:53",
            updater: "",
            updateTime: "",
            parentId: 0,
            name: "工作台",
            url: "/workbench",
            perms: "",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 1,
            desc: "描述",
            collapsed: false,
            show: true,
            children: []
          },
          {
            id: 3,
            creater: "admin",
            createTime: "2019-07-02 11:53:53",
            updater: "",
            updateTime: "",
            parentId: 0,
            name: "测试视图",
            url: "/testerView",
            perms: "",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 1,
            desc: "描述",
            collapsed: false,
            show: true,
            children: [
              {
                id: 4,
                creater: "admin",
                createTime: "2019-07-02 11:53:53",
                updater: "",
                updateTime: "",
                parentId: 0,
                name: "用例管理",
                url: "/testerView/testCaseManagement",
                perms: "",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 1,
                desc: "描述",
                collapsed: false,
                show: true,
                children: []
              }
            ]
          }
        ]
      }
    ]
  }

  return {
    url: "/api/v1/sys-menu-tree",
    type: "get",
    data: result
  }
}
// 获取子系统菜单
export function sysSubMenus() {
  const result = {
    success: true,
    msg: null,
    data: [
      {
        id: 1,
        creater: "admin",
        createTime: "2019-07-02 11:53:53",
        updater: "",
        updateTime: "",
        parentId: 0,
        name: "首页",
        url: "/home",
        perms: "",
        requireAuth: false,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 1,
        desc: "描述",
        collapsed: false,
        show: true
      },
      {
        id: 2,
        creater: "admin",
        createTime: "2019-07-02 11:53:53",
        updater: "",
        updateTime: "",
        parentId: 0,
        name: "工作台",
        url: "/workbench",
        perms: "",
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 1,
        desc: "描述",
        collapsed: false,
        show: true
      },
      {
        id: 3,
        creater: "admin",
        createTime: "2019-07-02 11:53:53",
        updater: "",
        updateTime: "",
        parentId: 0,
        name: "测试视图",
        url: "/testerView",
        perms: "",
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 1,
        desc: "描述",
        collapsed: false,
        show: true
      }
    ]
  }
  return {
    url: "/api/v1/sub-sys-menus",
    type: "get",
    data: result
  }
}

// 添加系统菜单
export function addSysMenus() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: {
      id: 4,
      creater: "admin", // 创建人
      createTime: "2019-07-02 11:53:53", // 创建时间
      updater: "", // 修改人
      updateTime: "", // 修改时间
      parentId: 0, // 上级ID，0表示上级ID为根节点
      name: "新增子菜单", // 菜单名称
      url: "/home", // 菜单URL
      perms: "", // 权限标识
      requireAuth: false, // 是否需要登录 flase-不需要 true 需要
      type: "菜单", // 类型 可选值 菜单 目录 按钮
      icon: "fa fa-home fa-lg", // 图标
      order: 1, // 顺序
      desc: "描述", // 描述信息
      collapsed: false, // 是否展开
      show: true // 是否显示
    }
  }
  return {
    url: "/api/v1/sys-menu",
    type: "post",
    data: result
  }
}

// 修改系统菜单
export function updateSysMenu() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: {
      creater: "admin", // 创建人
      createTime: "2019-07-02 11:53:53", // 创建时间
      updater: "", // 修改人
      updateTime: "", // 修改时间
      parentId: 0, // 上级ID，0表示上级ID为根节点
      name: "修改后的子菜单", // 菜单名称
      url: "/home", // 菜单URL
      perms: "", // 权限标识
      requireAuth: false, // 是否需要登录 flase-不需要 true 需要
      type: "菜单", // 类型 可选值 菜单 目录 按钮
      icon: "fa fa-home fa-lg", // 图标
      order: 1, // 顺序
      desc: "描述", // 描述信息
      collapsed: false, // 是否展开
      show: true // 是否显示
    }
  }
  return {
    url: "/api/v1/sys-menu/{menuId}",
    type: "patch",
    data: result
  }
}

// 删除系统菜单
export function deleteSysMenu() {
  const result = {
    success: true,
    msg: "删除成功"
  }
  return {
    url: "/api/v1/sys-menu/{menuId}",
    type: "delete",
    data: result
  }
}
