/*
 * 接口统一集成模块
 */

import * as login from "./modules/loginLogout";
import * as product from "./modules/productView/product";
import * as sprint from "./modules/productView/sprint";
import * as project from "./modules/projectView/project";
import * as projectVersion from "./modules/projectView/projectVersion";
import * as apiProjectGroup from "./modules/projectView/apiProjectGroup";
import * as apiProject from "./modules/projectView/apiProject";
import * as projectEnv from "./modules/projectView/projectEnv";
import * as projectAPIGroup from "./modules/developerView/projectAPIGroup";
import * as projectAPITable from "./modules/developerView/projectAPITable";

import * as sprintCaseSuite from "./modules/testerView/sprintCase/sprintCaseSuite";
import * as sprintCaseTable from "./modules/testerView/sprintCase/sprintCaseTable";
import * as sprintCaseDialog from "./modules/testerView/sprintCase/sprintCaseDialog";
import * as sprintTestPlan from "./modules/testerView/sprintTestPlan/sprintTestPlan";
import * as testPlanCaseTable from "./modules/testerView/sprintTestPlan/testPlanCaseTable";
import * as sprintTestReport from "./modules/testerView/sprintTestReport/sprintTestReport";
import * as sysMenu from "./modules/system/sysMenu";
import * as sysRole from "./modules/system/sysRole";
import * as sysUser from "./modules/system/sysUser";
import * as sysGroup from "./modules/system/sysGroup";
import * as env from "./modules/system/env";
import * as testPhase from "./modules/system/testPhase";
import * as msgPushAccount from "./modules/system/msgPushAccount";
import * as workbench from "./modules/workbench/workbench";
import * as sprintsStatistics from "./modules/metric/sprintsStatistics";
import * as onlineStatistics from "./modules/metric/onlineStatistics";

import * as common from "./modules/common";

// 默认全部导出
export default {
  login,
  product,
  sprint,
  project,
  projectVersion,
  apiProjectGroup,
  apiProject,
  projectEnv,
  projectAPIGroup,
  projectAPITable,
  sprintCaseSuite,
  sprintCaseTable,
  sprintCaseDialog,
  sprintTestPlan,
  testPlanCaseTable,
  sprintTestReport,
  sysMenu,
  sysRole,
  sysUser,
  sysGroup,
  env,
  testPhase,
  msgPushAccount,
  workbench,
  sprintsStatistics,
  onlineStatistics,

  common
};
