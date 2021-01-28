// import customUtils from "@/common/utils"
import axios from "axios";
import Cookies from "js-cookie";
import router from "@/router/";
import store from "@/store";
import Vue from "vue";

import { Message } from "element-ui";

let isRefreshing = false; // isRefreshing用于判断是否正在刷新token，以防止并发请求的情况下，重复请求更新token

function request(options) {
    return new Promise((resolve, reject) => {
    const instance = axios.create({
      baseURL: Vue.prototype.$appConfig.API_BASE_URL,
      headers: Vue.prototype.$appConfig.headers,
      timeout: Vue.prototype.$appConfig.API_REQUEST_TIMEOUT,
      withCredentials: Vue.prototype.$appConfig.withCredentials,
      responseType: Vue.prototype.$appConfig.responseType
    });

    // request 拦截器
    instance.interceptors.request.use(
      config => {
        let token = Cookies.get("token");
        // 2. 带上token
        if (token) {
          config.headers.Authorization = "Token " + token;
        }

        return config;
      },

      error => {
        // 请求错误时
        // 1. 判断请求超时
        if (
          error.code === "ECONNABORTED" &&
          error.message.indexOf("timeout") !== -1
        ) {
          console.log("timeout请求超时");
        }
        // 2. 需要重定向到错误页面
        const errorInfo = error.response;
        if (errorInfo) {
          error = errorInfo.data;
          const errorStatus = errorInfo.status; // 404 403 500 ...
          router.push({
            path: `/error/${errorStatus}`
          });
        }
        return Promise.reject(error); // 在调用的那边可以拿到(catch)你想返回的错误信息
      }
    );

    // response 拦截器
    instance.interceptors.response.use(
      response => {
        let data;
        // IE9时response.data是undefined，因此需要使用response.request.responseText(Stringify后的字符串)
        if (response.data == undefined) {
          data = JSON.parse(response.request.responseText);
        } else {
          data = response.data;
        }
        if (Object.prototype.toString.call(data) == "[object Blob]") {
          // 如果为下载请求响应，则返回整个响应，方便通过响应头等获取更多请求结果处理所需要的信息
          return response;
        } else {
          return data;
        }
      },
      err => {
        if (err && err.response) {
          switch (err.response.status) {
            case 400:
              err.msg = `请求错误: ${err.response.data.msg}`;
              break;
            case 401:
              err.msg = "未授权，请登录";
              break;
            case 403: {
              err.msg = `禁止访问`;
              break;
            }
            case 404:
              err.msg = `请求地址出错: ${err.response.config.url}`;
              break;
            case 408:
              err.msg = "请求超时";
              break;
            case 500:
              err.msg = `服务器内部错误 ${
                err.response.data.msg ? err.response.data.msg : ""
              }`;
              break;
            case 501:
              err.msg = "服务未实现";
              break;
            case 502:
              err.msg = "网关错误";
              break;
            case 503:
              err.msg = "服务不可用";
              break;
            case 504:
              err.msg = "网关超时";
              break;
            case 505:
              err.msg = "HTTP版本不受支持";
              break;
            default:
              err.msg = "未知错误";
          }
        }

        return Promise.reject(err); // 返回接口返回的错误信息
      }
    );

    // 请求处理
    options.url = toRestUrl(
      options.url,
      options.params ? options.params : options.data
    );

    instance(options)
      .then(res => {
        resolve(res);
      })
      .catch(error => {
        if (error && error.response) {
          let url = error.response.config.url.replace(
            Vue.prototype.$apiBaseURL,
            ""
          );
          url = url.replace(/^\/+|\/+$/gm, "");
          let searchResult = url.search(/^api\/.+?\/logout$/);
          if (error.response.status == 401) {
            if (
              error.response.data.detail == "TokenExpired" ||
              error.response.data.detail == "InvalidToken"
            ) {
              let token = sessionStorage.getItem("refreshToken");
              if (!token) {
                // 仅执行非退出登录操作时，才提示
                if (searchResult == -1) {
                  Message.info("token过期，请重新登录");
                }
                logout();
                return;
              }
              let refreshTokenRequestData = { refreshToken: token }; // 供刷新token请求使用的参数数据
              refreshToken(refreshTokenRequestData);
            } else if (
              error.response.data.detail == "TokenUserDisabledOrDeleted"
            ) {
              if (searchResult == -1) {
                Message.info("用户已被禁用或删除");
              }
              isRefreshing = false;
              logout();
            } else if (error.response.data.msg == "RefreshTokenExpired") {
              console.log("refersh token 过期，请重新登录");
              // 仅执行非退出登录操作时，才提示
              if (searchResult == -1) {
                Message.info("token过期，请重新登录");
              }
              isRefreshing = false;
              logout();
              return;
            }
            return;
          }

          if (
            error.response.status == 400 &&
            error.response.data.msg == "RefreshTokenNotExists"
          ) {
            console.log("refresh token 因过期被删除，请重新登录");

            // 仅执行非退出登录操作时，才提示
            if (searchResult == -1) {
              Message.info("token过期，请重新登录");
            }
            logout();
            return;
          }
        }

        reject(error);
      });
  });
}

//url转restful（替换url中的参数）
function toRestUrl(url, params) {
  //   let paramArr = url.match(/(?<=\{).*?(?=\})/gi) // npm run build打包失败，不支持这种正则表达式
  //   if (paramArr && paramArr.length) {
  //     if (Object.prototype.toString.call(params) === "[object FormData]") {
  //       // formData数据
  //       paramArr.forEach(el => {
  //         url = url.replace("{" + el + "}", params.get(el))
  //       })
  //     } else {
  //       paramArr.forEach(el => {
  //         url = url.replace("{" + el + "}", params[el])
  //       })
  //     }
  //   }
  let paramArr = url.match(/\{.*?\}/gi);
  if (paramArr && paramArr.length) {
    if (Object.prototype.toString.call(params) === "[object FormData]") {
      // formData数据
      paramArr.forEach(el => {
        let key = el.substring(1, el.length - 1); // 去掉左右 { } 边界符
        url = url.replace(el, params.get(key));
      });
    } else {
      paramArr.forEach(el => {
        let key = el.substring(1, el.length - 1);
        url = url.replace(el, params[key]);
      });
    }
  }

  return url;
}

// 退出登录
function logout() {
  sessionStorage.clear();
  Cookies.remove("token");
  store.commit("setUserName", undefined);
  store.commit("setUserId", undefined);
  store.commit("setIsSuperUser", undefined); // 保存是否超级管理员用户标识
  store.commit("setUserName", ""); // 保存用户姓名
  store.commit("setMenuRouteLoadStatus", false); // 重置导航菜单加载状态为false
  store.commit("updateMainTabs", []); // 关闭所有tab页

  router.push("/login");
}

// 刷新token
function refreshToken(requestData) {
  if (!isRefreshing) {
    isRefreshing = true;
    request({
      url: "/api-token-auth/",
      method: "post",
      data: requestData
    })
      .then(res => {
        if (res.success) {
          Cookies.set("token", res.token); // 保存token到Cookie
          Message.info("token过期，请重试");
        } else {
          Message.error(res.msg);
          logout();
        }
        isRefreshing = false;
      })
      .catch(error => {
        isRefreshing = false;
      });
  }
}

export default { request };
