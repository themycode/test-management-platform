// 获取迭代关联的测试计划
export function sprintTestPlans() {
  const result = {
    code: 200,
    msg: "",
    success: true,
    data: [
      {
        id: 1, //计划ID
        name: "询价-测试计划1", // 计划名称
        beginTime: "2019-06-27 10:21:22", //预估开始时间
        startTime: "2019-06-28 10:21:22", //实际开始时间
        endTime: "2019-07-21 10:21:22", //预估完成时间
        finishTime: "2019-07-21 10:21:22", //实际完成时间
        group: "订单,结算,询价,App,微信,商家,商品", //所属组别
        environment: "测试环境" //执行环境
      },
      {
        id: 2,
        name: "订单-测试计划1",
        beginTime: "2019-06-27 10:21:22",
        startTime: "2019-06-28 10:21:22",
        endTime: "2019-07-21 10:21:22",
        finishTime: "2019-07-21 10:21:22",
        group: "订单,结算,询价,微信,商家,商品",
        environment: "生产环境"
      }
    ]
  }
  return {
    url: "/api/v1/sprintTestPlans",
    method: "get",
    data: result
  }
}

// 生成测试报告
export function addSprintTestReport() {
  const result = {
    code: 200,
    msg: "生成测试报告成功",
    success: true,
    data: {
      id: 4, // 报告唯一ID
      title: "新增迭代Sprint100测试报告20190627095244ID1", // 报告名称
      // 引言
      introduction: "迭代Sprint100测试结果进行汇总，使团队能通过报告了解测试情况，在上线前处理好迭代风险",
      relatedPlans: [
        // 关联的测试计划
        {
          id: 1, //计划ID
          name: "询价-测试计划1", // 计划名称
          beginTime: "2019-06-27 10:21:22", //预估开始时间
          startTime: "2019-06-28 10:21:22", //实际开始时间
          endTime: "2019-07-21 10:21:22", //预估完成时间
          finishTime: "2019-07-21 10:21:22", //实际完成时间
          group: "订单,结算,询价,App,微信,商家,商品", //所属组别
          environment: "测试环境" //执行环境
        },
        {
          id: 2,
          name: "订单-测试计划1",
          beginTime: "2019-06-27 10:21:22",
          startTime: "2019-06-28 10:21:22",
          endTime: "2019-07-21 10:21:22",
          finishTime: "2019-07-21 10:21:22",
          group: "订单,结算,询价,微信,商家,商品",
          environment: "生产环境"
        }
      ],
      testScope: "", //测试范围
      // 需求覆盖饼图统计数据
      requirementPie: {
        centerText: "80.95%\n覆盖率", // 饼图中心的文字// 需求覆盖率
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 5, name: "未测试" },
          { value: 11, name: "测试中" },
          { value: 10, name: "已完成" }
        ]
      },
      // 缺陷状态图统计数据
      defectStatusPie: {
        centerText: "59.99%\n消缺率", //缺陷总数
        seriesData: [
          // 缺陷级别饼图统计数据,数据顺序不能变
          { value: 15, name: "激活" },
          { value: 50, name: "已关闭" },
          { value: 10, name: "已解决" }
        ]
      },

      // 缺陷级别饼图统计数据
      defectLevelPie: {
        centerText: "22\n总数", //缺陷总数
        seriesData: [
          // 缺陷级别饼图统计数据,数据顺序不能变
          { value: 1, name: "致命" },
          { value: 5, name: "严重" },
          { value: 10, name: "一般" },
          { value: 5, name: "轻微" }
        ]
      },
      // 用例通过率饼图统计数据
      casePassRatePie: {
        centerText: "99.00%\n通过率", //已通过用例数/用例总数
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 1, name: "通过" },
          { value: 5, name: "失败+阻塞+未执行" }
        ]
      },
      // 用例状态饼图统计数据
      caseStatusPie: {
        centerText: "95.00%\n执行率", // 已执行用例数/用例总数
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 1, name: "通过" },
          { value: 5, name: "失败" },
          { value: 10, name: "阻塞" },
          { value: 5, name: "未执行" }
        ]
      },
      // 个人测试情况统计
      
      
      personalTestInfo: [
        {
          id: 1, // 数据库自增ID
          userName: "上官某人", //用户名称
          caseNum: "100", // 分配用例数//目前为创建用例数
          bugNum: "90", // 提交bug数
          caseNumExecuted: "80", // 执行用例数
          caseExecutionRate: "80.00%", // 用例执行率
          casePassRate: "99.00%" // 用例通过率
        },
        {
          id: 2,
          userName: "赖晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "70",
          caseExecutionRate: "70.00%",
          casePassRate: "99.00%"
        },
        {
          id: 3,
          userName: "赖小晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "60",
          caseExecutionRate: "60.00%",
          casePassRate: "99.00%"
        },
        {
          id: 4,
          userName: "赖某人",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },

        {
          id: 5,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 6,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 7,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 8,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 9,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        }
      ],
      // 组别测试情况统计
      
      groupTestInfo: [
        {
          id: 1, // 数据库自增ID
          groupName: "订单", //组别名称
          caseNum: "100", // 分配用例数//目前为创建用例数
          bugNum: "90", // 提交bug数
          caseNumExecuted: "80", // 执行用例数
          caseExecutionRate: "80.00%", // 用例执行率
          casePassRate: "99.00%" // 用例通过率
        },
        {
          id: 2,
          groupName: "商品",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "70",
          caseExecutionRate: "70.00%",
          casePassRate: "99.00%"
        },
        {
          id: 3,
          groupName: "询价",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "60",
          caseExecutionRate: "60.00%",
          casePassRate: "99.00%"
        },
        {
          id: 4,
          groupName: "终端",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },

        {
          id: 5,
          groupName: "APP",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 6,
          groupName: "小马",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 7,
          groupName: "物流",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 8,
          groupName: "商城",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 9,
          groupName: "其它",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        }
      ],
      // 组别缺陷状态统计
      groupDefectStatusBar: {
        xAxisData: ["AIM", "APP", "会员", "基础数据", "备货", "广州H5团队", "开思助手", "结算"],
        seriesData: [
          {
            name: "新建",
            type: "bar",
            barWidth: "50", // 柱状条宽度
            stack: "groupDefect",

            data: [320, 332, 301, 334, 390, 330, 320]
          },
          {
            name: "接受/处理",
            type: "bar",
            stack: "groupDefect",
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: "已解决",
            type: "bar",
            stack: "groupDefect",
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: "已验证",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "重新打开",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "已拒绝",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "已关闭",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          }
        ]
      },
      // 组别缺陷趋势图统计
      groupDefectTrendLine: {
        xAxisData: [
          "2019-03-25",
          "2019-03-26",
          "2019-03-27",
          "2019-03-28",
          "2019-03-29",
          "2019-03-29",
          "2019-03-30",
          "2019-04-01",
          "2019-04-02",
          "2019-04-03"
        ],
        seriesData: {
          全部: [
            {
              name: "缺陷总数",
              type: "line",
              stack: "groupDefect",

              data: [30, 32, 101, 120, 110, 150, 360, 380, 350, 320]
            },
            {
              name: "新增缺陷数",
              type: "line",
              stack: "groupDefect",
              data: [10, 5, 6, 20, 90, 30, 40, 90, 30, 40]
            },
            {
              name: "遗留DI值",
              type: "line",
              stack: "groupDefect",
              data: [220, 182, 191, 234, 290, 330, 310, 290, 330, 310]
            }
          ],
          AIM: [
            {
              name: "缺陷总数",
              type: "line",
              barWidth: "50", // 柱状条宽度
              stack: "groupDefect",

              data: [29, 31, 100, 110, 109, 150, 360, 380, 350, 320]
            },
            {
              name: "当日新增缺陷数",
              type: "line",
              stack: "groupDefect",
              data: [10, 5, 6, 20, 90, 30, 40, 90, 30, 40]
            },
            {
              name: "遗留DI值",
              type: "line",
              stack: "groupDefect",
              data: [220, 180, 191, 234, 290, 330, 310, 290, 330, 310]
            }
          ]
        }
      },
      //遗留未关闭缺陷
      unclosedDefects: [
        {
          id: 1, // 数据库自增ID
          bugID: 1,
          name: "输入用户BBB和密码123无法正常登录",
          severityLevel: "严重",
          status: "已解决",
          handler: "处理人",
          creater: "提交人"
        },
        {
          id: 2,
          bugID: 2,
          name: "输入进行模糊搜索，结果不正确",
          severityLevel: "一般",
          status: "未解决",
          handler: "林某某",
          creater: "上官某人"
        },
        {
          id: 3,
          bugID: 3,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        },
        {
          id: 4,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某",
          relatedCases: []
        },
        {
          id: 5,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某",
          relatedCases: []
        },
        {
          id: 6,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        },
        {
          id: 7,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        }
      ],

      conclusion: "当前遗留DI值为 3 ，测试结果为：不通过", // 测试结论
      suggestion: "", // 相关建议
      riskAnalysis: "" // 风险分析
    }
  }
  return {
    url: "/api/v1/sprintTestReport/add",
    method: "post",
    data: result
  }
}

