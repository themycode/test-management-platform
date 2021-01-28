<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <div v-if="!planDetailVisible">
            <!-- 操作按钮 -->
            <div ref="tableToolbar" class="table-toolbar">
                <el-button-group>
                    <el-button :size="buttonSize" @click="newPlan">新增计划</el-button>
                    <el-button
                        :size="buttonSize"
                        @click="deleteRows($api.sprintTestPlan.deleteTestPlans)"
                    >删除计划</el-button>
                </el-button-group>
            </div>
            <!-- 查询表单 -->
            <div class="table-query-form" ref="queryForm">
                <el-form :inline="true" :model="queryForm" size="small">
                    <el-form-item label="创建时间">
                        <el-date-picker
                            style="width:330px"
                            v-model="createTime"
                            type="datetimerange"
                            placeholder="选择日期和时间"
                            range-separator="至"
                            start-placeholder="开始时间"
                            end-placeholder="结束时间"
                            size="mini"
                            :default-time="['00:00:00', '23:59:59']"
                            value-format="yyyy-MM-dd HH:mm:ss"
                        ></el-date-picker>
                    </el-form-item>
                    <el-form-item label="完成时间">
                        <el-date-picker
                            style="width:330px"
                            v-model="finishTime"
                            type="datetimerange"
                            placeholder="选择日期和时间"
                            range-separator="至"
                            start-placeholder="开始时间"
                            end-placeholder="结束时间"
                            size="mini"
                            :default-time="['00:00:00', '23:59:59']"
                            value-format="yyyy-MM-dd HH:mm:ss"
                        ></el-date-picker>
                    </el-form-item>

                    <el-form-item label="计划名称">
                        <el-input
                            v-model="queryForm.name"
                            placeholder="请输入计划名称"
                            clearable
                            style="width:230px"
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="计划状态">
                        <el-select
                            v-model="queryForm.status"
                            :multiple="true"
                            clearable
                            style="width: 235px;"
                        >
                            <el-option label="未执行" value="未执行"></el-option>
                            <el-option label="未完成" value="未完成"></el-option>
                            <el-option label="已完成" value="已完成"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="关联迭代">
                        <el-select v-model="queryForm.sprintId" clearable>
                            <el-option
                                v-for="item in sprintOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="创建人">
                        <el-input
                            v-model="queryForm.creater"
                            placeholder="请输入创建人"
                            clearable
                            style="width:200px"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="执行环境">
                        <el-input
                            v-model="queryForm.environment"
                            placeholder="请输入执行环境"
                            clearable
                            style="width:150px"
                        ></el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="queryRows('clickQuery')">查询</el-button>
                    </el-form-item>
                </el-form>
            </div>

            <!-- 表格 -->
            <el-table
                ref="myTable"
                :data="tableData"
                border
                stripe
                :empty-text="emptyText"
                class="my-table testplan-table"
                :lazy="false"
                @selection-change="onSelectChange"
                @row-click="clickRow"
                highlight-current-row
            >
                <!--多选复选框-->
                <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
                <!-- <el-table-column prop="id" label="ID" width="60px" header-align="center" align="center"></el-table-column> -->
                <el-table-column
                    prop="name"
                    label="计划名称"
                    show-overflow-tooltip
                    header-align="center"
                    min-width="220px"
                    align="left"
                >
                    <template slot-scope="scope">
                        <el-link
                            type="primary"
                            @click="viewPlanDetail(scope.$index, scope.row)"
                        >{{ scope.row.name }}</el-link>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="sprintName"
                    label="关联迭代"
                    show-overflow-tooltip
                    width="120px"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="projectNames"
                    label="关联项目"
                    show-overflow-tooltip
                    width="180px"
                    min-width="100"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="createrName"
                    label="创建人"
                    width="90px"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="createTime"
                    label="创建时间"
                    width="150px"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="finishTime"
                    label="完成时间"
                    width="150px"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="envNames"
                    label="执行环境"
                    width="100px"
                    header-align="center"
                    show-overflow-tooltip
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="progress"
                    label="测试进度"
                    width="120px"
                    header-align="center"
                    align="center"
                >
                    <template
                        slot-scope="scope"
                    >{{Math.round(scope.row.caseNumRelated ? (scope.row.caseNumExecuted - scope.row.caseNumBlocked)/scope.row.caseNumRelated*100:0)}}%({{scope.row.caseNumExecuted - scope.row.caseNumBlocked}}/{{scope.row.caseNumRelated}})</template>
                </el-table-column>
                <el-table-column
                    prop="passRate"
                    label="通过率"
                    width="120px"
                    header-align="center"
                    align="center"
                >
                    <template
                        slot-scope="scope"
                    >{{Math.round(scope.row.caseNumRelated ? scope.row.caseNumSuccess/scope.row.caseNumRelated*100:0)}}%({{scope.row.caseNumSuccess}}/{{scope.row.caseNumRelated}})</template>
                </el-table-column>
                <el-table-column
                    prop="status"
                    label="状态"
                    width="60px"
                    header-align="center"
                    align="center"
                ></el-table-column>
                <el-table-column label="操作" align="left" width="350px">
                    <template slot-scope="scope">
                        <el-button size="mini" @click="bindCase(scope.$index, scope.row)">关联用例</el-button>
                        <el-button size="mini" @click="viewPlanDetail(scope.$index, scope.row)">进入计划</el-button>
                        <el-button size="mini" @click="editPlan(scope.$index, scope.row)">编辑</el-button>
                        <el-button
                            size="mini"
                            type="danger"
                            @click="deleteRow(scope.$index, scope.row, $api.sprintTestPlan.deleteTestPlan)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination
                ref="tablePagination"
                class="table-pagination"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                layout="total, sizes, prev, pager, next"
                :hide-on-single-page="false"
                :total="total"
                prev-text="上一页"
                next-text="下一页"
                :current-page="currentPage"
                :page-sizes="pageSizes"
                :page-size="pageSize"
                :pager-count="pagerCount"
            ></el-pagination>

            <!-- 测试计划对话框 -->
            <test-plan-dialog
                v-if="planDialogVisible"
                :dialogVisible.sync="planDialogVisible"
                :dialogTitle="planDialogTitle"
                :tableData="tableData"
                :dialogFormData="planData"
                :row="row"
                :sprintOptions="sprintOptions"
            ></test-plan-dialog>

            <!-- 关联用例对话框 -->
            <bind-case-dialog
                v-if="bindCaseDialogVisible"
                :dialogVisible.sync="bindCaseDialogVisible"
                :planRow="row"
            ></bind-case-dialog>
        </div>

        <!-- 测试计划详情对话框 -->
        <test-plan-detail
            :planRow="row"
            v-if="planDetailVisible"
            :planDetailVisible.sync="planDetailVisible"
        ></test-plan-detail>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

