export function Envs() {
  const result = {
    code: 200,
    msg: null,
    success: true,
    data: {
      totalRows: 30, // 总的行记录数(包括嵌套行 //该值不能为字符串类型
      sprintList: [
        {
          id: 1, // 数据库自增ID
          name: "测试环境",
          desc: "环境描述",

          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 2,
          name: "演示环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 3,
          name: "生产环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 4,
          name: "线上环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 5,
          name: "其它环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 6,
          name: "其它环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        },
        {
          id: 7,
          name: "其它环境",
          desc: "环境描述",
          creater: "赖某人",
          createTime: "2019-05-28 09:14:59",
          modifier: "上官晓晓",
          modifyTime: "2019-06-04 09:14:59"
        }
      ]
    }
  }
  return {
    url: "/api/v1/system/envs",
    method: "get",
    data: result
  }
}

// 新增环境
export function addEnv() {
  const result = {
    code: 200,
    msg: "新增成功",
    success: true,
    data: {
      id: 10, // 数据库自增ID
      name: "新增的环境",
      desc: "环境描述",
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/env/add",
    method: "post",
    data: result
  }
}

// 修改环境
export function updateEnv() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {
      name: "修改后的环境",
      desc: "环境描述",
      creater: "赖某人",
      createTime: "2019-05-28 09:14:59",
      modifier: "上官晓晓",
      modifyTime: "2019-06-04 09:14:59"
    }
  }
  return {
    url: "/api/v1/system/env/update",
    method: "post",
    data: result
  }
}

// 删除环境
export function deleteEnv() {
  const result = {
    code: 200,
    success: true,
    msg: "删除成功",
    data: {}
  }
  return {
    url: "/api/v1/system/env/delete",
    type: "post",
    data: result
  }
}
