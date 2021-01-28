<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTabBodyHeight">
        <div class="test-info-wrapper" ref="topInfo">
            <span class="span-font">测试计划 / ID：{{planRow.id}}</span>
            <span class="span-font">
                [&nbsp;状态：
                <span class="test-info-text">{{planRow.status}}</span>&nbsp;&nbsp;进度：
                <span
                    class="test-info-text"
                >{{Math.round(planRow.caseNumRelated ? (planRow.caseNumExecuted - planRow.caseNumBlocked)/planRow.caseNumRelated*100:0)}}%({{planRow.caseNumExecuted - planRow.caseNumBlocked}}/{{planRow.caseNumRelated}})</span>&nbsp;&nbsp;通过率：
                <span
                    class="test-info-text"
                >{{Math.round(planRow.caseNumRelated ? planRow.caseNumSuccess/planRow.caseNumRelated*100:0)}}%({{planRow.caseNumSuccess}}/{{planRow.caseNumRelated}})</span>&nbsp;&nbsp;失败率：<span
                    class="test-info-text"
                >{{Math.round(planRow.caseNumRelated ? planRow.caseNumFail/planRow.caseNumRelated*100:0)}}%({{planRow.caseNumFail}}/{{planRow.caseNumRelated}})</span>&nbsp;&nbsp;阻塞率：<span
                    class="test-info-text"
                >{{Math.round(planRow.caseNumRelated ? planRow.caseNumBlocked/planRow.caseNumRelated*100:0)}}%({{planRow.caseNumBlocked}}/{{planRow.caseNumRelated}})</span>&nbsp;&nbsp;未执行：<span
                    class="test-info-text"
                >{{planRow.caseNumRelated - planRow.caseNumExecuted}}</span>&nbsp;]
            </span>
            <!--展开/折叠开关-->
            <span
                @click.prevent="togglePlanBaseInfo"
                style="height:32px; line-height: 32px;font-size:14px; color: #606266;"
            >
                <i class="el-icon-arrow-up el-icon--right" v-show="!planBaseInfoCollapsed">收起</i>
                <i class="el-icon-arrow-down el-icon--right" v-show="planBaseInfoCollapsed">展开</i>
            </span>
            <span class="span-font close-icon-span" @click.prevent="closePage">
                <i class="el-icon-back">返回上级</i>
            </span>
        </div>

        <!-- 计划基础信息 -->
        <div class="plan-base-info" ref="planBaseInfo" v-if="!planBaseInfoCollapsed">
            <table>
                <thead>
                    <tr>
                        <th style="border:none;width:30%;height:0px"></th>
                        <th style="border:none;width:15%;height:0px"></th>
                        <th style="border:none;width:20%;height:0px"></th>
                        <th style="border:none;width:20%;height:0px"></th>
                        <!-- <th style="border:none;width:10%;height:0px"></th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <label>计划名称：</label>
                            <div>{{planRow.name}}</div>
                        </td>
                        <td>
                            <label>创建人：</label>
                            <div>{{planRow.createrName}}</div>
                        </td>

                        <td>
                            <label>预估开始日期：</label>
                            <div>{{planRow.beginTime}}</div>
                        </td>

                        <td>
                            <label>预估完成日期：</label>
                            <div>{{planRow.endTime}}</div>
                        </td>
                    </tr>

                    <tr>
                        <!-- <td>
                                <label>迭代版本：</label>
                                <div
                                   
                                >{{planRow.sprint}}</div>
                        </td>-->
                        <td>
                            <label>执行环境：</label>
                            <div>{{planRow.envNames}}</div>
                        </td>
                        <td>
                            <label>创建时间：</label>
                            <div>{{planRow.createTime}}</div>
                        </td>
                        <td>
                            <label>实际开始时间：</label>
                            <div>{{planRow.startTime}}</div>
                        </td>
                        <td>
                            <label>实际完成时间：</label>
                            <div>{{planRow.finishTime}}</div>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <label>计划描述：</label>
                            <div style="font-size:12px">{{planRow.desc}}</div>
                        </td>
                        <td colspan="2">
                            <label>关联项目：</label>
                            <div style="font-size:12px">{{planRow.projectNames}}</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="plan-related-tabs" ref="planRelatedTabs" v-resize="setTabBodyHeight">
            <!-- 如果不设置type="border-card"，tab底部的激活条el-tabs__active-bar位置和长度显示会有问题-->
            <el-tabs
                v-model="defaultActiveTabPaneName"
                @tab-click="onTabClicked"
                type="border-card"
            >
                <el-tab-pane label="测试用例" name="caseList">
                    <test-plan-case-list-tab
                        v-if="displayTestPlanCaseListTab"
                        v-show="showPlanRelatedTabs"
                        :sprintID="planRow.sprintId"
                        :planRow="planRow"
                        ref="testPlanCaseListTab"
                    ></test-plan-case-list-tab>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
