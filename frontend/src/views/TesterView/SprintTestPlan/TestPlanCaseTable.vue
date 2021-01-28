<template>
    <div
        class="view-wrapper"
        ref="viewWrapper"
        v-resize="setTableBodySize"
        v-loading="loading"
        :element-loading-text="elementLoadingText"
    >
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button
                    :size="buttonSize"
                    type="primary"
                    @click="updateCaseTestResults"
                    :disabled="showCaseDialog"
                    >批量修改测试结果</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="batchUpdateTestCases"
                    :disabled="showCaseDialog"
                    >批量修改用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="newCase"
                    :disabled="iscurrSuiteRoot || showCaseDialog"
                    >新建用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="deleteCaseInBatch"
                    :disabled="showCaseDialog"
                    >删除用例</el-button
                >

                <el-button
                    :size="buttonSize"
                    @click="exportTestCase"
                    :disabled="showCaseDialog"
                    >导出用例</el-button
                >

                <el-dropdown>
                    <el-button :size="buttonSize" :disabled="showCaseDialog">
                        更多操作
                        <i class="el-icon-arrow-down el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item>待开发操作</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-button-group>
            <el-button
                :size="buttonSize"
                type="primary"
                @click="assignCases"
                :disabled="showCaseDialog"
                >批量指派给</el-button
            >
            <el-select
                v-model="batchAssignedTo"
                value-key="id"
                filterable
                clearable
                placeholder="请选择"
                :size="buttonSize"
                style="width: 120px"
            >
                <el-option
                    v-for="item in userOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item"
                ></el-option>
            </el-select>
        </div>

        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryFrom" size="small">
                <!-- <el-form-item label="创建时间">
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
                </el-form-item>-->
                <el-form-item label="测试结果">
                    <el-select
                        v-model="queryFrom.result"
                        clearable
                        style="width: 95px"
                    >
                        <el-option label="未执行" value="未执行"></el-option>
                        <el-option label="通过" value="通过"></el-option>
                        <el-option label="失败" value="失败"></el-option>
                        <el-option label="阻塞" value="阻塞"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="执行阶段">
                    <el-select
                        v-model="queryFrom.executionPhase"
                        clearable
                        style="width: 110px"
                    >
                        <el-option
                            v-for="item in executionPhaseOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="指派给">
                    <el-select
                        v-model="queryFrom.assignedTo"
                        filterable
                        clearable
                        placeholder="请选择"
                        size="small"
                        style="width: 120px"
                    >
                        <el-option
                            v-for="item in userOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>

                <span v-if="!isQueryItemsCollapsed">
                    <el-form-item label="用例名称">
                        <el-input
                            v-model="queryFrom.caseName"
                            placeholder="用例名称"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="优先级">
                        <el-select
                            v-model="queryFrom.priority"
                            :multiple="true"
                            clearable
                            style="width: 215px"
                        >
                            <el-option label="P1" value="P1"></el-option>
                            <el-option label="P2" value="P2"></el-option>
                            <el-option label="P3" value="P3"></el-option>
                            <el-option label="P4" value="P4"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="执行方式">
                        <el-select
                            v-model="queryFrom.executionMethod"
                            clearable
                            style="width: 95px"
                        >
                            <el-option
                                label="手工"
                                value="handwork"
                            ></el-option>
                            <el-option
                                label="自动化"
                                value="automation"
                            ></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试人">
                        <el-select
                            v-model="queryFrom.testerId"
                            filterable
                            clearable
                            placeholder="请选择"
                            size="small"
                            style="width: 120px"
                        >
                            <el-option
                                v-for="item in userOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="是否显示子集用例">
                        <el-select
                            v-model="queryFrom.recursive"
                            style="width: 60px"
                        >
                            <el-option label="是" value="1"></el-option>
                            <el-option label="否" value="0"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="标签">
                        <el-input
                            v-model="queryFrom.tag"
                            placeholder="请输入标签"
                            style="width: 150px"
                        ></el-input>
                    </el-form-item>
                </span>
                <el-form-item>
                    <el-button
                        type="primary"
                        @click="queryRows('clickQuery')"
                        :disabled="showCaseDialog"
                        >查询</el-button
                    >
                    <el-button @click="restQueryRowsForm">重置</el-button>
                </el-form-item>

                <span
                    @click.prevent="toggleQueryItems"
                    style="
                        height: 32px;
                        line-height: 32px;
                        font-size: 14px;
                        color: #606266;
                    "
                >
                    <i
                        class="el-icon-arrow-up el-icon--right"
                        v-show="!isQueryItemsCollapsed"
                        >收起</i
                    >
                    <i
                        class="el-icon-arrow-down el-icon--right"
                        v-show="isQueryItemsCollapsed"
                        >展开</i
                    >
                </span>
            </el-form>
        </div>

        <!-- 表格 -->
        <el-table
            ref="myTable"
            :data="tableData"
            :empty-text="emptyText"
            border
            stripe
            :lazy="false"
            row-key="guid"
            :span-method="mergeColumns"
            :cell-class-name="getCellClassName"
            :row-class-name="getRowClassName"
            class="my-table"
            @row-click="clickRow"
            @select="onSelectRow"
            @select-all="onSelectAllRow"
            @sort-change="sortChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column
                type="selection"
                :width="checkBoxColWidth"
                align="center"
            ></el-table-column>
            <!-- <el-table-column
                prop="customNo"
                label="用例编号"
                width="150px"
                header-align="center"
                align="left"
            ></el-table-column>-->
            <el-table-column
                prop="name"
                label="用例名称"
                show-overflow-tooltip
                header-align="center"
                align="left"
                sortable="custom"
                min-width="250px"
            ></el-table-column>
            <el-table-column
                prop="priority"
                label="优先级"
                width="90px"
                header-align="center"
                align="center"
                sortable="custom"
            ></el-table-column>
            <el-table-column
                prop="assignedTo"
                label="指派给"
                width="115px"
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">
                    <el-select
                        v-model="scope.row.assignedTo"
                        filterable
                        placeholder="请选择"
                        size="mini"
                        value-key="id"
                        @change="onAssignedToChanged(scope.row)"
                        @visible-change="
                            onAssignedToVisibleChange($event, scope.row)
                        "
                    >
                        <el-option
                            v-for="item in userOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column
                prop="result"
                label="测试结果"
                width="90px"
                header-align="center"
                align="center"
                class="test-result-class"
            >
                <template slot-scope="scope">
                    <el-select
                        v-model="scope.row.result"
                        placeholder="请选择"
                        size="mini"
                        @change="onResultChanged(scope, scope.row)"
                        @visible-change="
                            onVisibleChange($event, scope.row.result)
                        "
                    >
                        <el-option
                            v-for="item in resultOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column
                prop="testerName"
                label="测试人"
                width="80px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="remark"
                label="测试备注"
                width="250px"
                header-align="center"
                show-overflow-tooltip
                align="left"
            ></el-table-column>
            <el-table-column label="操作" align="left" width="175px">
                <template slot-scope="scope">
                    <el-button
                        size="mini"
                        @click="editRemark(scope.$index, scope.row)"
                        v-if="scope.row.remark"
                        >修改备注</el-button
                    >
                    <el-button
                        size="mini"
                        @click="editRemark(scope.$index, scope.row)"
                        v-else
                        >添加备注</el-button
                    >
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteOneCase(scope.$index, scope.row)"
                        >删除</el-button
                    >
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

        <!--测试用例对话框组件-->
        <transition name="slide-fade">
            <sprint-case-dialog
                v-if="caseDialogLoaded"
                :caseDialogLoaded.sync="caseDialogLoaded"
                :caseDialogEditing.sync="caseDialogEditing"
                :caseDialogTitle.sync="caseDialogTitle"
                :caseDialogVisible.sync="showCaseDialog"
                :tableData.sync="tableData"
                :caseData="caseData"
                :row.sync="row"
                :currentPage.sync="currentPage"
                :pageSize="pageSize"
                :total.sync="total"
                :operation.sync="operation"
                :caseOrder.sync="caseOrder"
                :currentModule="currentModule"
                :resultOptions="resultOptions"
                :planRow="planRow"
                :priorityOptions="priorityOptions"
                :executionPhaseOptions="executionPhaseOptions"
                :executedEachSprintDict="executedEachSprintDict"
            ></sprint-case-dialog>
        </transition>

        <!-- 批量更新测试结果对话框 -->
        <update-result-dialog
            v-if="updateResultDlgVisible"
            :dialogVisible.sync="updateResultDlgVisible"
            :resultOptions="resultOptions"
            :caseIDsSelected="caseIDsSelected"
            :planRow="planRow"
        ></update-result-dialog>

        <!--批量更新测试用例对话框-->
        <batch-update-cases-dlg
            v-if="updateCasesDlgVisible"
            :dialogVisible.sync="updateCasesDlgVisible"
            :casesInfoForUpdate="casesInfoForUpdate"
            :suiteId="suiteID"
            :executionPhaseOptions="executionPhaseOptions"
            :executedEachSprintDict="executedEachSprintDict"
        ></batch-update-cases-dlg>

        <!-- 添加、修改测试备注对话框 -->
        <remark-dialog
            v-if="remarkDialogVisible"
            :dialogVisible.sync="remarkDialogVisible"
            :row="row"
        ></remark-dialog>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";
