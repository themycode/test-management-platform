// 获取测试集包含的测试用例
export function suiteCases() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: {
      totalRows: 500, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      suitePath: "/Sprint100", // 测试集树中被点击节点的全路径
      suiteCaseList: [
        {
          id: 1, // 数据库自增ID 用例ID
          customNo: "", // 自定义编号,如果本字典对象表示测试集则为置为空,如果表示测试用例，如果不提供该值则置为
          name: "/Sprint100", // 测试集路径
          priority: "",
          type: "",
          creater: "赖某人",
          updater: "林某人",
          failNum: 0,
          tags: [],
          createTime: "2019-05-29 09:14:59",
          desc: "",
          suiteID: 2,
          suitePath: "/Sprint100",
          precondition: "",
          postcondition: "",
          result: "",
          tester: "",
          relatedBugs: [],
          remark: "",
          children: [
            {
              id: 2,
              customNo: "s13434",
              name: "人工译码容错测试用例x",
              priority: "P1",
              type: "功能",
              creater: "赖某人",
              updater: "上官晓晓",
              failNum: 0,
              tags: ["标签1", "标签2"],
              createTime: "2019-05-29 09:19:59",
              desc: "用例描述1",
              suitePath: "/Sprint100",
              precondition: "前置条件1",
              postcondition: "后置条件1",
              result: "通过",
              tester: "赖某人",
              relatedBugs: [
                { id: 100000008655222, projectID: 1 },
                { id: 1235000008655222, projectID: 2 },
                { id: 1200089556558898, projectID: 3 },
                { id: 1200089556558545, projectID: 4 },
                { id: 1203434346558545, projectID: 5 }
              ],
              remark: "测试备注1",
              children: []
            }
          ]
        },
        {
          id: 3,
          customNo: "",
          name: "/Sprint100/1001二级1",
          priority: "",
          type: "",
          creater: "林某人",
          updater: "林某人",
          failNum: 0,
          tags: [],
          createTime: "2019-05-29 09:14:59",
          desc: "",
          suiteID: 2,
          suitePath: "/Sprint100/1001二级1",
          precondition: "",
          postcondition: "",
          result: "",
          tester: "",
          remark: "",
          relatedBugs: [],
          children: [
            {
              id: 4,
              customNo: 2,
              name: "人工译码容错测试用例y",
              priority: "P2",
              type: "自动化",
              creater: "上官某人",
              updater: "赖某人",
              failNum: 0,
              tags: ["标签4-1", "标签4-2"],
              createTime: "2019-05-29 08:19:90",
              desc: "用例描述2",
              suitePath: "/Sprint100/1001二级1",
              precondition: "前置条件2",
              postcondition: "后置条件2",
              result: "阻塞",
              tester: "上官某人",
              relatedBugs: [
                { id: 1, projectID: 1 },
                { id: 2, projectID: 2 },
                { id: 3, projectID: 3 },
                { id: 4, projectID: 4 }
              ],
              remark: "测试备注1",
              children: []
            }
          ]
        },
        {
          id: 5,
          customNo: "",
          name: "/Sprint100/1003二级2",
          priority: "",
          type: "",
          creater: "赖某人",
          updater: "林某人",
          failNum: 0,
          tags: [],
          createTime: "2019-05-29 09:10:59",
          desc: "",
          suiteID: 2,
          suitePath: "/Sprint100/1003二级2",
          precondition: "",
          postcondition: "",
          result: "",
          tester: "",
          remark: "",
          relatedBugs: [],
          children: [
            {
              id: 6,
              customNo: 3,
              name: "人工译码页面在分辨率为1366*768时，快捷语和附图的+没有重叠2",
              priority: "P3",
              type: "功能",
              creater: "赖某人",
              updater: "赖某人",
              failNum: 0,
              tags: ["标签6-1", "标签6-2"],
              createTime: "2019-05-29 08:18:90",
              desc: "用例描述3",
              suitePath: "/Sprint100/1003二级2",
              precondition: "前置条件3",
              postcondition: "后置条件3",
              result: "通过",
              tester: "上官晓晓",
              relatedBugs: [],
              remark: "测试备注ddd",
              children: []
            }
          ]
        },
        {
          id: 7,
          customNo: "",
          name: "/Sprint100/1005二级3",
          priority: "",
          type: "",
          creater: "赖某人",
          updater: "林某人",
          failNum: 0,
          tags: "",
          createTime: "2019-05-29 09:10:59",
          desc: "",
          suiteID: 2,
          suitePath: "/Sprint100/1005二级3",
          precondition: "",
          postcondition: "",
          result: "",
          tester: "",
          relatedBugs: [],
          remark: "",
          children: [
            {
              id: 8,
              customNo: 4,
              name: "事故与非事故相关字段检查1",
              priority: "P1",
              type: "功能",
              creater: "赖某人",
              updater: "上官晓晓",
              failNum: 0,
              tags: [],
              createTime: "2019-05-29 08:18:90",
              desc: "用例描述4",
              suitePath: "/Sprint100/1005二级3",
              precondition: "前置条件4",
              postcondition: "后置条件4",
              result: "失败",
              tester: "上官某人",
              relatedBugs: [],
              remark: "测试的的备注测试的的备注测试的的备注测试的的备注",
              children: []
            },
            {
              id: 9,
              customNo: 5,
              name: "事故与非事故相关字段检查copy",
              priority: "P4",
              type: "功能",
              creater: "上官晓晓",
              updater: "赖某人",
              failNum: 0,
              tags: ["标签5"],
              createTime: "2019-05-29 08:17:90",
              desc: "",
              suitePath: "/Sprint100/1005二级3",
              precondition: "前置条件5",
              postcondition: "后置条件5",
              result: "未执行",
              tester: "上官某人",
              relatedBugs: [],
              remark: "老师说测试的备注要很长很长测试的的备注测试的的备注",
              children: []
            }
          ]
        }
      ]
    }
  }
  return {
    url: "/api/v1/plan/suiteCases",
    method: "get",
    data: result
  }
}