import TestPlanCaseListTab from "./TestPlanCaseListTab";

export default {
    props: ["planRow", "planDetailVisible"],
    components: {
        TestPlanCaseListTab,
    },
    data() {
        return {
            defaultActiveTabPaneName: "caseList", // 默认激活的tab名称
            displayTestPlanCaseListTab: true, // 标记是否加载测试用例tab
            planBaseInfoCollapsed: true, // 标记是否折叠计划详情基础信息
            showPlanRelatedTabs: true, // 标记是否显示计划详情页tab页
        };
    },
    mounted() {
        this.$nextTick(() => {
            this.setTabBodyHeight(); // 设置tab body高度
        });
    },
    methods: {
        // 设置tab body高度
        setTabBodyHeight() {
            let viewWrapper = this.$refs.viewWrapper;
            let topInfo = this.$refs.topInfo;
            let planBaseInfo = this.$refs.planBaseInfo;
            let planBaseInfoOffsetHeight = 0;
            let planRelatedTabs = this.$refs.planRelatedTabs;

            if (planBaseInfo) {
                planBaseInfoOffsetHeight = planBaseInfo.offsetHeight;
            }

            if (planRelatedTabs && topInfo && planRelatedTabs) {
                let h =
                    viewWrapper.offsetHeight -
                    topInfo.offsetHeight -
                    planBaseInfoOffsetHeight -
                    31 - // 31 plan-related-tabs占的高度
                    10 - // 10 为margin 总和
                    30; // el-tabs__content 上下padding之和

                planRelatedTabs.getElementsByClassName(
                    "el-tabs__content"
                )[0].style.height = h + "px";
            }
        },
        closePage() {
            this.$emit("update:planDetailVisible", false); // 关闭对话框
        },
        // 测试用例、缺陷列表、测试报告被点击后的事件处理函数
        onTabClicked(tab, event) {
            this.displayTestPlanCaseListTab = true;
        },
        // 折叠/展开测试计划详情基础信息
        togglePlanBaseInfo() {
            this.planBaseInfoCollapsed = !this.planBaseInfoCollapsed;
            this.showPlanRelatedTabs = false;
            this.$nextTick(() => {
                this.showPlanRelatedTabs = true;
                this.setTabBodyHeight();
                this.$refs.testPlanCaseListTab.$refs.rightElement.setTableBodySize();
            });
        },
    },
};
</script>

<style lang="scss">
.test-info-wrapper {
    margin: 5px 0px 5px 0px;
    line-height: 30px;
    height: 30px;
    background: #f2f3f7;
    border-style: solid;
    border-width: 1px;
    border-color: rgba(172, 167, 167, 0.3);
    .close-icon-span {
        float: right;
        margin-right: 5px;
    }
}
.test-info-text {
    color: #00a8b3;
}

/* 计划基础信息*/
.plan-base-info {
    border-style: solid;
    border-width: 1px;
    border-color: rgba(172, 167, 167, 0.3);
    background: rgb(241, 239, 239);
    td {
        padding-top: 5px;
        padding-bottom: 5px;
        label {
            font-size: 14px;
            color: #606266;
        }
        div {
            display: inline;
            font-size: 14px;
        }
    }
}
</style>