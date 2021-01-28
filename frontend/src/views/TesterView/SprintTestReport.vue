<template>
    <!-- 不知道为啥，div上添加class="view-warpper" 不起作用，必须使用style -->
    <div
        v-resize="setSprintReportTopPos"
        v-loading="loading"
        :element-loading-text="elementLoadingText"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        style="
            position: absolute;
            left: 0px;
            right: 0px;
            top: 0px;
            bottom: 0px;
            overflow: hidden;
        "
    >
        <div class="common-top-bar-wrapper" ref="topPannel">
            <span>产品</span>
            <el-select
                v-model="productSelected"
                ref="sprintProductSelector"
                filterable
                size="small"
                collapse-tags
                placeholder="输入关键词搜索产品"
                @change="onProductChange"
                style="width: 14%"
            >
                <el-option
                    v-for="item in productOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                ></el-option>
            </el-select>
            <span>&nbsp;迭代</span>
            <el-select
                v-model="sprintSelected"
                filterable
                size="small"
                placeholder="输入关键词搜索迭代"
                @change="onSprintChange"
                style="width: 12%"
            >
                <el-option
                    v-for="item in sprintOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                ></el-option>
            </el-select>
            <span>&nbsp;测试计划</span>
            <el-select
                v-model="plansSelected"
                value-key="id"
                ref="testplanSelector"
                filterable
                clearable
                :multiple="true"
                size="small"
                collapse-tags
                placeholder="输入关键词搜索计划"
                @change="onPlanChange"
                style="width: 15%"
            >
                <el-option
                    v-for="item in planOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item"
                ></el-option>
            </el-select>
            <span>&nbsp;缺陷归属项目</span>
            <el-select
                v-model="projectsSelected"
                value-key="id"
                ref="projectSelector"
                filterable
                clearable
                :multiple="true"
                size="small"
                collapse-tags
                placeholder="输入关键词搜索项目"
                @change="onProjectChange"
                style="width: 15%"
            >
                <el-option
                    v-for="item in projectOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item"
                ></el-option>
            </el-select>
            <span>&nbsp;缺陷归属项目版本</span>
            <el-select
                v-model="projectVersionsSelected"
                value-key="id"
                ref="projectVersionSelector"
                filterable
                clearable
                :multiple="true"
                size="small"
                collapse-tags
                placeholder="输入关键词搜索项目版本"
                @change="onProjectVersionChange"
                style="width: 13%"
            >
                <el-option
                    v-for="item in projectVersionOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item"
                ></el-option>
            </el-select>
            <el-button size="small" type="primary" @click="getReportStatistics"
                >查询</el-button
            >
            <el-button
                size="small"
                type="primary"
                @click="generateSprintTestReport"
                :disabled="ifDisableGenerateReportBtn"
                >生成报告</el-button
            >
            <span>查看报告</span>
            <el-select
                v-model="reportId"
                filterable
                clearable
                :multiple="false"
                size="small"
                placeholder="输入关键词查找测试报告或者下拉选取测试报告"
                @change="onReportChange"
                style="width: 25%"
            >
                <el-option
                    v-for="item in sprintReports"
                    :key="item.id"
                    :label="item.title"
                    :value="item.id"
                ></el-option>
            </el-select>

            <el-button
                size="small"
                type="primary"
                @click="downloadSprintTestReport"
                >下载报告</el-button
            >
            <el-button size="small" type="primary" @click="sendSprintTestReport"
                >发送报告</el-button
            >
        </div>

        <!-- 迭代测试报告 -->
        <div class="sprint-test-report-content" ref="sprintReport">
            <div style="height: 100%" v-if="showReport">
                <!-- 标题 -->
                <div class="report-title report-session" v-if="!showDataFromQuery">
                    <div v-if="!editing.title">
                        <span>{{ reportInfo.title }}</span>
                        <i
                            v-if="showEditableItem"
                            class="el-icon-edit"
                            @click="editReportItem('title')"
                        ></i>
                    </div>
                    <div v-else>
                        <el-input
                            ref="title"
                            type="text"
                            placeholder="请输入测试报告标题"
                            v-model="reportInfo.title"
                            maxlength="100"
                            size="small"
                            show-word-limit
                            @blur="onEditingBlur('title')"
                        ></el-input>
                    </div>
                </div>

                <!-- 引言 -->
                <div class="report-session" v-if="!showDataFromQuery">
                    <span class="report-session-title">引言：</span>
                    <div v-if="!editing.introduction">
                        <span class="hand-input-content pre-text">{{
                            reportInfo.introduction
                        }}</span>
                        <i
                            v-if="showEditableItem"
                            class="el-icon-edit"
                            @click="editReportItem('introduction')"
                        ></i>
                    </div>
                    <div v-else>
                        <el-input
                            ref="introduction"
                            type="textarea"
                            placeholder="请输入测试报告引言"
                            v-model="reportInfo.introduction"
                            maxlength="1000"
                            size="small"
                            show-word-limit
                            @blur="onEditingBlur('introduction')"
                        ></el-input>
                    </div>
                </div>
                <div class="report-session" v-if="!showDataFromQuery">
                    <div class="report-session-title">概述</div>             
                    <div class="report-sub-session">
                        <div class="report-sub-session-title">测试结论</div>
                        <div v-if="!editing.conclusion">
                            <span class="hand-input-content pre-text">{{
                                reportInfo.conclusion
                            }}</span>
                            <i
                                v-if="showEditableItem"
                                class="el-icon-edit"
                                @click="editReportItem('conclusion')"
                            ></i>
                        </div>
                        <div v-if="editing.conclusion">
                            <el-input
                                ref="conclusion"
                                type="textarea"
                                :autosize="{ minRows: 5 }"
                                placeholder="请输入测试结论"
                                v-model="reportInfo.conclusion"
                                maxlength="1000"
                                size="small"
                                show-word-limit
                                @blur="onEditingBlur('conclusion')"
                            ></el-input>
                        </div>
                    </div>
                    <div class="report-sub-session">
                        <div class="report-sub-session-title">相关建议</div>
                        <div v-if="!editing.suggestion">
                            <span class="hand-input-content pre-text">{{
                                reportInfo.suggestion
                            }}</span>
                            <i
                                v-if="showEditableItem"
                                class="el-icon-edit"
                                @click="editReportItem('suggestion')"
                            ></i>
                        </div>
                        <div v-if="editing.suggestion">
                            <el-input
                                ref="suggestion"
                                type="textarea"
                                :autosize="{ minRows: 5 }"
                                placeholder="请输入相关建议"
                                v-model="reportInfo.suggestion"
                                maxlength="1000"
                                size="small"
                                show-word-limit
                                @blur="onEditingBlur('suggestion')"
                            ></el-input>
                        </div>
                    </div>
                    <div class="report-sub-session" style="border-bottom-width: 0px;">
                        <div class="report-sub-session-title">风险分析</div>
                        <div v-if="!editing.riskAnalysis">
                            <span class="hand-input-content pre-text">{{
                                reportInfo.riskAnalysis
                            }}</span>
                            <i
                                v-if="showEditableItem"
                                class="el-icon-edit"
                                @click="editReportItem('riskAnalysis')"
                            ></i>
                        </div>
                        <div v-if="editing.riskAnalysis">
                            <el-input
                                ref="riskAnalysis"
                                type="textarea"
                                :autosize="{ minRows: 5 }"
                                placeholder="请输入存在的风险"
                                v-model="reportInfo.riskAnalysis"
                                maxlength="1000"
                                size="small"
                                show-word-limit
                                @blur="onEditingBlur('riskAnalysis')"
                            ></el-input>
                        </div>
                    </div>
                </div>
                <div class="report-session" v-if="!showDataFromQuery">
                    <span class="report-session-title">测试范围</span>
                    <div v-if="!editing.testScope">
                        <span class="hand-input-content pre-text">{{
                            reportInfo.testScope
                        }}</span>
                        <i
                            v-if="showEditableItem"
                            class="el-icon-edit"
                            @click="editReportItem('testScope')"
                        ></i>
                    </div>
                    <div v-if="editing.testScope">
                        <el-input
                            ref="testScope"
                            type="textarea"
                            placeholder="请输入迭代测试范围"
                            v-model="reportInfo.testScope"
                            maxlength="1000"
                            size="small"
                            show-word-limit
                            @blur="onEditingBlur('testScope')"
                        ></el-input>
                    </div>
                </div>
                <div class="report-session">
                    <span class="report-session-title">测试计划</span>
                    <div class="plan-table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <!-- <th style="border:none;width:5%;height:0px">ID</th> -->
                                    <th style="border: none; width: 16%">
                                        计划名称
                                    </th>
                                    <th style="border: none; width: 7%">
                                        预估开始日期
                                    </th>
                                    <th style="border: none; width: 9%">
                                        实际开始时间
                                    </th>
                                    <th style="border: none; width: 7%">
                                        预估完成日期
                                    </th>
                                    <th style="border: none; width: 9%">
                                        实际完成时间
                                    </th>
                                    <th style="border: none; width: 4%">
                                        状态
                                    </th>
                                    <th style="border: none; width: 8%">
                                        测试进度
                                    </th>
                                    <th style="border: none; width: 8%">
                                        通过率
                                    </th>
                                    <th style="border: none; width: 5%">
                                        失败
                                    </th>
                                    <th style="border: none; width: 5%">
                                        阻塞
                                    </th>
                                    <th style="border: none; width: 5%">
                                        未执行
                                    </th>
                                    <th style="border: none; width: 9%">
                                        关联项目
                                    </th>
                                    <th style="border: none; width: 8%">
                                        测试环境
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="plan in reportInfo.relatedPlans"
                                    :key="plan.id"
                                >
                                    <!-- <td>
                                    <div>{{plan.id}}</div>
                                </td>-->
                                    <td style="text-align: left">
                                        <div>{{ plan.name }}</div>
                                    </td>
                                    <td>
                                        <div>{{ plan.beginTime }}</div>
                                    </td>
                                    <td>
                                        <div>{{ plan.startTime }}</div>
                                    </td>
                                    <td>
                                        <div>{{ plan.endTime }}</div>
                                    </td>
                                    <td>
                                        <div>{{ plan.finishTime }}</div>
                                    </td>
                                    <td>
                                        <div>{{ plan.status }}</div>
                                    </td>
                                    <td>
                                        <div>
                                            {{ plan.progress }}%({{
                                                plan.caseNumExecuted
                                            }}/{{ plan.caseNumRelated }})
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            {{ plan.passRate }}%({{
                                                plan.caseNumSuccess
                                            }}/{{ plan.caseNumRelated }})
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            {{ plan.caseNumFail }}
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            {{ plan.caseNumBlocked }}
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            {{ plan.caseNumRelated - plan.caseNumExecuted }}                                              
                                        </div>
                                    </td>                                    
                                    <td style="text-align: left">
                                        <div>{{ plan.projectNames }}</div>
                                    </td>
                                    <td style="text-align: left">
                                        <div>{{ plan.envNames }}</div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- 测试统计 -->
                <div class="report-session">
                    <span class="report-session-title">测试统计</span>
                    <!-- 统计饼图 -->
                    <div class="report-sub-session">
                        <!-- 需求覆盖统计饼图 -->
                        <!-- <doughnut-pie-chart
                        :pieData="reportInfo.requirementPie"
                        :pieColor="requirementPie.color"
                        :pieTitle="requirementPie.title"
                        class="doughnut-pie-chart"
                    ></doughnut-pie-chart>-->
                        <!-- 缺陷状态统计饼图 -->
                        <doughnut-pie-chart
                            :pieData="reportInfo.defectStatusPie"
                            :pieColor="defectStatusPie.color"
                            :pieTitle="defectStatusPie.title"
                            :echartPicIdDict="echartPicIdDict"
                            :showLabel="false"
                            keyForEchartId="defectStatusPie"
                            class="doughnut-pie-chart"
                        ></doughnut-pie-chart>
                        <!-- 缺陷严重级别统计饼图 -->
                        <doughnut-pie-chart
                            :pieData="reportInfo.defectSeverityPie"
                            :pieColor="defectSeverityPie.color"
                            :pieTitle="defectSeverityPie.title"
                            :echartPicIdDict="echartPicIdDict"
                            :showLabel="false"
                            keyForEchartId="defectSeverityPie"
                            class="doughnut-pie-chart"
                        ></doughnut-pie-chart>

                        <!-- 缺陷类型统计饼图 -->
                        <doughnut-pie-chart
                            :pieData="reportInfo.defectTypePie"
                            :pieColor="defectTypePie.color"
                            :pieTitle="defectTypePie.title"
                            :echartPicIdDict="echartPicIdDict"
                            :showLabel="false"
                            keyForEchartId="defectTypePie"
                            class="doughnut-pie-chart"
                        ></doughnut-pie-chart>

                        <!-- 用例通过率统计饼图 -->
                        <doughnut-pie-chart
                            :pieData="reportInfo.caseExecutionPie"
                            :pieColor="caseExecutionPie.color"
                            :pieTitle="caseExecutionPie.title"
                            :showLabel="false"
                            class="doughnut-pie-chart"
                            keyForEchartId="caseExecutionPie"
                            :echartPicIdDict="echartPicIdDict"
                        ></doughnut-pie-chart>

                        <div class="terminology-wrapper">
                            <span>名词解释</span>
                            <br />

                            <span class="terminology" style="margin-left: 0px"
                                >消缺率：</span
                            >
                            <span>"已关闭"缺陷数/缺陷总数 * 100</span>
                            <span class="terminology">已拒绝：</span>
                            <span>扭转状态除外，不对缺陷做任何处理</span>
                            <span class="terminology">重新打开：</span>
                            <span>缺陷关闭后被再次打开</span>
                            <span class="terminology">通过率：</span>
                            <span>"通过"用例数/用例总数 * 100</span>
                            <span class="terminology">执行率：</span>
                            <span
                                >(用例总数-"未执行"用例数)/用例总数 * 100</span
                            >
                        </div>
                    </div>
                    <div
                        v-if="reportInfo.defectSourceBar.seriesData.length"
                        class="report-sub-session"
                    >
                        <div class="report-sub-session-title">
                            缺陷根源分组统计
                        </div>
                        <stacked-column-chart
                            :barData="reportInfo.defectSourceBar"
                            class="stacked-column-chart"
                            :echartPicIdDict="echartPicIdDict"
                            keyForEchartId="defectSourceBar"
                            yAxisType="category"
                            xAxisType="value"
                        ></stacked-column-chart>
                    </div>

                    <!-- 个人用例执行统计 -->
                    <div class="report-sub-session">
                        <div class="report-sub-session-title">
                            个人用例执行统计
                        </div>
                        <case-execution-individual-statistics
                            :caseExecutionIndividual="
                                reportInfo.caseExecutionIndividual
                            "
                        ></case-execution-individual-statistics>
                        <div class="terminology-wrapper">
                            <span>名词解释</span>
                            <br />
                            <span class="terminology" style="margin-left: 0px"
                                >用例执行率：</span
                            >
                            <span
                                >("分配用例数"-"执行用例数")/"分配用例数" *
                                100</span
                            >&nbsp;&nbsp;&nbsp;&nbsp;
                            <span class="terminology">用例通过率：</span>
                            <span>"通过用例数"/"执行用例数" * 100</span
                            >&nbsp;&nbsp;&nbsp;&nbsp;
                            <br />
                            <span class="terminology" style="margin-left: 0px"
                                >说明：</span
                            >
                            <span>全部统计项都为0的用户不显示</span>
                        </div>
                    </div>
                    <!-- 个人缺陷提交统计 -->
                    <div class="report-sub-session">
                        <div class="report-sub-session-title">
                            个人缺陷提交统计
                        </div>
                        <defect-created-individual-statistics
                            :defectsCreatedIndividual="
                                reportInfo.defectsCreatedIndividual
                            "
                        ></defect-created-individual-statistics>
                    </div>

                    <!-- 个人缺陷处理统计 -->
                    <div class="report-sub-session">
                        <div class="report-sub-session-title">
                            个人缺陷处理统计
                        </div>
                        <defect-resolved-individual-statistics
                            :defectsResolvedIndividual="
                                reportInfo.defectsResolvedIndividual
                            "
                        ></defect-resolved-individual-statistics>
                        <div class="terminology-wrapper">
                            <span class="terminology" style="margin-left: 0px"
                                >说明：</span
                            >
                            <span
                                >以上缺陷密度值为“引发缺陷数”的缺陷DI值统计；致命，严重，一般，轻微缺陷数为“引发缺陷数”的细分统计</span
                            >
                        </div>
                    </div>

                    <!-- 遗留缺陷统计 -->
                    <div>
                        <div class="report-sub-session-title">遗留缺陷列表</div>
                        <unclosed-defect-table
                            :unclosedDefects="reportInfo.unclosedDefects"
                        ></unclosed-defect-table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DefectResolvedIndividualStatistics from "./SprintTestReport/DefectResolvedIndividualStatistics";
