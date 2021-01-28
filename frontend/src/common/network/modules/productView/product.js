import axios from "../../axios"

// 获取table列表数据
export const getProducts = params => {
  return axios.request({
    url: "/api/v1/products",
    method: "get",
    params
  })
}

// 新增
export const addProduct = data => {
  return axios.request({
    url: "/api/v1/product",
    method: "post",
    data
  })
}

// 修改
export const updateProduct = data => {
  return axios.request({
    url: "/api/v1/product/{id}",
    method: "patch",
    data
  })
}

// 逐条删除
export const deleteProduct = data => {
  return axios.request({
    url: "/api/v1/product/{id}",
    method: "delete",
    data
  })
}

// 批量删除
export const deleteProducts = data => {
  return axios.request({
    url: "/api/v1/products",
    method: "delete",
    data
  })
}


// 按指定字段批量获取产品信息
export const getProductsDetails = params => {
  return axios.request({
    url: "/api/v1/products/details",
    method: "get",
    params
  })
}

// 按指定字段获取某个产品关联的迭代信息
export const getProductSprintsDetails = params => {
  return axios.request({
    url: "/api/v1/product/{productId}/sprints/details",
    method: "get",
    params
  })
}

