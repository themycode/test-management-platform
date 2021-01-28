// 获取计划关联的缺陷
export function planRelatedBugs() {
  const result = {
    code: 200,
    success: true,
    msg: "",
    totalRows: 10,
    data: [
      {
        id: 1, // 数据库自增ID
        bugID: 1,
        name: "输入用户BBB和密码123无法正常登录",
        severityLevel: "严重",
        status: "已解决",
        handler: "解决者",
        creater: "提交人",
        relatedCases: [12, 13, 1004, 1002, 1003, 10004, 10002, 103, 14, 1400000, 1410000000] // 关联的用例，数组元素为用例的CustomNo
      },
      {
        id: 2,
        bugID: 2,
        name: "输入进行模糊搜索，结果不正确",
        severityLevel: "一般",
        status: "未解决",
        handler: "林某某",
        creater: "上官某人",
        relatedCases: [10002, 1003, 10005]
      },
      {
        id: 3,
        bugID: 3,
        name: "部分产品名称糊搜索结果不存在",
        severityLevel: "轻微",
        status: "已解决",
        handler: "上官某某",
        creater: "林某某",
        relatedCases: []
      }
    ]
  }
  return {
    url: "/api/v1/plan/relatedBugs",
    type: "get",
    data: result
  }
}

// 新增计划关联的缺陷
export function relateBugToPlan() {
  const result = {
    code: 200,
    success: true,
    msg: "关联成功",
    data: [
      {
        id: 5,
        bugID: 5,
        name: "输入用户BBB和密码12346能够正常登录，用户BBB不存在",
        status: "已解决",
        handler: "解决者",
        creater: "提交人",
        relatedCases: []
      },
      {
        id: 6,
        bugID: 6,
        name: "输入部分产品名称，进行模糊搜索，结果不正确",
        status: "未解决",
        handler: "林某某",
        creater: "上官某人",
        relatedCases: []
      }
    ]
  }
  return {
    url: "/api/v1/plan/relatedBug/add",
    type: "post",
    data: result
  }
}

// 删除计划关联的缺陷
export function deleteRelatedBug() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/relatedBug/delete",
    type: "post",
    data: result
  }
}

// 获取和测试计划关联的测试用例详情信息
export function planRelatedCase() {
  const result = {
    code: 200,
    success: true,
    msg: "",
    data: {
      id: 2,
      customNo: 13434,
      name: "人工译码容错测试用例x",
      priority: "P1",
      type: "功能",
      creater: "赖某人",
      updater: "上官晓晓",
      tags: ["标签1", "标签2"],
      desc: "用例描述1",
      suitePath: "/Sprint100",
      precondition: "前置条件1",
      postcondition: "后置条件1"
    }
  }
  return {
    url: "/api/v1/plan/relatedCase",
    type: "post",
    data: result
  }
}

// 更新和计划关联的测试用例详情信息
export function updatePlanRelatedCase() {
  const result = {
    code: 200,
    success: true,
    msg: "保存成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/relatedCase/update",
    type: "post",
    data: result
  }
}
