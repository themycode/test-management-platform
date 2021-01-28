(function(env) {
  // 开发环境服务器地址
  var dev = {
    API_BASE_URL: "http://localhost:8000",
    API_REQUEST_TIMEOUT: 180000
  };

  // 线上环境服务器地址
  var prod = {
    API_BASE_URL: "http://10.168.11.88:8000",
    API_REQUEST_TIMEOUT: 180000
  };

  var config = {};
  if (env == "dev") {
    config = dev;
  } else if (env == "prod") {
    config = prod;
  }

  config["headers"] = {
    // 默认请求头
    "Content-Type": "application/json;charset=UTF-8"
  };
  config["withCredentials"] = true; // 请求是否携带凭证配置
  config["responseType"] = "json"; // 默认返回数据类型

  config["indexOfTopNavMenuActive"] = 0; // 默认选中的顶部导航菜单索引
  config["caseAttachmentNumLimit"] = 5; // 允许上传的用例附件数量
  config["caseAttachmentSizeLimit"] = 10; // 允许上传的用例附件大小，单位 M
  config["jiraIssueBrowseBaseUrl"] = "https://jira.casstime.com/browse/EC-"; // jira issue查阅基础地址
  config["zentaoBugBrowseBaseUrl"] = "http://10.171.21.212/zentaopms/www/bug-view-"; // 禅道 bug查阅基础地址
  return config;
})("dev");