// 删除测试用例
export function deleteTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/testCase/delete",
    type: "post",
    data: result
  }
}

// // 获取测试用例步骤
// export function getTestCaseSteps() {
//   const result = {
//     code: 200,
//     success: true,
//     msg: "",
//     data: [
//       {
//         id: 1, // 数据库自增ID 测试用例步骤ID
//         action: "第1步做啥", // 动作描述
//         expection: "第1步期望结果", // 预期结果
//         editing: false // 是否编辑状态标识 false 非编辑状态 true 编辑状态
//       },
//       {
//         id: 2, // 数据库自增ID 测试用例步骤ID
//         action: "第2步做啥", // 动作描述
//         expection: "第2步期望结果", // 预期结果
//         editing: false
//       },
//       {
//         id: 3, // 数据库自增ID 测试用例步骤ID
//         action: "第3步做啥", // 动作描述
//         expection: "第3步期望结果", // 预期结果
//         editing: false
//       },
//       {
//         id: 4, // 数据库自增ID 测试用例步骤ID
//         action: "第4步做啥", // 动作描述
//         expection: "第4步期望结果", // 预期结果
//         editing: false
//       },
//       {
//         id: 5, // 数据库自增ID 测试用例步骤ID
//         action: "第5步做啥", // 动作描述
//         expection: "第5步期望结果", // 预期结果
//         editing: false
//       }
//     ]
//   }
//   return {
//     url: "/api/v1/plan/testCase/steps",
//     type: "get",
//     data: result
//   }
// }

// // 获取测试用例附件列表
// export function caseAttachments() {
//   const result = {
//     code: 200,
//     success: true,
//     msg: "获取测试用例附件成功",
//     data: [
//       {
//         id: 1, //数据库自增id
//         name: "food.jpeg", //文件名称
//         url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?" // 文件访问链接
//       },
//       {
//         id: 2,
//         name: "food2.jpeg",
//         url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?"
//       }
//     ]
//   }
//   return {
//     url: "/api/v1/plan/testCase/caseAttachments",
//     type: "get",
//     data: result
//   }
// }

// 导出测试用例
export function exportTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "导出成功",
    data: { fileName: "导出用例201906111603.xlsx", tableData: { key: "暂时没法mock" } }
  }
  return {
    url: "/api/v1/plan/testCase/export",
    type: "get",
    data: result
  }
}

// 批量修改用例测试结果
export function updateCaseTestResult() {
  const result = {
    code: 200,
    success: true,
    msg: "修改成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/testCase/testResult/update",
    type: "post",
    data: result
  }
}

// 修改测试用例的测试备注
export function updateCaseTestRemark() {
  const result = {
    code: 200,
    success: true,
    msg: "修改成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/testCase/testRemark/update",
    type: "post",
    data: result
  }
}

// 删除测试用例关联的bug
export function deleteCaseRelatedBug() {
  const result = {
    code: 200,
    success: true,
    msg: "取消关联成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/testCase/relatedBug/delete",
    type: "post",
    data: result
  }
}

// 新增和测试用例关联的bug
export function relateBugToCase() {
  const result = {
    code: 200,
    success: true,
    msg: "关联成功",
    data: {}
  }
  return {
    url: "/api/v1/plan/testCase/relatedBug/add",
    type: "post",
    data: result
  }
}