// 查看测试报告
export function getSprintTestReport() {
  const result = {
    msg: "",
    success: true,
    data: {
      id: 1, // 报告唯一ID
      title: "迭代Sprint100测试报告20190627095244ID1", // 报告名称
      // 引言
      introduction: "迭代Sprint100测试结果进行汇总，使团队能通过报告了解测试情况，在上线前处理好迭代风险",
      relatedPlans: [
        // 关联的测试计划
        {
          id: 1, //计划ID
          name: "询价-测试计划1", // 计划名称
          beginTime: "2019-06-27 10:21:22", //预估开始时间
          startTime: "2019-06-28 10:21:22", //实际开始时间
          endTime: "2019-07-21 10:21:22", //预估完成时间
          finishTime: "2019-07-21 10:21:22", //实际完成时间
          group: "订单,结算,询价,App,微信,商家,商品", //所属组别
          environment: "测试环境" //执行环境
        },
        {
          id: 2,
          name: "订单-测试计划1",
          beginTime: "2019-06-27 10:21:22",
          startTime: "2019-06-28 10:21:22",
          endTime: "2019-07-21 10:21:22",
          finishTime: "2019-07-21 10:21:22",
          group: "订单,结算,询价,微信,商家,商品",
          environment: "生产环境"
        }
      ],
      testScope: "", //测试范围
      // 需求覆盖饼图统计数据
      requirementPie: {
        centerText: "80.95%\n覆盖率", // 饼图中心的文字// 需求覆盖率
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 5, name: "未测试" },
          { value: 11, name: "测试中" },
          { value: 10, name: "已完成" }
        ]
      },
      // 缺陷状态图统计数据
      defectStatusPie: {
        centerText: "59.99%\n缺陷消除率", //缺陷消除率
        seriesData: [
          // 缺陷级别饼图统计数据,数据顺序不能变
          { value: 15, name: "激活" },
          { value: 50, name: "已关闭" },
          { value: 10, name: "已解决" }
        ]
      },

      // 缺陷级别饼图统计数据
      defectLevelPie: {
        centerText: "22\n总数", //缺陷总数
        seriesData: [
          // 缺陷级别饼图统计数据,数据顺序不能变
          { value: 1, name: "致命" },
          { value: 5, name: "严重" },
          { value: 10, name: "一般" },
          { value: 5, name: "轻微" }
        ]
      },
      // 用例通过率饼图统计数据
      casePassRatePie: {
        centerText: "99.00%\n通过率", //已通过用例数/用例总数
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 1, name: "通过" },
          { value: 5, name: "不通过" }
        ]
      },
      // 用例状态饼图统计数据
      caseStatusPie: {
        centerText: "95.00%\n执行率", // 已执行用例数/用例总数
        seriesData: [
          // 缺陷饼图统计数据,数据顺序不能变
          { value: 1, name: "通过" },
          { value: 5, name: "失败" },
          { value: 10, name: "阻塞" },
          { value: 5, name: "未执行" }
        ]
      },
      // 个人测试情况统计
      personalTestInfo: [
        {
          id: 1, // 数据库自增ID
          userName: "上官某人", //用户名称
          caseNum: "100", // 分配用例数//目前为创建用例数
          bugNum: "90", // 提交bug数
          caseNumExecuted: "80", // 执行用例数
          caseExecutionRate: "80.00%", // 用例执行率
          casePassRate: "99.00%" // 用例通过率
        },
        {
          id: 2,
          userName: "赖晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "70",
          caseExecutionRate: "70.00%",
          casePassRate: "99.00%"
        },
        {
          id: 3,
          userName: "赖小晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "60",
          caseExecutionRate: "60.00%",
          casePassRate: "99.00%"
        },
        {
          id: 4,
          userName: "赖某人",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },

        {
          id: 5,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 6,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 7,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 8,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 9,
          userName: "上官晓晓",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        }
      ],
      // 组别测试情况统计
      groupTestInfo: [
        {
          id: 1, // 数据库自增ID
          groupName: "订单", //组别名称
          caseNum: "100", // 分配用例数//目前为创建用例数
          bugNum: "90", // 提交bug数
          caseNumExecuted: "80", // 执行用例数
          caseExecutionRate: "80.00%", // 用例执行率
          casePassRate: "99.00%" // 用例通过率
        },
        {
          id: 2,
          groupName: "商品",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "70",
          caseExecutionRate: "70.00%",
          casePassRate: "99.00%"
        },
        {
          id: 3,
          groupName: "询价",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "60",
          caseExecutionRate: "60.00%",
          casePassRate: "99.00%"
        },
        {
          id: 4,
          groupName: "终端",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },

        {
          id: 5,
          groupName: "APP",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 6,
          groupName: "小马",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 7,
          groupName: "物流",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 8,
          groupName: "商城",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        },
        {
          id: 9,
          groupName: "其它",
          caseNum: "100",
          bugNum: "90",
          caseNumExecuted: "80",
          caseExecutionRate: "80.00%",
          casePassRate: "99.00%"
        }
      ],
      // 组别缺陷状态统计
      groupDefectStatusBar: {
        xAxisData: ["AIM", "APP", "会员", "基础数据", "备货", "广州H5团队", "开思助手", "结算"],
        seriesData: [
          {
            name: "新建",
            type: "bar",
            barWidth: "50", // 柱状条宽度
            stack: "groupDefect",

            data: [320, 332, 301, 334, 390, 330, 320]
          },
          {
            name: "接受/处理",
            type: "bar",
            stack: "groupDefect",
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: "已解决",
            type: "bar",
            stack: "groupDefect",
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: "已验证",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "重新打开",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "已拒绝",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "已关闭",
            type: "bar",
            stack: "groupDefect",
            data: [150, 232, 201, 154, 190, 330, 410]
          }
        ]
      },
      // 组别缺陷趋势图统计
      groupDefectTrendLine: {
        xAxisData: [
          "2019-03-25",
          "2019-03-26",
          "2019-03-27",
          "2019-03-28",
          "2019-03-29",
          "2019-03-29",
          "2019-03-30",
          "2019-04-01",
          "2019-04-02",
          "2019-04-03"
        ],
        seriesData: {
          全部: [
            {
              name: "缺陷总数",
              type: "line",
              barWidth: "50", // 柱状条宽度
              stack: "groupDefect",

              data: [30, 32, 101, 120, 110, 150, 360, 380, 350, 320]
            },
            {
              name: "新增缺陷数",
              type: "line",
              stack: "groupDefect",
              data: [10, 5, 6, 20, 90, 30, 40, 90, 30, 40]
            },
            {
              name: "遗留DI值",
              type: "line",
              stack: "groupDefect",
              data: [220, 182, 191, 234, 290, 330, 310, 290, 330, 310]
            }
          ],
          AIM: [
            {
              name: "缺陷总数",
              type: "line",
              barWidth: "50", // 柱状条宽度
              stack: "groupDefect",

              data: [29, 31, 100, 110, 109, 150, 360, 380, 350, 320]
            },
            {
              name: "新增缺陷数",
              type: "line",
              stack: "groupDefect",
              data: [10, 5, 6, 20, 90, 30, 40, 90, 30, 40]
            },
            {
              name: "遗留DI值",
              type: "line",
              stack: "groupDefect",
              data: [220, 180, 191, 234, 290, 330, 310, 290, 330, 310]
            }
          ]
        }
      },
      //遗留未关闭缺陷
      unclosedDefects: [
        {
          id: 1, // 数据库自增ID
          bugID: 1,
          name: "输入用户BBB和密码123无法正常登录",
          severityLevel: "严重",
          status: "已解决",
          handler: "处理人",
          creater: "提交人"
        },
        {
          id: 2,
          bugID: 2,
          name: "输入进行模糊搜索，结果不正确",
          severityLevel: "一般",
          status: "未解决",
          handler: "林某某",
          creater: "上官某人"
        },
        {
          id: 3,
          bugID: 3,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        },
        {
          id: 4,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某",
          relatedCases: []
        },
        {
          id: 5,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某",
          relatedCases: []
        },
        {
          id: 6,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        },
        {
          id: 7,
          bugID: 4,
          name: "部分产品名称糊搜索结果不存在",
          severityLevel: "轻微",
          status: "已解决",
          handler: "上官某某",
          creater: "林某某"
        }
      ],
      conclusion: "当前遗留DI值为 2 ，测试结果为：通过", // 测试结论
      suggestion: "", // 相关建议
      riskAnalysis: "" // 风险分析
    }
  }
  return {
    url: "/api/v1/sprintTestReportDetail",
    method: "get",
    data: result
  }
}
// 修改迭代报告标题
export function updateReportTitle() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/title/update",
    method: "post",
    data: result
  }
}

