// 获取导航菜单树
export function navMenuData() {
  const menuData = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        id: 1,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "首页",
        url: "/home",
        perms: null,
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 1,
        collapsed: true, // 是否展开

        children: [
          {
            id: 2,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 1,
            name: "首页二级菜单1",
            url: "",
            perms: null,
            requireAuth: true,
            type: "目录",
            icon: "fa fa-home fa-lg",
            order: 1,
            collapsed: false, // 是否展开
            children: [
              {
                id: 3,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 2,
                name: "首页三级菜单1",
                url: "",
                perms: null,
                requireAuth: true,
                type: "目录",
                icon: "fa fa-home fa-lg",
                order: 1,
                collapsed: false, // 是否展开

                children: [
                  {
                    id: 4,
                    creater: null,
                    createTime: null,
                    modifier: null,
                    updateTime: null,
                    parentID: 3,
                    name: "首页四级菜单1",
                    url: "/home/level4Menu1",
                    perms: null,
                    requireAuth: true,
                    type: "菜单",
                    icon: "fa fa-home fa-lg",
                    order: 1,
                    children: []
                  }
                ]
              },
              {
                id: 5,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 2,
                name: "首页三级菜单2",
                url: "/home/level3Menu2",
                perms: null,
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 2,
                children: []
              }
            ]
          },
          {
            id: 6,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 1,
            name: "首页二级菜单2",
            url: "",
            perms: null,
            requireAuth: true,
            type: "目录",
            icon: "fa fa-home fa-lg",
            order: 2,
            children: [
              {
                id: 7,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 6,
                name: "首页三级菜单3",
                url: "/home/level3Menu3",
                perms: null,
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 1,
                children: []
              }
            ]
          }
        ]
      },
      {
        id: 8,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "工作台",
        url: "/workbench",
        perms: null,
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 2,
        children: []
      },
      {
        id: 9,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "测试视图",
        url: "/testerView",
        perms: null,
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 3,
        children: [
          {
            id: 10,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 9,
            name: "测试用例管理",
            url: "/testerView/testCaseManagement",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 1,
            children: []
          },
          {
            id: 11,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 9,
            name: "测试计划管理",
            url: "/testerView/testPlanManagement",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 2,
            children: []
          },
          {
            id: 12,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 9,
            name: "测试报告管理",
            url: "",
            perms: null,
            requireAuth: true,
            type: "目录",
            icon: "fa fa-home fa-lg",
            order: 3,
            children: [
              {
                id: 13,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 12,
                name: "迭代测试报告",
                url: "/testerView/sprintTestReport",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 1,
                children: []
              }
            ]
          }
        ]
      },
      {
        id: 14,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "度量",
        url: "/metrics",
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 4,
        children: [
          {
            id: 15,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 14,
            name: "度量二级菜单",
            url: "",
            requireAuth: true,
            type: "目录",
            icon: "fa fa-home fa-lg",
            order: 1,
            children: [
              {
                id: 16,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 15,
                name: "测试计划报告",
                url: "/metrics/testPlanReport",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 1,
                children: []
              }
            ]
          }
        ]
      },
      {
        id: 17,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "系统管理",
        url: "/system",
        requireAuth: true,
        type: "菜单",
        icon: "fa fa-home fa-lg",
        order: 5,
        children: [
          {
            id: 18,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 17,
            name: "系统配置",
            url: "",
            requireAuth: true,
            type: "目录",
            icon: "fa fa-home fa-lg",
            order: 1,
            collapsed: false,
            children: [
              {
                id: 19,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 18,
                name: "资源管理",
                url: "/system/sysMenu",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 1,
                children: []
              },
              {
                id: 20,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 18,
                name: "角色管理",
                url: "/system/sysRole",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 2,
                children: []
              },
              {
                id: 21,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 18,
                name: "用户管理",
                url: "/system/sysUser",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 3,
                children: []
              },
              {
                id: 22,
                creater: null,
                createTime: null,
                modifier: null,
                updateTime: null,
                parentID: 18,
                name: "组别管理",
                url: "/system/sysGroup",
                requireAuth: true,
                type: "菜单",
                icon: "fa fa-home fa-lg",
                order: 3,
                children: []
              }
            ]
          },
          {
            id: 23,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 17,
            name: "迭代管理",
            url: "/system/sprint",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 2,
            children: []
          },
          {
            id: 24,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 17,
            name: "环境管理",
            url: "/system/env",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 3,
            children: []
          },
          {
            id: 25,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 17,
            name: "推送账号管理",
            url: "/system/msgPushAccount",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 4,
            children: []
          }
        ]
      },
      {
        id: 26,
        creater: null,
        createTime: null,
        modifier: null,
        updateTime: null,
        parentID: 0,
        name: "其它",
        url: "",
        requireAuth: true,
        type: "目录",
        icon: "fa fa-home fa-lg",
        order: 6,
        children: [
          {
            id: 27,
            creater: null,
            createTime: null,
            modifier: null,
            updateTime: null,
            parentID: 26,
            name: "其它菜单",
            url: "/other",
            requireAuth: true,
            type: "菜单",
            icon: "fa fa-home fa-lg",
            order: 1,
            children: []
          }
        ]
      }
    ]
  }
  return {
    url: "/api/v1/user/{username}/menus",
    type: "get",
    data: menuData
  }
}
