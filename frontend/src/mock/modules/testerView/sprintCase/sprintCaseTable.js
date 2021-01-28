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
          children: [
            {
              id: 2,
              customNo: 13434,
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
          children: [
            {
              id: 4,
              customNo: 2,
              name: "人工译码容错测试用例y",
              priority: "P2",
              type: "功能",
              creater: "上官某人",
              updater: "赖某人",
              failNum: 0,
              tags: ["标签4-1", "标签4-2"],
              createTime: "2019-05-29 08:19:90",
              desc: "用例描述2",
              suitePath: "/Sprint100/1001二级1",
              precondition: "前置条件2",
              postcondition: "后置条件2",
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
              children: []
            }
          ]
        }
      ]
    }
  }
  return {
    url: "/api/v1/suiteCases",
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
    url: "/api/v1/testCase/delete",
    type: "post",
    data: result
  }
}

// 导入测试用例
// 参数：测试集ID，测试集类型，用例文件
export function importTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "导入成功",
    data: {}
  }
  return {
    url: "/api/v1/test-case/import",
    type: "post",
    data: result
  }
}

// 导出测试用例
export function exportTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "导出成功",
    data: { fileName: "导出用例201906111603.xlsx", tableData: { key: "暂时没法mock" } }
  }
  return {
    url: "/api/v1/testCase/export",
    type: "post",
    data: result
  }
}