// 修改迭代报告引言
export function updateReportIntroduction() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/introduction/update",
    method: "post",
    data: result
  }
}

// 修改迭代报告测试范围
export function updateReportTestScope() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/testScope/update",
    method: "post",
    data: result
  }
}

// 修改迭代报告测试结论
export function updateReportConclusion() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/conclusion/update",
    method: "post",
    data: result
  }
}

// 修改迭代报告相关建议
export function updateReportSuggestion() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/suggestion/update",
    method: "post",
    data: result
  }
}

// 修改迭代报告风险分析
export function updateReportRiskAnalysis() {
  const result = {
    code: 200,
    msg: "修改成功",
    success: true,
    data: {}
  }
  return {
    url: "/api/v1/sprintTestReport/riskAnalysis/update",
    method: "post",
    data: result
  }
}

// 获取迭代关联的测试报告列表
export function getSprintTestReportList() {
  const result = {
    code: 200,
    msg: "",
    success: true,
    data: [
      { id: 1, name: "迭代Sprint100测试报告20190627095244ID1" },
      { id: 2, name: "迭代Sprint100测试报告20190627095244ID2" },
      { id: 3, name: "迭代Sprint100测试报告20190627095244ID3" }
    ]
  }
  return {
    url: "/api/v1/sprintTestReports",
    method: "get",
    data: result
  }
}

// 下载测试报告
export function downloadSprintTestReport() {
  const result = {
    code: 200,
    msg: "",
    success: true,
    data: { fileName: "迭代Sprint100测试报告20190627095244ID1.pdf", fileData: "暂时没法mock"}
  }
  return {
    url: "/api/v1/sprintTestReport/download",
    method: "get",
    data: result
  }
}