import SprintCaseDialog from "../SprintCase/SprintCaseDialog";
import BatchUpdateCasesDlg from "../SprintCase/BatchUpdateCasesDlg";
import UpdateResultDialog from "./UpdateResultDialog";
import RemarkDialog from "./RemarkDialog";

export default {
    mixins: [elTableMixin, elButtonMixin],
    props: ["planRow"],
    components: {
        SprintCaseDialog,
        UpdateResultDialog,
        RemarkDialog,
        BatchUpdateCasesDlg,
    },
    data() {
        return {
            // 查询表单
            queryFrom: {
                // startTime: "", // 起始时间
                // endTime: "", // 结束时间
                caseName: "", // 用例名称
                priority: [], // 优先级
                result: "", //测试结果
                executionPhase: "", // 执行阶段
                executionMethod: "handwork", // 执行方式
                recursive: "1", // 是否展示子套件测试用例
                testerId: "", // 测试人ID
                assignedTo: "", // 指派给ID
                // creater: "", // 创建人
                // updater: "", // 更新人
                tag: "", // 标签
                sort: "-id",
            },
            caseStepTableData: [], // 存放步骤表数据
            caseAttachmentList: [], // 存放测试用例附件
            caseData: null, // 测试用例相关数据，给对测试用例对话框使用
            pageSizes: [10, 15, 20, 25, 30, 40, 50, 100, 150], //每页显示记录数选择器的选项设置
            pageSize: 15, // 表格默认每页显示的记录数
            showCaseDialog: false, // 是否隐藏/显示测试用例对话框 true 显示，false 隐藏
            caseDialogLoaded: false, // 是否已加载对话框 true 已加载 false 未加载
            caseDialogEditing: false, // 测试用例对话框编辑状态 true 编辑状态 false 非编辑状态
            caseDialogTitle: "查看用例", // 测试用例对话框标题
            operation: "viewCase", // 存储用户操作 查看用例 viewCase 新建用例 newCase 编辑用例
            // suitePath: "", // 存放用户在左侧测试集树中点选的测试集的全路径
            caseIDsSelected: [], // 存放用户选取的用例ID，用于批量更新测试结果
            caseOrder: 0, // 用于记录用例顺序号,即属于第几条用例, 序号从1开始
            caseTestResult: "", // 用于临时存放用例测试结果更新前的结果值

            // 测试结果下拉选项
            resultOptions: [
                {
                    value: "通过",
                    label: "通过",
                },
                {
                    value: "失败",
                    label: "失败",
                },
                {
                    value: "阻塞",
                    label: "阻塞",
                },
                {
                    value: "未执行",
                    label: "未执行",
                },
            ],
            updateResultDlgVisible: false, // 批量修改测试结果对话框是否可见 true - 可见 false -不可见
            remarkDialogVisible: false, // 修改、添加测试备注对话框是否可见 true - 可见 false -不可见
            currentModule: "testPlanCaseTable", // 存放当前模块名称，用于标识在哪个模块编辑用例
            bindBugDialogVisible: false, // 关联新缺陷对话框是否可见 true - 可见 false -不可见
            userOptions: [], // 存放用户下拉列表
            assginedToOld: {}, // 用于临时存放用例“指派给”更新前的值
            batchAssignedTo: {}, // 存放批量“指派给”对象
            priorityOptions: [
                { label: "P1", value: "P1" },
                { label: "P2", value: "P2" },
                { label: "P3", value: "P3" },
                { label: "P4", value: "P4" },
            ],
            executionPhaseOptions: [], // 测试用例执行阶段选项
            executedEachSprintDict: {}, // 测试用例执行阶段和是否每次迭代都执行字典映射
            loading: false, // 标记是否正在加载
            elementLoadingText: "",
            updateCasesDlgVisible: false, // 标记批量更新测试用例对话框是否可见
            casesInfoForUpdate: [], // 存放用户选中的需要更新的测试用例必备信息
            isQueryItemsCollapsed: true, // 标记是否收起查询条件项
        };
    },
    methods: {
        // 重置查询表单
        restQueryRowsForm() {
            this.queryFrom.caseName = "";
            this.queryFrom.priority = [];
            this.queryFrom.executionPhase = "";
            this.queryFrom.executionMethod = "handwork";
            this.queryFrom.result = "";
            this.queryFrom.recursive = "1";
            this.queryFrom.testerId = "";
            this.queryFrom.assignedTo = "";
            this.queryFrom.tag = "";
        },
        // 获取测试用例
        queryRows(action, resolve, reject) {
            if (this.suiteID == -1 || this.suiteID == -2) {
                // suiteID为默认state值为-1、-2，此时不发送请求，因为取不到数据
                this.total = 0;
                this.tableData = [];
                return;
            }

            if (action == "clickQuery") {
                this.currentPage = 1;
            }

            let queryParams = Object.assign({}, this.queryFrom);
            queryParams["planId"] = this.planRow.id;
            queryParams["suiteId"] = this.suiteID;
            queryParams["suiteType"] = this.suiteType;
            queryParams["pageSize"] = this.pageSize;
            queryParams["pageNo"] = this.currentPage;
            queryParams.priority = queryParams.priority.join(",");

            // 向后台发送请求
            this.$api.testPlanCaseTable
                .getSuiteCases(queryParams)
                .then((res) => {
                    if (res.success) {
                        this.total = res.data.total;
                        this.tableData = res.data.rows;
                        if (resolve) {
                            resolve(res.success);
                        }
                    } else {
                        this.$message.error(res.msg);
                        if (reject) {
                            reject(res.success);
                        }
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                    if (reject) {
                        reject(res.success);
                    }
                });
        },
        // 合并列
        mergeColumns({ row, column, rowIndex, columnIndex }) {
            if (row.children.length) {
                if (columnIndex == 1) {
                    return [1, 8];
                } else if (columnIndex > 1) {
                    return [0, 0];
                }
            }
        },
        // 获取供表格记录行使用的类名
        getRowClassName(object) {
            if (object.row.children.length) {
                return "row-class-for-colspan";
            } else {
                return "row-class";
            }
        },
        // 展开表格折叠行数据
        expandAll() {
            this.$nextTick(function () {
                const els = this.$el.getElementsByClassName(
                    "el-table__expand-icon"
                );
                for (let i = 0; i < els.length; i++) {
                    if (
                        els[i]
                            .getAttribute("class")
                            .indexOf("el-table__expand-icon--expanded") == -1
                    ) {
                        // 如果行记录未展开，则展开记录行
                        els[i].click();
                    }
                }
            });
        },

        // 打开测试用例对话框
        // title 对话框标题
        // editingStatus 对话框编辑状态
        openCaseDialog(title, editingStatus) {
            if (!this.caseDialogLoaded) {
                // 未加载测试用例对话框则先加载
                this.caseDialogLoaded = true;
            }

            this.caseDialogTitle = title;
            this.caseDialogEditing = editingStatus;

            if (!this.showCaseDialog) {
                // 如果没打开对话框，则先打开对话框
                this.showCaseDialog = true;
            }
        },
        // 批量修改测试结果
        updateCaseTestResults() {
            if (!this.updateResultDlgVisible) {
                let caseIDArray = []; // 存放勾选的用例ID
                let rowsSelected = this.$refs.myTable.selection;
                for (let i = 0; i < rowsSelected.length; i++) {
                    if (!rowsSelected[i].children.length) {
                        // 勾选的记录为测试用例
                        caseIDArray.push(rowsSelected[i].id);
                    }
                }

                if (!caseIDArray.length) {
                    this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
                this.caseIDsSelected = caseIDArray;
                this.updateResultDlgVisible = true;
            }
        },
        // 通过点击测试结果下拉选框，手动修改测试结果时的事件触发函数
        onVisibleChange(event, result) {
            if (event) {
                // 记录更改前的值
                this.caseTestResult = result;
            }
        },
        onResultChanged(scope, row) {
            this.$api.testPlanCaseTable
                .updateCaseTestResult({
                    id: row.id,
                    result: row.result,
                    planId: row.testplanId,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);

                        // 更新用例表中的对应用例数据
                        for (let key in res.data.caseDataUpdated) {
                            if (key in row) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                row[key] = res.data.caseDataUpdated[key];
                            }
                        }
                        this.setTestResultStyle(scope.$index);

                        // 更新测试计划详情及测试计划表中对应测试计划信息
                        for (let key in res.data.planDataUpdated) {
                            if (key in this.planRow) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                this.planRow[key] =
                                    res.data.planDataUpdated[key];
                            }
                        }
                    } else {
                        // 还原数据
                        row["result"] = this.caseTestResult;
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    row["result"] = this.caseTestResult;
                    this.$message.error(res.msg);
                });
        },
        // 批量更新测试用例
        batchUpdateTestCases() {
            if (this.showCaseDialog) {
                this.$alert("请关闭当前打开的用例对话框后再操作", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }
            this.elementLoadingText = "正在批量更新测试用例，请勿进行其它操作";
            this.casesInfoForUpdate = []; // 存放用例guid
            let rowsSelected = this.$refs.myTable.selection;
            for (let i = 0; i < rowsSelected.length; i++) {
                if (!rowsSelected[i].children.length) {
                    // 勾选的记录不为测试套件
                    this.casesInfoForUpdate.push({
                        guid: rowsSelected[i].guid,
                        suiteId: rowsSelected[i].suiteId,
                        suite_type: rowsSelected[i].suiteType,
                        detailSuiteType: rowsSelected[i].detailSuiteType,
                        testplanId: rowsSelected[i].testplanId,
                    });
                }
            }

            if (!this.casesInfoForUpdate.length) {
                this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (!this.updateCasesDlgVisible) {
                // 如果没打开对话框，则先打开对话框
                this.updateCasesDlgVisible = true;
            }
        },
        // 新建用例
        newCase() {
            let executionPhase = [];
            for (let item in this.executedEachSprintDict) {
                if (this.executedEachSprintDict[item].default) {
                    executionPhase = [item];
                    break;
                }
            }

            this.caseData = {
                testplanId: this.planRow.id,
                suiteId: this.suiteID,
                productId: this.planRow.productId,
                sprintId: this.planRow.sprintId,
                suiteType: this.suiteType,
                customNo: "",
                name: "",
                createrName: "",
                updaterName: "",
                priority: "P3",
                executedEachSprint: "",
                executionMethod: "handwork",
                executionPhase: executionPhase,
                suitePath: this.suitePath,
                precondition: "",
                steps: [],
                postcondition: "",
                tags: [],
                desc: "",
                result: "未执行",
                remark: "",
            };

            this.operation = "newCase";
            this.openCaseDialog("新建用例", true); // 测试用例对话框默认进入编辑状态
        },
        // 点击表格用例行
        clickRow(row, column, event) {
            let handleFunc = () => {
                let counter = 0; // 计数器，用于计算用例所在行属于第几条用例
                let caseRowFound = false; // 标记是否找到测试用例
                for (let i = 0; i < this.tableData.length; i++) {
                    let testSuite = this.tableData[i];

                    if (testSuite.children.length) {
                        for (let i = 0; i < testSuite.children.length; i++) {
                            counter += 1;
                            let testCase = testSuite.children[i];
                            if (testCase.id == row.id) {
                                caseRowFound = true;
                                break;
                            }
                        }
                        if (caseRowFound) {
                            break;
                        }
                    }
                }
                this.caseOrder =
                    counter + (this.currentPage - 1) * this.pageSize;

                this.caseData = {
                    testplanId: row.testplanId,
                    suiteId: row.suiteId,
                    productId: row.productId,
                    sprintId: row.sprintId,
                    suiteType: row.suiteType,
                    detailSuiteType: row.detailSuiteType,
                    caseId: row.id,
                    guid: row.guid,
                    customNo: row.customNo,
                    name: row.name,
                    createrName: row.createrName,
                    updaterName: row.updaterName,
                    priority: row.priority,
                    executedEachSprint: row.executedEachSprint,
                    executionMethod: row.executionMethod,
                    executionPhase: row.executionPhase,
                    suitePath: row.suitePath,
                    precondition: row.precondition,
                    steps: JSON.parse(row.steps),
                    postcondition: row.postcondition,
                    desc: row.desc,
                    tags: row.tags,
                };

                this.operation = "viewCase";
                this.openCaseDialog("查看用例", false);
                this.row = row;
            };

            // 点击行非套件，并且非“操作”列,且列名称为用例名称
            if (!row.children.length && column && column.label == "用例名称") {
                if (this.caseDialogEditing) {
                    this.$confirm("您有正在编辑的用例，确定离开吗?", "提示", {
                        confirmButtonText: "确定",
                        cancelButtonText: "取消",
                        type: "warning",
                        cancelButtonClass: "btn-custom-cancel",
                    })
                        .then(() => {
                            handleFunc();
                        })
                        .catch(() => {});
                } else {
                    handleFunc();
                }
            }
        },
        // caseIDArray 用例ID数组，用于发送删除用例请求
        deleteCase(caseIDArray) {
            // 发送删除请求
            this.$api.testPlanCaseTable
                .deleteTestCases({
                    planId: this.planRow.id,
                    caseIds: caseIDArray,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.total = this.total - caseIDArray.length;

                        for (let i = 0; i < caseIDArray.length; i++) {
                            for (let x = 0; x < this.tableData.length; x++) {
                                // 遍历的id不为测试套件ID
                                let caseRowFound = false; // 标记是否找到测试用例
                                if (this.tableData[x].children.length) {
                                    // 在套件包含的测试用例中查找对应记录
                                    for (
                                        let y = 0;
                                        y < this.tableData[x].children.length;
                                        y++
                                    ) {
                                        if (
                                            this.tableData[x].children[y].id ==
                                            caseIDArray[i]
                                        ) {
                                            caseRowFound = true;
                                            this.tableData[x].children.splice(
                                                y,
                                                1
                                            ); // 删除本行数据
                                            if (
                                                !this.tableData[x].children
                                                    .length
                                            ) {
                                                // 所在测试集下没有其它测试用例，一并删除测试集
                                                this.tableData.splice(x, 1);
                                            }

                                            break;
                                        }
                                    }
                                    if (caseRowFound) {
                                        // 跳出外层循环 // 继续执行下一条删除用例
                                        break;
                                    }
                                }
                            }

                            // 更新测试计划详情及测试计划表中对应测试计划信息
                            for (let key in res.data) {
                                if (key in this.planRow) {
                                    this.planRow[key] = res.data[key];
                                }
                            }

                            if (!this.tableData.length && this.total != 0) {
                                // 如果本页数据都被删除

                                let totalPages = Math.ceil(
                                    this.total / this.pageSize
                                );

                                if (this.currentPage > totalPages) {
                                    // 当前页位于最后一页，翻页到前一页
                                    this.currentPage -= 1;
                                } else {
                                    // 直接刷新当前页
                                }

                                this.queryRows();
                                return;
                            }

                            // 重新设置tableData，使得仅仅删除用例(不含测试套件)时，更新界面视图
                            this.tableData = Object.assign([], this.tableData);
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                });
        },

        // 删除单条用例
        deleteOneCase(index, row) {
            if (this.showCaseDialog) {
                this.$alert("请关闭当前打开的用例对话框后再操作", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }
            this.$confirm("确定要删除该用例吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    // 发送删除请求
                    this.$api.testPlanCaseTable
                        .deleteTestCase({
                            id: row.id,
                            planId: row.testplanId,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.total = this.total - 1;

                                this.$message.success(res.msg);

                                for (
                                    let x = 0;
                                    x < this.tableData.length;
                                    x++
                                ) {
                                    let caseRowFound = false; // 标记是否找到测试用例
                                    if (this.tableData[x].children.length) {
                                        // 在套件包含的测试用例中查找对应记录
                                        for (
                                            let y = 0;
                                            y <
                                            this.tableData[x].children.length;
                                            y++
                                        ) {
                                            if (
                                                this.tableData[x].children[y]
                                                    .guid == row.guid
                                            ) {
                                                caseRowFound = true;
                                                this.tableData[
                                                    x
                                                ].children.splice(y, 1); // 删除本行数据

                                                if (
                                                    !this.tableData[x].children
                                                        .length
                                                ) {
                                                    // 所在测试集下没有其它测试用例，一并删除测试集
                                                    this.tableData.splice(x, 1);
                                                }

                                                break;
                                            }
                                        }
                                        if (caseRowFound) {
                                            // 跳出外层循环
                                            break;
                                        }
                                    }
                                }

                                // 更新测试计划详情及测试计划表中对应测试计划信息
                                for (let key in res.data) {
                                    if (key in this.planRow) {
                                        this.planRow[key] = res.data[key];
                                    }
                                }

                                if (!this.tableData.length && this.total != 0) {
                                    // 如果本页数据都被删除

                                    let totalPages = Math.ceil(
                                        this.total / this.pageSize
                                    );

                                    if (this.currentPage > totalPages) {
                                        // 当前页位于最后一页，翻页到前一页
                                        this.currentPage -= 1;
                                    } else {
                                        // 直接刷新当前页
                                    }

                                    this.queryRows();
                                    return;
                                }

                                // 重新设置tableData，(仅仅删除用例(不含测试套件)时，如果缺少以下代码，不会更新界面视图)
                                this.tableData = Object.assign(
                                    [],
                                    this.tableData
                                );
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg);
                        });
                })
                .catch(() => {});
        },
        //全选、取消全选
        onSelectAllRow(selection) {
            // 如果selection中能找到表数据中第一条记录，那么说明是全选，否则取消全选
            // 表中无记录时，无法手动勾选、取消勾选复选框，所以tableData至少存在一条记录
            if (selection.indexOf(this.tableData[0]) > -1) {
                // 全选
                // 勾选所有套件的子记录
                for (let i = 0; i < this.tableData.length; i++) {
                    for (
                        let j = 0;
                        j < this.tableData[i].children.length;
                        j++
                    ) {
                        this.$refs.myTable.toggleRowSelection(
                            this.tableData[i].children[j],
                            true
                        );
                    }
                }
            } else {
                // 取消全选
                this.$refs.myTable.clearSelection();
            }
        },
        //用户手动勾选记录（逐行，非通过复选框全选,并且是手动勾选）时的事件处理函数
        onSelectRow(selection, row) {
            let selected;
            if (!selection.length) {
                selected = false; // 取消勾选
            } else {
                for (let i = 0; i < selection.length; i++) {
                    if (selection[i].guid == row.guid) {
                        // 勾选记录
                        selected = true;
                        break;
                    } else {
                        // 取消勾选记录
                        selected = false;
                    }
                }
            }

            // 如果勾选\取消勾选的是测试集在测试用例表中的映射的记录，则勾选\取消勾选其子记录即用例
            if (row.children.length) {
                for (let j = 0; j < this.tableData.length; j++) {
                    if (this.tableData[j].guid == row.guid) {
                        for (
                            let i = 0;
                            i < this.tableData[j].children.length;
                            i++
                        ) {
                            this.$refs.myTable.toggleRowSelection(
                                this.tableData[j].children[i],
                                selected
                            );
                        }
                        break;
                    }
                }
            } else {
                // 如果勾选的是测试用例，则需要判断是否已勾选其所在测试集映射记录，如果没勾选则直接勾选，否则不做处理
                // 如果是取消勾选测试用例，暂且不做处理
                for (let i = 0; i < this.tableData.length; i++) {
                    // 查找用例所在测试集的映射记录
                    let suiteRowFound = false;
                    for (
                        let j = 0;
                        j < this.tableData[i].children.length;
                        j++
                    ) {
                        if (this.tableData[i].children[j].guid == row.guid) {
                            suiteRowFound = true;
                            if (selected) {
                                // 判断测试集是否已经勾选
                                let suiteChecked = false;
                                for (let x = 0; x < selection.length; x++) {
                                    if (
                                        selection[x].guid ==
                                        this.tableData[i].guid
                                    ) {
                                        suiteChecked = true;
                                        break;
                                    }
                                }
                                if (!suiteChecked) {
                                    // 未勾选，则勾选
                                    this.$refs.myTable.toggleRowSelection(
                                        this.tableData[i],
                                        true
                                    );
                                }
                            }
                            break;
                        }
                    }
                    if (suiteRowFound) {
                        break;
                    }
                }
            }
        },
        // 批量删除用例
        deleteCaseInBatch() {
            if (this.showCaseDialog) {
                this.$alert("请关闭当前打开的用例对话框后再操作", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }
            this.$confirm("确定要删除选中用例吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    let rowsSelected = this.$refs.myTable.selection;
                    let caseIDArray = []; // 存放用例ID

                    for (let i = 0; i < rowsSelected.length; i++) {
                        if (!rowsSelected[i].children.length) {
                            // 勾选的记录不为测试套件
                            caseIDArray.push(rowsSelected[i].id);
                        }
                    }

                    if (!caseIDArray.length) {
                        this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                            confirmButtonText: "确定",
                        });
                        return;
                    }

                    this.deleteCase(caseIDArray);
                })
                .catch(() => {});
        },

        // 导出用例
        exportTestCase() {
            this.$alert("功能待开发", "提示", {
                confirmButtonText: "确定",
            });

            return;
        },
        // 修改、添加测试备注
        editRemark(index, row) {
            if (!this.remarkDialogVisible) {
                this.remarkDialogVisible = true;
                this.row = row;
            }
        },

        // 获取用户列表
        getUserOptionsList() {
            this.$api.sysUser
                .getUsersDetails()
                .then((res) => {
                    if (res.success) {
                        this.userOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                });
        },
        // 通过点击“指派给”下拉选框，手动修改“指派给”时的事件触发函数
        onAssignedToVisibleChange(event, row) {
            if (event) {
                // 只记录更改前的值
                this.assginedToOld = {
                    id: row.assignedToId,
                    name: row.assignedTo,
                };
            }
        },
        // 修改“指派给”
        onAssignedToChanged(row) {
            let assignedToUserSelect = Object.assign({}, row.assignedTo);

            this.$api.testPlanCaseTable
                .updateTestCase({
                    id: row.id,
                    planId: row.testplanId,
                    assignedTo: row.assignedTo.name,
                    assignedToId: row.assignedTo.id,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);

                        // 更新用例表中的对应用例数据
                        for (let key in res.data) {
                            if (key in row) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                row[key] = res.data[key];
                            }
                        }
                    } else {
                        // 还原数据
                        row["assignedTo"] = this.assginedToOld.assignedTo;
                        row["assignedToId"] = this.assginedToOld.assignedToId;
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    row["assignedTo"] = this.assginedToOld.name;
                    row["assignedToId"] = this.assginedToOld.id;
                    this.$message.error(res.msg);
                });
        },
        // 批量指派用例
        assignCases() {
            let rowsSelected = [];
            let selection = this.$refs.myTable.selection;
            let caseIDArray = []; // 存放勾选的用例ID
            for (let i = 0; i < selection.length; i++) {
                if (!selection[i].children.length) {
                    // 勾选的记录为测试用例
                    caseIDArray.push(selection[i].id);
                    rowsSelected.push(selection[i]);
                }
            }

            if (!caseIDArray.length) {
                this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (
                !this.batchAssignedTo ||
                JSON.stringify(this.batchAssignedTo) == "{}"
            ) {
                this.$alert("请选择要指派的对象", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            this.$confirm(
                "确定要批量指派给 " + this.batchAssignedTo.name + " 吗?",
                "提示",
                {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                    cancelButtonClass: "btn-custom-cancel",
                }
            )
                .then(() => {
                    // 更新“指派给”
                    this.$api.testPlanCaseTable
                        .updateTestCases({
                            caseIds: caseIDArray,
                            batchAssignedTo: this.batchAssignedTo,
                            planId: this.planRow.id,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);
                                // 更新用例表中的对应用例数据
                                this.$nextTick(() => {
                                    const caseInfos = res.data;
                                    for (let i = 0; i < caseInfos.length; i++) {
                                        for (
                                            let j = 0;
                                            j < rowsSelected.length;
                                            j++
                                        ) {
                                            if (
                                                rowsSelected[j].id ==
                                                caseInfos[i].id
                                            ) {
                                                for (let key in caseInfos[i]) {
                                                    if (
                                                        key in
                                                            rowsSelected[j] &&
                                                        key != "id"
                                                    ) {
                                                        rowsSelected[j][key] =
                                                            caseInfos[i][key];
                                                    }
                                                }

                                                break;
                                            }
                                        }
                                    }
                                });
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg);
                        });
                })
                .catch(() => {});
        },
        // 监听排序操作
        sortChange(object) {
            let order = object.order;
            let property = object.prop;
            if (!property) {
                // 取消按字段排序
                property = "-id";
            } else {
                property = this.$customUtils.stringHandler.humpToUnderline(
                    property
                );
                if (property == "create_time") {
                    property = "id";
                }
            }

            if (order == "descending") {
                if (property == "priority") {
                    this.queryFrom.sort = "-" + property + ",-id";
                } else {
                    this.queryFrom.sort = "-" + property;
                }
            } else {
                if (property == "priority") {
                    this.queryFrom.sort = property + ",id";
                } else {
                    this.queryFrom.sort = property;
                }
            }

            this.queryRows();
        },
        // 获取测试阶段
        getTestPhases() {
            this.$api.testPhase
                .getTestPhasesDetails({
                    fields: "name,code,default",
                })
                .then((res) => {
                    if (res.success) {
                        for (let i = 0; i < res.data.length; i++) {
                            let label = res.data[i].name;
                            let value = res.data[i].code;
                            let defualt = res.data[i].default;
                            let temp = {
                                label: label,
                                value: value,
                                defualt: defualt,
                            };
                            this.executedEachSprintDict[value] = {};
                            this.executedEachSprintDict[value][
                                "executedEachSprint"
                            ] = "N";
                            this.executedEachSprintDict[value][
                                "executionPhase"
                            ] = res.data[i].name;
                            this.executedEachSprintDict[value][
                                "default"
                            ] = defualt;
                            this.executionPhaseOptions.push(temp);
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                });
        },

        // 修改当前页指定用例的测试结果的样式
        setTestResultStyle(index) {
            index += 1;
            if (this.$refs.myTable) {
                let testResult = this.$refs.myTable.$el.querySelector(
                    "tr:nth-child(" + index + ")"
                );

                if (testResult) {
                    let td = testResult.querySelector("td:nth-child(5)");
                    if (td) {
                        let testResultInputInner = td.querySelector(
                            ".el-input__inner"
                        );

                        let testResult = testResultInputInner.value;
                        if (testResult == "通过") {
                            testResultInputInner.style.cssText =
                                "font-weight:bold;color:green";
                        } else if (testResult == "阻塞") {
                            testResultInputInner.style.cssText =
                                "font-weight:bold;color:#B22222";
                        } else if (testResult == "失败") {
                            testResultInputInner.style.cssText =
                                "font-weight:bold;color:red";
                        } else {
                            testResultInputInner.style.cssText =
                                "font-weight:bold;color:black";
                        }
                    }
                }
            }
        },
        // 修改当前页所有测试结果的样式
        setTestResultsStyle() {
            if (this.$refs.myTable) {
                let testResults = this.$refs.myTable.$el.querySelectorAll(
                    "td:nth-child(5)"
                );
                testResults.forEach((element, index, srcArray) => {
                    let testResultInputInner = element.querySelector(
                        ".el-input__inner"
                    );

                    let testResult = testResultInputInner.value;
                    if (testResult == "通过") {
                        testResultInputInner.style.cssText =
                            "font-weight:bold;color:green";
                    } else if (testResult == "阻塞") {
                        testResultInputInner.style.cssText =
                            "font-weight:bold;color:#B22222";
                    } else if (testResult == "失败") {
                        testResultInputInner.style.cssText =
                            "font-weight:bold;color:red";
                    } else {
                        testResultInputInner.style.cssText =
                            "font-weight:bold;color:black";
                    }
                });
            }
        },

        // 折叠/展开用例查询条件
        toggleQueryItems() {
            this.isQueryItemsCollapsed = !this.isQueryItemsCollapsed;
        },
    },
    watch: {
        suiteID: function () {
            this.currentPage = 1;
            this.queryRows();
            this.caseDialogEditing = false;
            this.showCaseDialog = false;
            this.caseDialogLoaded = false;
        },
    },
    computed: {
        ...mapState({
            suiteType: (state) => state.sprintCaseSuite.suiteType,
            suiteID: (state) => state.sprintCaseSuite.suiteID,
            suitePath: (state) => state.sprintCaseSuite.suitePath,
            parentID: (state) => state.sprintCaseSuite.parentID,
        }),
        iscurrSuiteRoot: {
            get() {
                if (this.parentID == -1) {
                    return true;
                } else {
                    return false;
                }
            },
        },
    },
    created() {
        try {
            this.getUserOptionsList();
            this.getTestPhases();
        } catch (err) {
            this.$message.error(err.message);
        }
    },

    updated() {
        this.setTableBodySize(); // 设置表格高度

        this.expandAll(); // 数据更新后展开折叠行
        this.$nextTick(() => {
            this.setTestResultsStyle();
        });
    },
};
</script>

<style lang="scss">
.my-table {
    .el-table__header-wrapper {
        th {
            padding-top: 1px !important;
            padding-bottom: 1px !important;
        }
    }

    // 设置用例名称靠左展示
    .el-table__placeholder {
        width: 0px;
    }
    .el-table__indent {
        padding-left: 0px !important;
    }

    .row-class-for-colspan {
        background: rgb(231, 229, 229);
        td {
            padding-top: 1px !important;
            padding-bottom: 1px !important;
        }

        .cell {
            color: grey;
            height: auto !important;
            width: 100% !important;
        }
    }

    .row-class {
        td {
            padding-top: 3px !important;
            padding-bottom: 3px !important;
            // 设置下拉框高度
            .el-select,
            .el-input,
            .el-input__inner {
                height: auto !important;
            }
        }
        .cell {
            height: auto !important;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }
    }
}
</style>
