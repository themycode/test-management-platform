/*
 * 工具统一集成模块
 */

import * as permission from "./permission"
import * as htmlToPdf from "./htmlToPdf"
import * as headerMenu from "./headerMenu"
import * as userInfo from "./userInfo"
import * as cookie from "./cookie"
import * as stringHandler from "./stringHandler"
import * as dateTimeHandler from "./dateTimeHandler"
import * as uuid from "./uuid"

// 默认全部导出
export default {
  permission,
  htmlToPdf,
  headerMenu,
  userInfo,
  cookie,
  stringHandler,
  dateTimeHandler,
  uuid
}