import TestPlanDialog from "./TestPlanDialog";
import BindCaseDialog from "./BindCaseDialog";
import TestPlanDetail from "./TestPlanDetail";

export default {
    mixins: [elTableMixin, elButtonMixin],
    props: ["productID"],
    data() {
        return {
            // 查询表单
            queryForm: {
                startTime: "", // 起始时间（创建时间）
                endTime: "", // 结束时间（创建时间）
                finishStartTime: "", // 起始时间（完成时间）
                finishEndTime: "", // 结束时间（完成时间）
                name: "", // 计划名称
                status: [], // 测试计划状态,状态之间用逗号隔开
                creater: "", // 创建人
                envId: "", // 测试环境
                sprintId: "", // 迭代ID
                productId: this.productID, // 产品ID
            },
            pageSizes: [10, 15, 20, 30, 40, 50, 100, 150], //每页显示记录数选择器的选项设置
            pageSize: 15, // 表格默认每页显示的记录数
            planData: null, // 存放新增，修改测试计划相关数据

            planDialogVisible: false, // 标识新建\编辑测试计划对话框是否可见，true - 可见， false - 不可见
            planDialogTitle: "", // 测试计划对话框标题

            bindCaseDialogVisible: false, // 标识关联用例对话框是否可见 true - 可见 false - 不可见
            sprintCaseIDList: [], // 存放当前已绑定sprint测试用例ID(包含测试集在测试用例表中映射记录的ID)
            baseCaseIDList: [], // 存放当前已绑定基线测试用例ID(包含测试集在测试用例表中映射记录的ID)
            planDetailVisible: false, // 标识是否展示测试计划详情页 true - 显示 false - 不显示

            tabPanelName: "测试计划详情", // 测试计划详情tab标签页名称
            sprintOptions: [], // 存放迭代下拉选项
        };
    },
    components: {
        TestPlanDialog,
        BindCaseDialog,
        TestPlanDetail,
    },
    methods: {
        // 获取测试计划
        queryRows(action) {
            if (action == "clickQuery") {
                this.currentPage = 1;
            }

            let queryParams = Object.assign({}, this.queryForm);
            queryParams["pageSize"] = this.pageSize;
            queryParams["pageNo"] = this.currentPage;
            queryParams.status = queryParams.status.join(",");

            if (!this.productID) {
                this.total = 0;
                this.tableData = [];
                return;
            }

            // 向后台发送请求
            this.$api.sprintTestPlan
                .getTestPlans(queryParams)
                .then((res) => {
                    if (res.success) {
                        this.total = res.data.total;
                        this.tableData = res.data.rows;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                });
        },
        // 新增计划
        newPlan() {
            if (!this.planDialogVisible) {
                this.planData = {
                    name: "", // 计划名称
                    desc: "", // 计划描述
                    beginTime: "", // 预估开始时间
                    endTime: "", // 预估结束时间
                    sprint: this.sprintOptions.length
                        ? this.sprintOptions[0]
                        : null, // 迭代
                    projectIds: [], // 关联项目id
                    envNames: [], // 执行环境
                    sprintId: null, // 关联迭代ID
                    productId: this.productID, // 关联产品ID
                };
                this.planDialogVisible = true;
                this.planDialogTitle = "新增计划";
            }
        },
        // 编辑计划
        editPlan(index, row) {
            if (!this.planDialogVisible) {
                this.getTestPlanDetail(row.id)
                    .then((data) => {
                        for (let key in row) {
                            row[key] = data[key];
                        }

                        let projectIdList = row.projectIds.split(",");
                        let projectIds = projectIdList.map((item) => {
                            return parseInt(item);
                        });

                        this.planData = {
                            id: row.id,
                            name: row.name, // 计划名称
                            desc: row.desc, // 计划描述
                            beginTime: row.beginTime, // 预估开始时间
                            endTime: row.endTime, // 预估结束时间
                            sprint: {
                                // 关联迭代
                                id: row.sprintId,
                                name: row.sprintName,
                            },
                            projectIds: projectIds, // 关联项目id
                            productId: row.productId,
                            envNames: row.envNames.split(","), // 执行环境名称
                        };
                        this.row = row;
                        this.planDialogVisible = true;
                        this.planDialogTitle = "修改计划";
                    })
                    .catch((err) => {
                        this.$message.error(err.msg||err.message);
                    });
            }
        },
        // 打开关联测试用例对话框
        bindCase(index, row) {
            if (!this.bindCaseDialogVisible) {
                this.bindCaseDialogVisible = true;
                this.row = row;
            }
        },

        // 查看计划详情
        viewPlanDetail(index, row) {
            if (!this.planDetailVisible) {
                this.planDetailVisible = true;
                this.row = row;
            }
        },
        // 关闭测试计划详情tab页
        removePlanDetailTab() {
            this.planDetailVisible = false;
        },
        // 点击表格记录行
        clickRow(row, column, event) {
            // if (column && column.label != "操作") {
            //     this.viewPlanDetail(undefined, row);
            // }
        },
        // 获取产品关联的迭代列表
        getProductSprintsDetails() {
            if (!this.productID) {
                this.sprintOptions = [];
                return;
            }
            this.$api.product
                .getProductSprintsDetails({
                    productId: this.productID,
                })
                .then((res) => {
                    if (res.success) {
                        this.sprintOptions = res.data;
                    } else {
                        this.sprintOptions = [];
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                    this.sprintOptions = [];
                });
        },
        // 获取测试计划详情信息
        getTestPlanDetail(planId) {
            return new Promise((resolve, reject) => {
                this.$api.sprintTestPlan
                    .getTestPlanDetail({
                        id: planId,
                    })
                    .then((res) => {
                        if (res.success) {
                            resolve(res.data);
                        } else {
                            reject(res);
                        }
                    })
                    .catch((res) => {
                        reject(res);
                    });
            });
        },
    },
    watch: {
        sprint: function () {
            this.planDetailVisible = false; // 关闭测试计划详情页
            this.currentPage = 1;
            this.queryRows();
        },
    },
    computed: {
        ...mapState({
            suiteType: (state) => state.sprintCaseSuite.suiteType,
            suiteID: (state) => state.sprintCaseSuite.suiteID,
        }),
        createTime: {
            get() {
                if (this.queryForm.startTime && this.queryForm.endTime) {
                    return [this.queryForm.startTime, this.queryForm.endTime];
                } else {
                    return [];
                }
            },
            set(value) {
                if (value) {
                    this.queryForm.startTime = value[0];
                    this.queryForm.endTime = value[1];
                } else {
                    this.queryForm.startTime = "";
                    this.queryForm.endTime = "";
                }
            },
        },
        finishTime: {
            get() {
                if (
                    this.queryForm.finishStartTime &&
                    this.queryForm.finishEndTime
                ) {
                    return [
                        this.queryForm.finishStartTime,
                        this.queryForm.finishEndTime,
                    ];
                } else {
                    return [];
                }
            },
            set(value) {
                if (value) {
                    this.queryForm.finishStartTime = value[0];
                    this.queryForm.finishEndTime = value[1];
                } else {
                    this.queryForm.finishStartTime = "";
                    this.queryForm.finishEndTime = "";
                }
            },
        },
    },
    created() {
        this.queryRows(); // 加载时查询用例数据
        this.getProductSprintsDetails();
    },
    updated() {
        this.setTableBodySize(); // 设置表格高度
    },
};
</script>



<style lang="scss">
.testplan-table {
    .cell {
        padding-left: 5px !important;
        padding-right: 5px !important;
    }

    .operation-col-cell-class .cell .el-button--danger {
        padding-left: 15px !important;
        padding-right: 15px !important;
    }
}
</style>


