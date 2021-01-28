export function sprints() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: {
      totalRows: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      sprintList: [
        {
          id: 1, // 数据库自增ID
          name: "Sprint100",
          version: "100",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 4,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 5,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          name: "Sprint101",
          version: "101",
          desc: "用户描述1",
          status: "启用", // 是否启用
          creater: "赖晓晓",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/system/sprints",
    method: "get",
    data: result
  }
}

// 新增迭代
export function addSprint() {
  const result = {
    code: 200,
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      name: "新增的迭代",
      version: "101",
      desc: "用户描述1",
      status: "启用", // 是否启用
      creater: "赖晓晓",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/sprint/add",
    method: "post",
    data: result
  }
}

// 修改迭代
export function updateSprint() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {
      name: "修改后的迭代",
      version: "101",
      desc: "用户描述1",
      status: "启用", // 是否启用
      creater: "赖晓晓",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/sprint/update",
    method: "post",
    data: result
  }
}

// 删除迭代
export function deleteSprint() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/system/sprint/delete",
    type: "post",
    data: result
  }
}

// 启用/作废sprint
export function toggleSprintStatus() {
  const result = {
    code: 200,
    success: true,
    msg: "操作成功",
    data: {}
  }
  return {
    url: "/api/v1/system/sprint/status/toggle",
    type: "post",
    data: result
  }
}
