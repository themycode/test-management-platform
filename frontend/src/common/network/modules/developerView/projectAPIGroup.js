import axios from "../../axios";

// 获取API分组树
export const getAPIGroupTree = params => {
  return axios.request({
    url: "/api/v1/api-group-tree",
    method: "get",
    params
  });
};

// 新增API分组
export const addAPIGroup = data => {
  return axios.request({
    url: "/api/v1/api-group",
    method: "post",
    data
  });
};

// 更新API分组
export const updateAPIGroup = data => {
  return axios.request({
    url: "/api/v1/api-group/{groupId}",
    method: "patch",
    data
  });
};

// 删除API分组
export const deleteAPIGroup = data => {
  return axios.request({
    url: "/api/v1/api-group/{groupId}",
    method: "delete",
    data
  });
};


// 拖拽API分组
export const dragAPIGroup = data => {
  return axios.request({
    url: "/api/v1/drag-api-group",
    method: "post",
    data
  });
};

// // 黏贴拷贝的用例到测试集下
// export const pasteTestcasesCopied = data => {
//   return axios.request({
//     url: "/api/v1/testcase-suite/{suiteId}/testcases-copied",
//     method: "post",
//     data
//   });
// };

// // 黏贴剪切的用例到测试集下
// export const pasteTestcasesCut = data => {
//   return axios.request({
//     url: "/api/v1/testcase-suite/{suiteId}/testcases-cut",
//     method: "post",
//     data
//   });
// };

// // 黏贴剪切的测试集到目标测试集下
// export const pasteSuiteCut = data => {
//   return axios.request({
//     url: "/api/v1/paste-suite-cut/{suiteId}",
//     method: "post",
//     data
//   });
// };

// // 按结构黏贴复制的测试集
// export const pasteSuiteByStructure = data => {
//   return axios.request({
//     url: "/api/v1/paste-suite-by-structure",
//     method: "post",
//     data
//   });
// };
