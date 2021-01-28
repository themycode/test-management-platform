// 获取sprint版本关联的测试计划
export function testPlans() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: {
      totalRows: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      testPlanList: [
        {
          id: 1, // 数据库自增ID
          name: "询价-测试计划1", //计划名称
          desc: "询价-测试计划1-具体描述",
          beginTime: "2019-06-03 09:00:00", // 预估开始时间
          endTime: "2019-06-03 10:23:59", // 预估结束时间
          sprint: "Sprint101",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59", //实际开始时间
          finishTime: "2019-06-30 09:14:59", // 实际完成时间
          group: "订单组",
          groupID: [1],
          environment: "测试环境",
          environmentID: 1,
          progress: "54.1%(46/85)",
          passRate: "42.4%(36/85)",
          status: "测试中",
          sprintCaseIDList: [1, 2, 99, 100, 1000], //存放关联的测试用例ID(包含用例所在sprint测试集在用例表中的映射记录的ID)
          baseCaseIDList: [1, 2, 99, 100, 1000] //存放关联的测试用例ID(包含用例所在基线测试集在用例表中的映射记录的ID)
        },
        {
          id: 2, // 数据库自增ID
          name: "询价-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "询价组",
          groupID: [3],
          environment: "演示环境",
          environmentID: 2,
          progress: "54.1%(46/85)",
          passRate: "42.4%(36/85)",
          status: "测试中",
          sprintCaseIDList: [3, 4],
          baseCaseIDList: [3, 4]
        },
        {
          id: 3, // 数据库自增ID
          name: "订单-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [5, 6],
          baseCaseIDList: [3, 4]
        },
        {
          id: 5, // 数据库自增ID
          name: "订单-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [1, 2, 3, 4, 5, 6],
          baseCaseIDList: [3, 4]
        },
        {
          id: 6, // 数据库自增ID
          name: "订单-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [],
          baseCaseIDList: [3, 4]
        },
        {
          id: 7, // 数据库自增ID
          name: "订单-测试计划2",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [],
          baseCaseIDList: [3, 4]
        },
        {
          id: 8, // 数据库自增ID
          name: "订单-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [],
          baseCaseIDList: []
        },
        {
          id: 9, // 数据库自增ID
          name: "订单-测试计划2",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [],
          baseCaseIDList: []
        },
        {
          id: 10, // 数据库自增ID
          name: "订单-测试计划10",
          beginTime: "2019-06-03 09:00:00",
          endTime: "2019-06-03 10:23:59",
          sprint: "Sprint101",
          creater: "上官晓晓",
          createTime: "2019-05-28 09:14:59",
          startTime: "2019-06-04 09:14:59",
          finishTime: "2019-06-30 09:14:59",
          group: "订单组",
          groupID: [1],
          environment: "生产环境",
          environmentID: 3,
          progress: "100%(100/100)",
          passRate: "92%(92/100)",
          status: "已完成",
          sprintCaseIDList: [],
          baseCaseIDList: []
        }
      ]
    }
  }
  return {
    url: "/api/v1/testplans",
    method: "get",
    data: result
  }
}

// 新增测试计划
export function addTestPlan() {
  const result = {
    code: 200,
    msg: "新增测试计划成功",
    success: true,
    data: {
      id: 4, // 数据库自增ID
      name: "订单-测试计划3", // 测试集路径
      desc: "订单-测试计划3-具体描述",
      beginTime: "2019-06-03 09:00:00", // 预估开始时间
      endTime: "2019-06-03 10:23:59", // 预估结束时间
      sprint: "Sprint101",
      creater: "上官晓晓",
      createTime: "2019-05-28 09:14:59",
      startTime: "",
      finishTime: "",
      group: "订单组",
      groupID: [1],
      environment: "测试环境",
      environmentID: 1,
      progress: "0%(0/0)",
      passRate: "0%(0/0)",
      status: "待测试",
      sprintCaseIDList: [],
      baseCaseIDList: []
    }
  }
  return {
    url: "/api/v1/testplan",
    method: "post",
    data: result
  }
}

// 修改测试计划
export function updateTestPlan() {
  const result = {
    code: 200,
    msg: "修改测试计划成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/testplan",
    method: "patch",
    data: result
  }
}

// 删除测试计划
export function deleteTestPlan() {
  const result = {
    code: 200,
    success: true,
    msg: "计划删除成功",
    data: {}
  }
  return {
    url: "/api/v1/testplan",
    type: "delete",
    data: result
  }
}

// 关联测试计划和用例
export function bindTestCase() {
  const result = {
    code: 200,
    success: true,
    msg: "用例关联成功",
    data: { sprintCaseIDList: [1, 2, 3, 5, 6], baseCaseIDlist: [1, 2, 3, 4, 5, 6] } // sprintCaseIDList, baseCaseIDlist 存放当前测试计划绑定的测试用例ID(包含测试集在用例表中映射记录的ID)
  }
  return {
    url: "/api/v1/bindTestCase",
    type: "post",
    data: result
  }
}