import DefectCreatedIndividualStatistics from "./SprintTestReport/DefectCreatedIndividualStatistics";
import CaseExecutionIndividualStatistics from "./SprintTestReport/CaseExecutionIndividualStatistics";
import UnclosedDefectTable from "./SprintTestReport/UnclosedDefectTable";
import DoughnutPieChart from "@/common/components/MyEcharts/DoughnutPieChart";
import StackedColumnChart from "@/common/components/MyEcharts/StackedColumnChart";

export default {
    components: {
        DoughnutPieChart,
        StackedColumnChart,
        DefectCreatedIndividualStatistics,
        DefectResolvedIndividualStatistics,
        CaseExecutionIndividualStatistics,
        UnclosedDefectTable,
    },
    data() {
        // 缺陷明细状态颜色 新建-DarkRed 已确认-DarkMagenta	已拒绝 -DarkOrange  延期处理-DimGrey 已解决-YellowGreen	已验证-LimeGreen 重新打开-VioletRed1  已关闭-ForestGreen
        let defectStatusColor = {
            新建: "#8B0000",
            处理中: "#8B008B",
            延期处理: "#696969",
            已解决: "#9ACD32",
            已拒绝: "#FF8C00",
            已关闭: "#228B22",
            重新打开: "#FF3E96",
        };

        return {
            echartPicIdDict: {}, // 存放echart图表ID
            productOptions: [], // 存放产品列表
            productSelected: "", // 存放用户所选择的产品ID
            sprintOptions: [], // sprint选取框下拉列表
            sprintSelected: "", // 存放用户选择的迭代ID
            planOptions: [], // 存放迭代关联的测试计划
            plansSelected: [], // 存放用户所选择的测试计划,计划之间逗号隔开
            allPlanSelected: false, // 标识是否选取"全部"计划
            projectsSelected: [], // 存放用户选择的项目,项目之间逗号隔开
            initProjectOptions: [], // 项目选取框下拉列表(存放每次请求服务器获取的项目列表,仅在每次成功请求服务器数据后更新)
            projectOptions: [], // 项目选取框下拉列表
            allProjectSelected: false, // 标识是否选取"全部"项目
            projectVersionsSelected: [], // 存放用户选择的项目,项目之间逗号隔开
            projectVersionOptions: [], // 项目版本选取框下拉列表
            initProjectVersionOptions: [], // 项目选取框下拉列表(存放每次请求服务器获取的项目列表,仅在每次成功请求服务器数据后更新)
            allProjectVersionSelected: false, // 标识是否选取"全部"项目版本
            ifDisableGenerateReportBtn: true, // 是否禁用生成报告按钮
            elementLoadingText: "", // 正在加载报告、下载报告时的文案
            loading: false, // 标记是否正在生成测试报告
            reportId: "", // 存放用户所选择的测试报告ID
            showEditableItem: false, // 标记是否是展示可编辑项
            showReport: false, // 用于标记是否展示测试报告
            reportInfo: {}, // 存放报告统计数据
            sprintReports: [], // 存放迭代关联的测试报告
            oldValueOfReportItem: "", // 存放报告项被编辑前的旧值
            requirementPie: {
                title: "需求覆盖统计", //需求覆盖统计饼图标题
                // 需求统计饼图数据颜色 已完成 ForestGreen 测试中 LightSeaGreen  未测试 DarkOrange
                color: {
                    未测试: "#FFA500",
                    测试中: "#20B2AA",
                    已完成: "#228B22",
                },
            },

            defectStatusPie: {
                title: "缺陷状态统计", // 缺陷状态统计饼图标题
                color: defectStatusColor,
            },
            defectSeverityPie: {
                title: "缺陷级别统计", // 缺陷级别统计饼图标题
                // 缺陷分级统计饼图数据颜色 致命-DarkRed 严重 -DarkOrange 一般-LightSeaGreen 轻微-grey41
                color: {
                    致命: "#8B0000",
                    严重: "#FFA500",
                    一般: "#20B2AA",
                    轻微: "#696969",
                },
            },
            defectTypePie:{
                title:"缺陷类型统计",
                color: {
                    性能缺陷: "#8B0000",
                    功能缺陷: "#FFA500",
                    界面缺陷: "#20B2AA",
                    其它缺陷: "#696969"
                }
            },
            caseExecutionPie: {
                title: "用例执行统计", //用例通过率统计饼图标题
                // 用例执行统计饼图数据颜色 通过-ForestGreen  失败-DarkRed 阻塞-DarkOrange 未执行-grey41
                color: {
                    通过: "#228B22",
                    失败: "#8B0000",
                    阻塞: "#FFA500",
                    未执行: "#696969",
                },
            },
            editing: {
                title: false, // 标识是否正在编辑标题
                introduction: false,
                testScope: false,
                conclusion: false,
                suggestion: false,
                riskAnalysis: false,
            },
            showDataFromQuery:false, // 标记是否显示查询的数据还是报告里面生成的数据

        };
    },

    methods: {
        // 切换产品时触发的事件
        onProductChange(value) {
            if (!value) {
                this.productSelected = "";
            }
            localStorage.setItem(
                "productIdForSprintReport",
                this.productSelected
            );

            this.getSprintsDetails()
                .then((sprintId) => {
                    this.getSprintTestPlans();
                    this.getProjectVersionsWithProjects();
                    this.loadSprintTestReportList(sprintId);
                })
                .catch((err) => {
                    this.$message({
                        message: err.msg || err.message,
                        type: "warning",
                        duration: 3000,
                    });
                });
        },
        // 切换迭代项目时触发的事件
        onSprintChange(value) {
            // 冗余代码，因为请求异步进行，需要重置已选中项目，避免传递错误参数
            this.plansSelected = [];
            this.projectsSelected = [];
            this.projectVersionsSelected = [];

            this.getSprintTestPlans();
            this.getProjectVersionsWithProjects();
            this.loadSprintTestReportList(value);
        },

        // 修改已选中计划的计数器
        updateCounterForMultiSelector(optionsSelected, selectorName) {
            this.$nextTick(() => {
                let tempArr1 = undefined;
                try {
                    tempArr1 = this.$refs[
                        selectorName
                    ].$el.getElementsByClassName("el-select__tags-text");
                } catch (e) {
                    this.$message.error(
                        "修改Selector选择器中选项计数器失败：选择器名称参数错误"
                    );
                    return;
                }

                if (tempArr1.length > 1) {
                    tempArr1[1].innerHTML = "+ " + (optionsSelected.length - 1);
                }

                // 如果选择全部，不显示计数器
                if (tempArr1.length > 1) {
                    if (tempArr1[0].innerHTML == "全部") {
                        tempArr1[1].parentNode.style.cssText =
                            "Visibility:hidden";
                    } else {
                        tempArr1[1].parentNode.style.cssText =
                            "Visibility:display";
                    }
                }
            });
        },
        // 切换计划时触发的事件
        onPlanChange(value) {
            // 当前取项是否包含 全部 选项
            let valueContainAll = value.some(function (item, index, array) {
                return item.id == 0;
            });

            if (this.allPlanSelected && !valueContainAll) {
                // 已选取项包含“全部”，当前选中项不包含“全部”，说明是取消全选
                this.plansSelected = [];
                this.allPlanSelected = false;
            } else if (!this.allPlanSelected && valueContainAll) {
                //  已选取项不包含“全部”，当前选中项包含“全部”,说明全选
                this.allPlanSelected = true;
                this.plansSelected = [];
                for (let i = 0; i < this.planOptions.length; i++) {
                    this.plansSelected.push(this.planOptions[i]);
                }
            } else if (this.allPlanSelected && valueContainAll) {
                // 已选取项包含“全部”，当前选中项包含“全部”，说明只是部分选中,需要移除“全部”选项
                this.allPlanSelected = false;
                for (let i = 0; i < this.plansSelected.length; i++) {
                    if (this.plansSelected[i].id == 0) {
                        this.plansSelected.splice(i, 1);
                        break;
                    }
                }
            } else {
                // 已选取项不包含“全部”，当前选中项也不包含“全部”
            }

            // // 修改计数器(因为上述代码会导致官方自带的计数器不准确）
            // this.$nextTick(() => {
            //     let tempArr1 = this.$refs.sprintPlan.$el.getElementsByClassName(
            //         "el-select__tags-text"
            //     );
            //     if (tempArr1.length > 1) {
            //         tempArr1[1].innerHTML = "+ " + (plansSelected.length - 1);
            //     }

            //     // 如果选择全部，不显示计数器
            //     if (tempArr1.length > 1) {
            //         if (tempArr1[0].innerHTML == "全部") {
            //             tempArr1[1].parentNode.style.cssText =
            //                 "Visibility:hidden";
            //         } else {
            //             tempArr1[1].parentNode.style.cssText =
            //                 "Visibility:display";
            //         }
            //     }
            // });
            this.updateCounterForMultiSelector(value, "testplanSelector");

            let projectIdArr = [];
            if (this.plansSelected.length) {
                this.plansSelected.forEach((item) => {
                    if (item.projectIds) {
                        projectIdArr = projectIdArr.concat(
                            item.projectIds.split(",")
                        );
                    }
                });
                let projectIdSet = new Set(projectIdArr);
                projectIdArr = Array.from(projectIdSet);
                this.projectsSelected = [];
                this.projectOptions = [];
                this.projectVersionsSelected = [];
                this.projectVersionOptions = [];
                this.initProjectOptions.forEach((item) => {
                    if (projectIdArr.includes("" + item.id)) {
                        this.projectsSelected.push(item);
                        this.projectOptions.push(item);
                        this.projectVersionOptions = this.projectVersionOptions.concat(
                            item.versions
                        );
                        this.projectVersionsSelected = this.projectVersionsSelected.concat(
                            item.versions
                        );
                    }
                });
            } else {
                this.projectOptions = this.initProjectOptions;
                this.projectsSelected = [];
                this.projectVersionOptions = this.initProjectVersionOptions;
                this.projectVersionsSelected = [];
            }
        },
        onProjectChange(value) {
            // 当前取项是否包含 全部 选项
            let valueContainAll = value.some(function (item, index, array) {
                return item.id == 0;
            });
            if (this.allProjectSelected && !valueContainAll) {
                // 已选取项包含“全部”，当前选中项不包含“全部”，说明是取消全选
                this.projectsSelected = [];
                this.allProjectSelected = false;
            } else if (!this.allProjectSelected && valueContainAll) {
                //  已选取项不包含“全部”，当前选中项包含“全部”,说明全选
                this.allProjectSelected = true;
                this.projectsSelected = [];
                for (let i = 0; i < this.projectOptions.length; i++) {
                    this.projectsSelected.push(this.projectOptions[i]);
                }
            } else if (this.allProjectSelected && valueContainAll) {
                // 已选取项包含“全部”，当前选中项包含“全部”，说明只是部分选中,需要移除“全部”选项
                this.allProjectSelected = false;
                for (let i = 0; i < this.projectsSelected.length; i++) {
                    if (this.projectsSelected[i].id == 0) {
                        this.projectsSelected.splice(i, 1);
                        break;
                    }
                }
            } else {
                // 已选取项不包含“全部”，当前选中项也不包含“全部”
            }

            this.updateCounterForMultiSelector(value, "projectSelector");
            if (this.projectsSelected.length) {
                this.projectVersionsSelected = [];
                this.projectVersionOptions = [];
                this.projectsSelected.forEach((item) => {
                    if (item.versions) {
                        this.projectVersionOptions = this.projectVersionOptions.concat(
                            item.versions
                        );
                        this.projectVersionsSelected = this.projectVersionsSelected.concat(
                            item.versions
                        );
                    }
                });
            } else {
                let projectIdArr = [];
                if (this.plansSelected.length) {
                    this.plansSelected.forEach((item) => {
                        if (item.projectIds) {
                            projectIdArr = projectIdArr.concat(
                                item.projectIds.split(",")
                            );
                        }
                    });
                    let projectIdSet = new Set(projectIdArr);
                    projectIdArr = Array.from(projectIdSet);
                    this.projectVersionsSelected = [];
                    this.projectVersionOptions = [];
                    this.initProjectOptions.forEach((item) => {
                        if (projectIdArr.includes("" + item.id)) {
                            this.projectVersionOptions = this.projectVersionOptions.concat(
                                item.versions
                            );
                            this.projectVersionsSelected = this.projectVersionsSelected.concat(
                                item.versions
                            );
                        }
                    });

                    this.projectVersionsSelected = [];
                } else {
                    this.projectVersionsSelected = [];
                    this.projectVersionOptions = this.initProjectVersionOptions;
                }
            }
        },
        onProjectVersionChange(value) {
            // 当前取项是否包含 全部 选项
            let valueContainAll = value.some(function (item, index, array) {
                return item.id == 0;
            });

            if (this.allProjectVersionSelected && !valueContainAll) {
                // 已选取项包含“全部”，当前选中项不包含“全部”，说明是取消全选
                this.projectVersionsSelected = [];
                this.allProjectVersionSelected = false;
            } else if (!this.allProjectVersionSelected && valueContainAll) {
                //  已选取项不包含“全部”，当前选中项包含“全部”,说明全选
                this.allProjectVersionSelected = true;
                this.projectVersionsSelected = [];
                for (let i = 0; i < this.projectVersionOptions.length; i++) {
                    this.projectVersionsSelected.push(
                        this.projectVersionOptions[i]
                    );
                }
            } else if (this.allProjectVersionSelected && valueContainAll) {
                // 已选取项包含“全部”，当前选中项包含“全部”，说明只是部分选中,需要移除“全部”选项
                this.allProjectVersionSelected = false;
                for (let i = 0; i < this.projectVersionsSelected.length; i++) {
                    if (this.projectVersionsSelected[i].id == 0) {
                        this.projectVersionsSelected.splice(i, 1);
                        break;
                    }
                }
            } else {
                // 已选取项不包含“全部”，当前选中项也不包含“全部”
            }

            this.updateCounterForMultiSelector(value, "projectVersionSelector");
        },
        // 获取测试报告统计数据
        getReportStatistics() {
            try {
                if (!this.sprintSelected) {
                    this.$alert("迭代为空", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }

                this.elementLoadingText = "请稍等，正在努力加载统计数据...";
                this.loading = true; // 加载遮罩
  
                let planIdArray = [];
                for (let i = 0; i < this.plansSelected.length; i++) {
                    planIdArray.push(this.plansSelected[i].id);
                }

                let projectIdArray = [];
                for (let i = 0; i < this.projectsSelected.length; i++) {
                    projectIdArray.push(this.projectsSelected[i].id);
                }

                let projectVersionIdArray = [];
                for (let i = 0; i < this.projectVersionsSelected.length; i++) {
                    projectVersionIdArray.push(
                        this.projectVersionsSelected[i].id
                    );
                }

                // 发送生成测试报告统计数据请求
                this.$api.sprintTestReport
                    .generateSprintTestReportStatistics({
                        sprintId: this.sprintSelected,
                        planIds: planIdArray,
                        projects: projectIdArray,
                        projectVersions: projectVersionIdArray,
                    })
                    .then((res) => {
                        this.loading = false; // 取消遮罩
                        this.ifDisableGenerateReportBtn = false; // 启用生成报告按钮
                        if (res.success) {
                            this.reportInfo = res.data;
                            if (res.msg.length) {
                                this.$message({
                                    dangerouslyUseHTMLString: true,
                                    message: res.msg,
                                    type: "warning",
                                });
                            }
                        } else {
                            this.$message.error(res.msg);
                            return;
                        }

                        this.refreshReportContent(true);
                    })
                    .catch((res) => {
                        this.loading = false; // 取消遮罩
                        this.$message.error(res.msg || res.message);
                    });
            } catch (error) {
                this.loading = false;
                this.$message.error("" + error.message);
            }
        },
        // 刷新报告展示内容
        refreshReportContent(fromQuery){
            this.showReport = false;
            if (fromQuery){ // 要展示的统计数据来自查询
                this.$nextTick(()=>{
                    this.reportId = "";
                    this.showEditableItem = false;
                    this.showDataFromQuery = true;
                    this.showReport = true;
                }); 
            } else { // 要展示的统计数据来自已生成的报告             
                this.$nextTick(() => {
                    this.showEditableItem = true;
                    this.showDataFromQuery = false;
                    this.showReport = true;
                });
            }        
        },
        // 生成测试报告
        generateSprintTestReport() {
            try {
                this.elementLoadingText = "请稍等，正在努力生成测试报告...";
                this.loading = true;

                // 发送生成测试报告请求
                this.$api.sprintTestReport
                    .createSprintTestReport({
                        sprintId: this.sprintSelected,
                    })
                    .then((res) => {
                        this.loading = false; // 取消遮罩
                        if (res.success) {
                            this.ifDisableGenerateReportBtn = true; // 禁用生成按钮
                            this.reportInfo = res.data;

                            // 查看报告，报告列表中插入新增的报告，并且设置为当前选中报告
                            this.sprintReports.splice(0, 0, {
                                id: this.reportInfo.id,
                                title: this.reportInfo.title,
                            });
                            this.reportId = this.reportInfo.id;
                        } else {
                            this.$message.error(res.msg);
                            return;
                        }

                        this.refreshReportContent(false);
                    })
                    .catch((res) => {
                        this.loading = false; // 取消遮罩
                        this.$message.error(res.msg || res.message);
                    });
            } catch (err) {
                this.loading = false; // 取消遮罩
                this.$message.error(res.msg || res.message);
            }
        },
        // 加载迭代关联的测试报告列表
        loadSprintTestReportList(sprintID) {
            this.$api.sprintTestReport
                .getSprintTestReportsDetails({
                    sprintId: sprintID,
                })
                .then((res) => {
                    if (res.success) {
                        this.sprintReports = res.data;
                        if (this.sprintReports.length) {
                            this.reportId = this.sprintReports[0].id;
                            this.viewSprintTestReport(this.reportId);
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 查看测试报告
        viewSprintTestReport(reportID, sprintID) {
            this.loading = true;
            this.elementLoadingText = "请稍等，正在努力加载测试报告...";
            this.$api.sprintTestReport
                .getSprintTestReport({
                    sprintId: sprintID,
                    reportId: reportID,
                })
                .then((res) => {
                    this.loading = false;
                    if (res.success) {
                        this.reportInfo = res.data;
                    } else {
                        this.$message.error(res.msg);
                        return;
                    }

                    this.refreshReportContent(false);
                })
                .catch((res) => {
                    this.loading = false;
                    this.$message.error(res.msg || res.message);
                });
        },
        // 查看报告选择框选择值发生变化时的处理函数
        onReportChange(reportID) {
            if (reportID) {
                // 仅在执行非清空所选择报告操作时，才执行“查看报告”的动作
                this.viewSprintTestReport(reportID);
            }
        },
        // 编辑报告项
        editReportItem(item) {
            this.editing[item] = true;
            this.oldValueOfReportItem = this.reportInfo[item];
            this.$nextTick((_) => {
                this.$refs[item].focus();
            });
        },

        // 编辑输入框失去焦点事件统一处理函数
        onEditingBlur(item) {
            this.editing[item] = false;
            this.updateReportItem(item, this.oldValueOfReportItem);
        },
        //修改测试报告项
        updateReportItem(item, oldValue) {
            this.$api.sprintTestReport
                .updateSprintTestReport({
                    reportId: this.reportInfo.id,
                    targetItem: item, // 要修改的目标项
                    value: this.reportInfo[item],
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        if (item == "title") {
                            // 修改标题，同步修改查看报告下拉选项
                            for (
                                let i = 0;
                                i < this.sprintReports.length;
                                i++
                            ) {
                                let report = this.sprintReports[i];

                                if (report.id == this.reportInfo.id) {
                                    report.title = res.data.title;
                                }
                            }
                        }
                    } else {
                        this.$message.error(res.msg);
                        this.reportInfo[item] = oldValue;
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                    this.reportInfo[item] = oldValue;
                });
        },

        // 发送报告
        sendSprintTestReport() {
            this.$alert("功能待开发", "提示", {
                confirmButtonText: "确定",
            });
        },
        // 下载报告
        downloadSprintTestReport() {
            if (!this.reportInfo.id) {
                this.$message.warning("请先选择要下载的报告");
                return;
            }
            try {
                this.loading = true;
                this.elementLoadingText = "请稍等，正在努力下载测试报告......";

                let echartBase64Info = {}; // 存放通过getDataURL获取的echarts图表base64编码信息

                // 获取echart图表base64编码后的数据信息
                for (let key in this.echartPicIdDict) {
                    // let echartObj = this.$echarts.getInstanceById(this.echartPicIdDict[key]); // 结果 echartObj=undefined
                    let echartDomObj = document.getElementById(
                        this.echartPicIdDict[key]
                    );
                    if (echartDomObj) {
                        let echartObj = this.$echarts.getInstanceByDom(
                            document.getElementById(this.echartPicIdDict[key])
                        );

                        if (echartObj) {
                            try {
                                const picBase64Data = echartObj.getDataURL(); //返回数据格式：data:image/png;base64,base64编码数据
                                echartBase64Info[key] = picBase64Data;
                            } catch (err) {
                                console.log(
                                    err +
                                        "可能是成图片(ID:" +
                                        key +
                                        ")未生成导致"
                                );
                            }
                        }
                    }
                }

                // 发送下载报告请求
                this.$api.sprintTestReport
                    .downloadSprintTestReport({
                        reportId: this.reportInfo.id,
                        sprintId: this.reportInfo.sprintId,
                        echartBase64Info: echartBase64Info,
                    })
                    .then((res) => {
                        let link = document.createElement("a");
                        let blob = new Blob([res.data], {
                            type: res.headers["content-type"],
                        });

                        link.style.display = "none";
                        link.href = window.URL.createObjectURL(blob);
                        // 下载文件名无法通过后台响应获取，因为获取不到Content-Disposition响应头
                        link.setAttribute(
                            "download",
                            this.reportInfo.title + ".pdf"
                        );

                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        this.loading = false;
                    })
                    .catch((res) => {
                        if (
                            Object.prototype.toString.call(res.response.data) ==
                            "[object Blob]"
                        ) {
                            let reader = new FileReader();
                            reader.onload = (e) => {
                                let responseData = JSON.parse(e.target.result);
                                if (responseData.msg) {
                                    this.$message.error(
                                        res.msg ||
                                            res.message + ":" + responseData.msg
                                    );
                                } else {
                                    this.$message.error(
                                        res.msg ||
                                            res.message +
                                                ":" +
                                                responseData.detail
                                    );
                                }
                            };
                            reader.readAsText(res.response.data);
                        } else {
                            this.$message.error(res.msg || res.message);
                        }
                        this.loading = false;
                    });
            } catch (err) {
                this.loading = false;
                this.$message.error(err.message);
            }
        },
        // 设置迭代测试报告内容容器的top 位置
        setSprintReportTopPos() {
            if (this.idOfSetTimeOut) {
                clearTimeout(this.idOfSetTimeOut);
            }
            this.idOfSetTimeOut = setTimeout(() => {
                let topPannel = this.$refs.topPannel;

                let topPannelOffsetHeight = 0;
                let topPannelMarginTop = 0;
                let topPannelMarginBottom = 0;
                let topPannelHeight = 0;

                if (topPannel) {
                    topPannelOffsetHeight = topPannel.offsetHeight;

                    let elementStyle = window.getComputedStyle(topPannel);
                    topPannelMarginTop = parseInt(
                        elementStyle.marginTop.replace("px", "")
                    );

                    topPannelMarginBottom = parseInt(
                        elementStyle.marginBottom.replace("px", "")
                    );

                    topPannelHeight =
                        topPannelMarginTop +
                        topPannelMarginBottom +
                        topPannelOffsetHeight;
                }
                if (this.$refs.sprintReport) {
                    this.$refs.sprintReport.style.cssText =
                        "top:" + topPannelHeight + "px;";
                }
            }, 100);
        },
        // 获取产品列表
        getProductsDetails() {
            this.productSelected = "";
            this.productOptions = [];
            return new Promise((resolve, reject) => {
                this.$api.product
                    .getProductsDetails({ fields: "id,name" })
                    .then((res) => {
                        if (res.success) {
                            this.productOptions = res.data;

                            let productSelected = localStorage.getItem(
                                "productIdForSprintReport"
                            );
                            if (productSelected) {
                                productSelected = parseInt(productSelected);
                                let result = this.productOptions.some(
                                    (item) => {
                                        if (item.id == productSelected) {
                                            return true;
                                        }
                                    }
                                );
                                if (result) {
                                    this.productSelected = productSelected;
                                } else {
                                    if (this.productOptions.length) {
                                        this.productSelected = this.productOptions[0].id;
                                    } else {
                                        this.$message.warning(
                                            "未获取到产品列表"
                                        );
                                    }
                                }
                            } else {
                                if (this.productOptions.length) {
                                    this.productSelected = this.productOptions[0].id;
                                } else {
                                    this.$message.warning("未获取到产品列表");
                                }
                            }

                            localStorage.setItem(
                                "productIdForSprintReport",
                                this.productSelected
                            );
                            resolve(this.productSelected);
                        } else {
                            this.$message.error(res.msg);
                            reject(res);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                        reject(res);
                    });
            });
        },
        // 获取迭代列表
        getSprintsDetails() {
            this.sprintOptions = [];
            this.sprintSelected = "";
            this.planOptions = [];
            this.plansSelected = [];
            this.projectOptions = [];
            this.projectsSelected = [];
            this.initProjectOptions = [];

            return new Promise((resolve, reject) => {
                if (!this.productSelected) {
                    reject({ msg: "请选择产品" });
                }
                this.$api.product
                    .getProductSprintsDetails({
                        productId: this.productSelected,
                    })
                    .then((res) => {
                        if (res.success) {
                            this.sprintOptions = res.data;

                            if (this.sprintOptions.length) {
                                this.sprintSelected = this.sprintOptions[0].id;
                            } else {
                                reject({
                                    msg: "未获取到当前产品关联的迭代",
                                });
                            }
                            resolve(this.sprintSelected);
                        } else {
                            reject(res);
                        }
                    })
                    .catch((res) => {
                        reject(res);
                    });
            });
        },
        // 获取迭代关联的测试计划
        getSprintTestPlans() {
            this.planOptions = [];
            this.plansSelected = [];

            if (!this.sprintSelected) {
                return;
            }

            this.$api.sprint
                .getSprintTestPlans({
                    sprintId: this.sprintSelected,
                    fields: "id,name,project_ids",
                })
                .then((res) => {
                    if (res.success) {
                        this.planOptions = res.data;
                        if (this.planOptions.length) {
                            // 添加 全部 选项
                            this.planOptions.splice(0, 0, {
                                id: 0,
                                name: "全部",
                            });
                        } else {
                            this.$message({
                                message: "未获取到当前迭代关联的测试计划",
                                type: "warning",
                                duration: 3000,
                            });
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 获取迭代关联的项目版本及对应项目
        getProjectVersionsWithProjects() {
            this.projectOptions = [];
            this.projectsSelected = [];
            this.initProjectOptions = [];
            this.projectVersionOptions = [];
            this.projectVersionsSelected = [];
            this.initProjectVersionOptions = [];

            if (!this.sprintSelected) {
                return;
            }

            this.$api.sprint
                .getRelatedProjectsWithVersions({
                    sprintId: this.sprintSelected,
                })
                .then((res) => {
                    if (res.success) {
                        this.projectOptions = res.data.projectOptions;
                        this.initProjectOptions = JSON.parse(
                            JSON.stringify(res.data.projectOptions)
                        );

                        this.projectVersionOptions =
                            res.data.projectVersionOptions;
                        this.initProjectVersionOptions = JSON.parse(
                            JSON.stringify(res.data.projectVersionOptions)
                        );

                        if (this.projectVersionOptions.length) {
                            // 添加 全部 选项
                            this.projectVersionOptions.splice(0, 0, {
                                id: 0,
                                name: "全部",
                            });
                            this.initProjectVersionOptions.splice(0, 0, {
                                id: 0,
                                name: "全部",
                            });

                            this.projectOptions.splice(0, 0, {
                                id: 0,
                                name: "全部",
                            });
                            this.initProjectOptions.splice(0, 0, {
                                id: 0,
                                name: "全部",
                            });
                        } else {
                            this.projectOptions = [];
                            this.$message({
                                message: "未获取到当前迭代关联的项目",
                                type: "warning",
                                duration: 1000,
                            });
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        getSelectWidthStyle(string, initWidth) {
            let style = "width:" + initWidth + "px";
            if (string) {
                let tempWidth = this.$customUtils.stringHandler.getTextPixelWith(
                    string,
                    "400 13.3333px Arial"
                ); //
                console.log(string, tempWidth);
                if (tempWidth > initWidth - 47) {
                    style = "width:" + (tempWidth + 47 + 30) + "px";
                }
            }
            return style;
        },
    },
    created() {
        this.getProductsDetails().then((data) => {
            this.getSprintsDetails()
                .then((sprintId) => {
                    // 获取迭代关联的测试计划
                    this.getSprintTestPlans();

                    // 获取迭代关联的项目&项目版本
                    this.getProjectVersionsWithProjects();

                    this.loadSprintTestReportList(sprintId);
                })
                .catch((err) => {
                    this.$message({
                        message: err.msg || err.message,
                        type: "warning",
                        duration: 3000,
                    });
                });
        });
    },
    updated() {
        this.setSprintReportTopPos();
    },
};
</script>

<style scoped lang="scss">
.view-wrapper {
    position: absolute;
    left: 0px;
    right: 0px;
    top: 0px;
    bottom: 0px;
    overflow: hidden;
}

// 存放迭代测试报告内容的容器
.sprint-test-report-content {
    position: absolute;
    top: 78px;
    bottom: 0px;
    left: 0px;
    right: 0px;
    background: rgba(250, 248, 248, 0.747);
    // border-style: solid;
    // border-color: rgba(172, 167, 167, 0.2);
    // border-width: 1px;
    // border-radius: 1px;
    padding: 5px 5px 5px 5px;
    overflow: auto;
}

/* 报告标题 */
.report-title {
    text-align: center;
    font-weight: bold;
}

/* 手工输入内容*/
.hand-input-content {
    font-size: 14px;
}

/* 报告子节点 */
.report-session,
.report-sub-session {
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-bottom-color: rgba(217, 223, 223, 0.9);
    padding: 10px 0px 10px 0px;
}
/* 报告节点标题 */
.report-session-title {
    font-weight: bold;
}

/* 报告子节点标题 */
.report-sub-session-title {
    font-weight: bold;
    font-size: 15px;
    color: #4a4a4a;
    margin: 5px 2px 5px 2px;
}

.plan-table-wrapper {
    // border-width: 1px;
    // border-style: solid;
    // background: rgba(241, 239, 239, 0.438);
    // border-color: rgb(204, 206, 206);
    td {
        text-align: center;
        padding-top: 3px;
        padding-bottom: 3px;
        font-size: 14px;
        > div {
            display: inline;
        }
    }
}

/* 名词解释\说明 */
.terminology-wrapper {
    font-size: 12px;
    .terminology {
        font-weight: bold;
        margin-left: 5px;
    }
}

// 测试统计饼图样式
.doughnut-pie-chart {
    margin: 5px 0px 5px 0px;
    padding: 5px 3px 5px 3px;
    display: inline-block;
    width: 400px;
    // width: 20%; // 会导致屏幕较小的情况下，不换行展示组件
    height: 210px;
    border-width: 1px;
    border-style: solid;
    border-color: rgba(204, 206, 206, 0.7);
}

// 测试统计柱状图样式
.stacked-column-chart {
    padding: 0px 0px 0px 0px;
    width: 98%;
}

// 支持 text area 输入框输入的值换行显示
.pre-text {
    white-space: pre-wrap;
    word-wrap: break-word;
    word-break: break-all;
}
</style>
