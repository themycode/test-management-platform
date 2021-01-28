import Mock from "mockjs"

// import * as login from "./modules/loginLogout"
// import * as menu from "./modules/menu"
// import * as sprintCaseSuite from "./modules/testerView/sprintCase/sprintCaseSuite"
// import * as sprintCaseTable from "./modules/testerView/sprintCase/sprintCaseTable"
// import * as sprintCaseDialog from "./modules/testerView/sprintCase/sprintCaseDialog"
// import * as sprintTestPlan from "./modules/testerView/sprintTestPlan/sprintTestPlan"
// import * as testPlanCaseTable from "./modules/testerView/sprintTestPlan/testPlanCaseTable"
// import * as testPlanBugTable from "./modules/testerView/sprintTestPlan/testPlanBugTable"
// import * as sprintTestReport from "./modules/testerView/sprintTestReport/sprintTestReport"
// import * as sysMenu from "./modules/system/sysMenu"
// import * as sysRole from "./modules/system/sysRole"
// import * as sysUser from "./modules/system/sysUser"
// import * as sysGroup from "./modules/system/sysGroup"
// import * as sprint from "./modules/system/sprint"
// import * as env from "./modules/system/env"
// import * as msgPush from "./modules/system/msgPush"

// import * as common from "./modules/common"

import constant from "@/common/constant"

// 1. 开启/关闭[所有模块]拦截, 通过调[openMock参数]设置.
// 2. 开启/关闭[业务模块]拦截, 通过调用fnCreate方法[isOpen参数]设置.
// 3. 开启/关闭[业务模块中某个请求]拦截, 通过函数返回对象中的[isOpen属性]设置.
// let openMock = true

// fnCreate(menu, openMock)
// fnCreate(sprintCaseSuite, openMock)
// fnCreate(sprintCaseTable, openMock)
// fnCreate(sprintCaseDialog, openMock)
// fnCreate(sprintTestPlan, openMock)
// fnCreate(testPlanCaseTable, openMock)
// fnCreate(testPlanBugTable, openMock)
// fnCreate(sprintTestReport, openMock)
// fnCreate(sysMenu, openMock)
// fnCreate(sysRole, openMock)
// fnCreate(sysUser, openMock)
// fnCreate(sysGroup, openMock)
// fnCreate(sprint, openMock)
// fnCreate(env, openMock)
// fnCreate(msgPush, openMock)

// fnCreate(common, openMock)

/**
 * 创建mock模拟数据
 * @param {*} mod 模块
 * @param {*} isOpen 是否开启?
 */
function fnCreate(mod, isOpen = true) {
  if (isOpen) {
    for (var key in mod) {
      ;(res => {
        if (res.isOpen !== false) {
          let url = constant.baseUrl
          if (!url.endsWith("/")) {
            url = url + "/"
          }
          if (res.url.startsWith("/")) {
            res.url = res.url.substring(1)
          }

          url = url + res.url
          Mock.mock(new RegExp(url), res.method, opts => {
            console.log("\n")
            console.log("%cmock拦截, 请求: ", "color:blue", opts)
            console.log("%cmock拦截, 响应: ", "color:blue", res.data)
            return res.data
          })
        }
      })(mod[key]() || {})
    }
  }
}
