// 新增测试用例
export function addTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "新增用例成功",
    data: {
      parentID: 2, // 新增用例所在的父级记录ID
      case: {
        id: 1000,
        customNo: 1000,
        name: "人工译码正向测试用例",
        priority: "P1",
        type: "功能",
        creater: "赖某人",
        updater: "上官晓晓",
        failNum: 0,
        tag: "tagName",
        createTime: "2019-05-29 09:19:59",
        desc: "用例描述1",
        suitePath: "/Sprint100",
        precondition: "前置条件",
        postcondition: "后置条件",
        children: []
      }
    }
  }

  return {
    url: "/api/v1/testCase/add",
    type: "post",
    data: result
  }
}

// 获取测试用例步骤
export function getTestCaseSteps() {
  const result = {
    code: 200,
    success: true,
    msg: "",
    data: [
      {
        id: 1, // 数据库自增ID 测试用例步骤ID
        action: "第1步做啥", // 动作描述
        expection: "第1步期望结果", // 预期结果
        editing: false // 是否编辑状态标识 false 非编辑状态 true 编辑状态
      },
      {
        id: 2, // 数据库自增ID 测试用例步骤ID
        action: "第2步做啥", // 动作描述
        expection: "第2步期望结果", // 预期结果
        editing: false
      },
      {
        id: 3, // 数据库自增ID 测试用例步骤ID
        action: "第3步做啥", // 动作描述
        expection: "第3步期望结果", // 预期结果
        editing: false
      },
      {
        id: 4, // 数据库自增ID 测试用例步骤ID
        action: "第4步做啥", // 动作描述
        expection: "第4步期望结果", // 预期结果
        editing: false
      },
      {
        id: 5, // 数据库自增ID 测试用例步骤ID
        action: "第5步做啥", // 动作描述
        expection: "第5步期望结果", // 预期结果
        editing: false
      }
    ]
  }
  return {
    url: "/api/v1/testCaseSteps",
    type: "get",
    data: result
  }
}

// 获取测试用例附件列表
export function caseAttachments() {
  const result = {
    code: 200,
    success: true,
    msg: "获取测试用例附件成功",
    data: [
      {
        id: 1, //数据库自增id
        name: "food.jpeg", //文件名称
        url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?" // 文件访问链接
      },
      {
        id: 2,
        name: "food2.jpeg",
        url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?"
      }
    ]
  }
  return {
    url: "/api/v1/caseAttachments",
    type: "get",
    data: result
  }
}

// 上传测试用例附件
export function uploadCaseAttachment() {
  const result = {
    code: 200,
    success: true,
    msg: "附件上传成功",
    data: {
      name: "我的附件文件.txt",
      url: "http://localhost:8080/file/caseAttachment/25555fskdkdslafdalsfadsfla-20190610.txt"
    }
  }
  return {
    url: "/api/v1/caseAttachement/upload",
    type: "post",
    data: result
  }
}

// 更新测试用例
export function updateTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "更新用例成功",
    data: {}
  }
  return {
    url: "/api/v1/testCase/update",
    type: "post",
    data: result
  }
}
