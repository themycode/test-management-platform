/*
 * 公用模块
 */
// 获取用户列表
export function sysUsers() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: [
      {
        value: 1,
        label: "上官晓晓"
      },
      {
        value: 2,
        label: "林笑笑"
      }
    ]
  }
  return {
    url: "/api/v1/sysUsers/details",
    method: "get",
    data: result
  }
}

// 获取项目版本
export function projectSprints() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        value: 1,
        label: "Sprint100"
      },
      {
        value: 2,
        label: "Sprint101"
      }
    ]
  }
  return {
    url: "/api/v1/sprints/details",
    type: "get",
    data: result
  }
}

// 获取环境列表
export function environments() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        value: 1,
        label: "测试环境"
      },
      {
        value: 2,
        label: "演示环境"
      },
      {
        value: 3,
        label: "生产环境"
      }
    ]
  }
  return {
    url: "/api/v1/environments/details",
    type: "get",
    data: result
  }
}

// 搜索tpad缺陷
export function bugs() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        id: 5,
        name: "输入用户BBB和密码12346能够正常登录，用户BBB不存在",
        severityLevel: "严重",
        status: "已解决",
        handler: "处理人",
        creater: "提交人"
      },
      {
        id: 6,
        name: "输入部分产品名称，进行模糊搜索，结果不正确",
        severityLevel: "一般",
        status: "未解决",
        handler: "林某某",
        creater: "上官某人"
      },
      {
        id: 7,
        name: "输入部分产品名称，进行模糊搜索，结果用户BBB不存在",
        severityLevel: "轻微",
        status: "已解决",
        handler: "上官某某",
        creater: "林某某"
      }
    ]
  }
  return {
    url: "/api/v1/tpad/bugs/details",
    type: "get",
    data: result
  }
}
