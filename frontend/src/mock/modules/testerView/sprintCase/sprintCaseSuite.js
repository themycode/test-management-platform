// 获取sprint测试用例套件、测试集
export function sprintCaseSuiteTree() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        id: 1,
        nodeType: "base", // nodeType: 节点分类  base  基线测试套件 sprint 迭代测试套件  sprintRoot 迭代测试套件-根套件
        name: "基线测试集",
        nodeGroupID: 0, // 节点归属组别
        // isLeaf: false, // 是否叶子节点
        parentID: 0, //父节点id
        editing: false, // 是否正在编辑 true-正在编辑 false-展示状态
        children: []
      },
      {
        id: 2,
        nodeType: "sprintRoot",
        name: "Sprint100",
        nodeGroupID: 0,
        // isLeaf: false,
        parentID: 0,
        editing: false,
        children: []
      }
    ]
  }
  return {
    url: "/api/v1/sprintCaseSuiteTree",
    type: "get",
    data: result
  }
}

// 获取测试用例套件的子套件
export function subCaseSuite() {
  const result = {
    code: 200,
    success: true,
    msg: null,
    data: [
      {
        id: 3,
        nodeType: "sprint",
        name: "二级1",
        nodeGroupID: 1,
        // isLeaf: false,
        parentID: 2,
        // editing: true,
        children: []
      },
      {
        id: 6,
        nodeType: "sprint",
        name: "二级 2",
        nodeGroupID: 1,
        // isLeaf: false,
        parentID: 2,
        // editing: false,
        children: []
      },
      {
        id: 4,
        name: "二级 3",
        nodeGroupID: 1,
        nodeType: "base",
        // isLeaf: true,
        parentID: 2,
        // editing: false,
        children: []
      }
    ]
  }
  return {
    url: "/api/v1/subCaseSuite",
    type: "get",
    data: result
  }
}

// 新增sprint测试用例套件
export function addSprintCaseSuite() {
  const result = {
    code: 200,
    success: true,
    msg: "",
    data: {
      id: 200,
      nodeType: "sprint",
      name: "新建测试集ID200",
      nodeGroupID: 1,
      // isLeaf: false,
      parentID: 2,
      editing: true,
      children: []
    }
  }
  return {
    url: "/api/v1/sprintCaseSuite/add",
    type: "post",
    data: result
  }
}

// 修改sprint测试用例套件
export function updateSprintCaseSuite() {
  const result = {
    code: 200,
    success: true,
    msg: "修改成功",
    data: {}
  }
  return {
    url: "/api/v1/sprintCaseSuite/update",
    type: "post",
    data: result
  }
}

// 删除测试套件
export function deleteSprintCaseSuite() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/sprintCaseSuite/delete",
    type: "post",
    data: result
  }
}
