import axios from "../../../axios"

// 新建测试用例
export const addTestCase = data => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcase",
    method: "post",
    data
  })
}

// 更新测试用例
export const updateTestCase = data => {
  return axios.request({
    url: "/api/v1/testsuite/{suiteId}/testcase/{caseId}",
    method: "patch",
    data
  })
}


// 获取测试用例关联的附件
export const getCaseAttachments = params => {
  return axios.request({
    url: "/api/v1/testcase/{caseId}/attachments",
    method: "get",
    params
  })
}

// 上传测试用例附件
export const uploadAttatchment = data => {
  return axios.request({
    url: "/api/v1/testcase/{caseId}/attachment",
    method: "post",
    data: data,
    headers: { "Content-type": "multipart/form-data" }
  })
}

// 删除测试用例附件
export const deleteAttatchment = data => {
  return axios.request({
    url: "/api/v1/testcase/{caseId}/attachment/{attachmentId}",
    method: "delete",
    data: data
  })
}

// 下载测试用例附件
export const downloadAttatchment = params => {
  return axios.request({
    url: "/api/v1/testcase/{caseId}/attachment/{attachmentId}",
    method: "get",
    params,
    responseType: "blob"
  })
}
