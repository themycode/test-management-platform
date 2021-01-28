<template>
    <div
        class="view-wrapper"
        ref="viewWrapper"
        v-resize="setTableBodySize"
        v-loading="loading"
        :element-loading-text="elementLoadingText"
    >
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="执行阶段">
                    <el-select
                        v-model="queryForm.executionPhase"
                        clearable
                        style="width: 115px"
                    >
                        <el-option
                            v-for="item in executionPhaseOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="是否每个迭代都执行">
                    <el-select
                        v-model="queryForm.executedEachSprint"
                        clearable
                        style="width: 85px"
                    >
                        <el-option label="是" value="Y"></el-option>
                        <el-option label="否" value="N"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item
                    label="仅显示历史迭代用例"
                    v-if="currentModule == 'bindPlanAndCaseDialog'"
                >
                    <el-select
                        v-model="queryForm.showHistoryOnly"
                        clearable
                        style="width: 85px"
                    >
                        <el-option label="是" value="1"></el-option>
                        <el-option label="否" value="0"></el-option>
                    </el-select>
                </el-form-item>

                <span v-if="!isQueryItemsCollapsed">
                    <el-form-item label="创建时间">
                        <el-date-picker
                            style="width: 330px"
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
                    <el-form-item label="优先级">
                        <el-select
                            v-model="queryForm.priority"
                            :multiple="true"
                            clearable
                            style="width: 170px"
                        >
                            <el-option
                                v-for="item in priorityOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="执行方式">
                        <el-select
                            v-model="queryForm.executionMethod"
                            clearable
                            @clear="clearExecutionMethod"
                            style="width: 85px"
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
                    <el-form-item label="是否显示子集用例">
                        <el-select
                            v-model="queryForm.recursive"
                            style="width: 60px"
                        >
                            <el-option label="是" value="1"></el-option>
                            <el-option label="否" value="0"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="用例名称">
                        <el-input
                            v-model="queryForm.name"
                            placeholder="请输入用例名称"
                            :style="getInputWidthStyle(queryForm.name, 125)"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="创建人">
                        <el-input
                            v-model="queryForm.creater"
                            placeholder="请输入"
                            :style="getInputWidthStyle(queryForm.creater, 85)"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="更新人">
                        <el-input
                            v-model="queryForm.updater"
                            placeholder="请输入"
                            :style="getInputWidthStyle(queryForm.creater, 85)"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="标签">
                        <el-input
                            v-model="queryForm.tag"
                            placeholder="请输入标签"
                            :style="getInputWidthStyle(queryForm.creater, 110)"
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
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button
                    :size="buttonSize"
                    @click="newCase"
                    :disabled="iscurrSuiteRoot || showCaseDialog"
                    >新建用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="batchDeleteCases"
                    :disabled="showCaseDialog"
                    >删除用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="copyTestCasesToSprint"
                    :disabled="showCaseDialog || suiteType == 'base'"
                    >克隆至迭代</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="copyCases"
                    :disabled="showCaseDialog"
                    >复制用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="cutCases"
                    :disabled="showCaseDialog"
                    >剪切用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    :disabled="showCaseDialog"
                    @click="importTestCases"
                    >导入用例</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="exportTestCases"
                    :disabled="showCaseDialog"
                    >导出用例(Excel)</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="exportXmindTestCases"
                    :disabled="showCaseDialog"
                    >导出用例(XMind)</el-button
                >
                <el-button
                    :size="buttonSize"
                    @click="batchUpdateTestCases"
                    :disabled="showCaseDialog"
                    >批量修改用例</el-button
                >
                <el-dropdown>
                    <el-button :size="buttonSize" :disabled="showCaseDialog">
                        更多操作
                        <i class="el-icon-arrow-down el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item>其它操作</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-button-group>
        </div>
        <!-- 表格 -->
        <el-table
            ref="myTable"
            :data="tableData"
            border
            stripe
            :empty-text="emptyText"
            class="my-table sprint-testcase-table"
            :lazy="false"
            row-key="guid"
            :span-method="mergeColumns"
            :cell-class-name="getCellClassName"
            :row-class-name="getRowClassName"
            @row-click="clickRow"
            @selection-change="onSelectChange"
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
            <!-- <el-table-column
                prop="executionMethod"
                label="执行方式"
                width="80px"
                header-align="center"
                align="center"
            ></el-table-column>-->
            <el-table-column
                prop="createrName"
                label="创建人"
                width="90px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updaterName"
                label="更新人"
                width="90px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="createTime"
                label="创建时间"
                width="160px"
                header-align="center"
                align="center"
                sortable="custom"
            ></el-table-column>
            <el-table-column
                prop="updateTime"
                label="更新时间"
                width="160px"
                header-align="center"
                align="center"
                sortable="custom"
            ></el-table-column>
            <el-table-column label="操作" align="left" width="205px">
                <template slot-scope="scope">
                    <!-- <el-button
                        size="mini"
                        @click="editCase(scope.$index, scope.row)"
                    >编辑</el-button>-->
                    <el-button
                        size="mini"
                        @click="viewCase(scope.$index, scope.row)"
                        >查看</el-button
                    >
                    <el-button
                        size="mini"
                        @click="copyCase(scope.$index, scope.row)"
                        >复制</el-button
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
                :priorityOptions="priorityOptions"
                :executionPhaseOptions="executionPhaseOptions"
                :executedEachSprintDict="executedEachSprintDict"
            ></sprint-case-dialog>
        </transition>

        <!-- 导入测试用例对话框 -->
        <import-case-dialog
            v-if="importCaseDialogVisible"
            :dialogVisible.sync="importCaseDialogVisible"
            :dataForImportCase="dataForImportCase"
        ></import-case-dialog>

        <!-- 克隆用例到迭代对话框 -->
        <copy-case-to-sprint-dlg
            v-if="copyCaseToSprintDlgVisible"
            :dialogVisible.sync="copyCaseToSprintDlgVisible"
            :currentModule="currentModule"
        ></copy-case-to-sprint-dlg>

        <!--批量更新测试用例对话框-->
        <batch-update-cases-dlg
            v-if="updateCasesDlgVisible"
            :dialogVisible.sync="updateCasesDlgVisible"
            :casesInfoForUpdate="casesInfoForUpdate"
            :suiteId="suiteID"
            :executionPhaseOptions="executionPhaseOptions"
            :executedEachSprintDict="executedEachSprintDict"
        ></batch-update-cases-dlg>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

import SprintCaseDialog from "./SprintCaseDialog";
import ImportCaseDialog from "./ImportCaseDialog";
import CopyCaseToSprintDlg from "./CopyCaseToSprintDlg";
import BatchUpdateCasesDlg from "./BatchUpdateCasesDlg";

export default {
    mixins: [elTableMixin, elButtonMixin],
    props: [
        "currentModule",
        "relatedCaseGuidList",
        "testplanId",
        "productID",
        "sprintID",
    ],
    data() {
        return {
            // 查询表单
            queryForm: {
                startTime: "", // 起始时间
                endTime: "", // 结束时间
                name: "", // 用例名称
                priority: [], // 优先级
                executionPhase: "", // 执行阶段
                executionMethod: "handwork", // 执行方式
                executedEachSprint: "", // 是否每个迭代都执行
                showHistoryOnly: "", // 仅显示历史迭代用例
                recursive: "1", // 是否展示子套件测试用例
                creater: "", // 创建人
                updater: "", // 更新人
                tag: "", // 标签
                sort: "-id", // 排序列
            },
            caseData: null, // 测试用例数据，给对测试用例对话框使用
            pageSizes: [10, 15, 20, 25, 30, 40, 50, 100, 150], //每页显示记录数选择器的选项设置
            pageSize: 15, // 表格默认每页显示的记录数
            showCaseDialog: false, // 是否隐藏/显示测试用例对话框 true 显示，false 隐藏
            caseDialogLoaded: false, // 是否已加载对话框 true 已加载 false 未加载
            caseDialogEditing: false, // 测试用例对话框编辑状态 true 编辑状态 false 非编辑状态
            caseDialogTitle: "查看用例", // 测试用例对话框标题
            operation: "viewCase", // 存储用户操作 查看用例 viewCase 新建 newCase 编辑用例 editCase 复制用例 copyCase 删除用例 deleteCase
            guidsOfRelatedOldCases: [], // 存放每次页面重新加载完成时，当前页面默认选中的行记录ID，给测试计划管理页面，获取当前页面计划已关联记录使用
            caseOrder: 1, // 用于记录用例顺序号,即属于第几条用例, 序号从1开始
            importCaseDialogVisible: false, // 导入用例对话框是否可见标识 true - 可见 false -不可见
            copyCaseToSprintDlgVisible: false, // 克隆用例到迭代对话框是否可见标识 true - 可见 false -不可见
            dataForImportCase: {}, // 存放导入用例所需的额外数据
            casesCopyToSprint: [], // 存放需要克隆到迭代项目的用例
            priorityOptions: [
                { label: "P1", value: "P1" },
                { label: "P2", value: "P2" },
                { label: "P3", value: "P3" },
                { label: "P4", value: "P4" },
            ],
            executionPhaseOptions: [], // 测试用例执行阶段选项
            executedEachSprintDict: {}, // 测试用例执行阶段和是否每次迭代都执行字典映射
            loading: false, // 标记是否正在导出测试用例
            elementLoadingText: "",
            updateCasesDlgVisible: false, // 标记批量更新测试用例对话框是否可见
            casesInfoForUpdate: [], // 存放用户选中的需要更新的测试用例必备信息
            confirmRadioValue: "1", // confirm消息弹窗 radio按钮value默认值
            isQueryItemsCollapsed: true,
        };
    },
    components: {
        SprintCaseDialog,
        ImportCaseDialog,
        CopyCaseToSprintDlg,
        BatchUpdateCasesDlg,
    },
    methods: {
        // 重置查询表单
        restQueryRowsForm() {
            // this.$refs["caseTableQueryForm"].resetFields(); // 不起作用
            this.queryForm.startTime = "";
            this.queryForm.endTime = "";
            this.queryForm.name = "";
            this.queryForm.priority = [];
            this.queryForm.executionPhase = "";
            this.queryForm.executionMethod = "handwork";
            this.queryForm.executedEachSprint = "";
            this.queryForm.recursive = "1";
            this.queryForm.creater = "";
            this.queryForm.updater = "";
            this.queryForm.tag = "";
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

            let queryParams = Object.assign({}, this.queryForm);
            queryParams["suiteId"] = this.suiteID;
            // queryParams["productId"] = this.productID
            queryParams["suiteType"] = this.suiteType;
            queryParams["pageSize"] = this.pageSize;
            queryParams["pageNo"] = this.currentPage;
            queryParams["testplanId"] = this.testplanId;
            queryParams["sprintId"] = this.sprintID;
            queryParams.priority = queryParams.priority.join(",");

            // 向后台发送请求
            this.$api.sprintCaseTable
                .getSuiteCases(queryParams)
                .then((res) => {
                    if (res.success) {
                        this.total = res.data.total;
                        this.tableData = res.data.rows;

                        // 自动勾选计划关联的用例
                        if (this.currentModule == "bindPlanAndCaseDialog") {
                            this.checkCaseRow(
                                res.data.testplanRelatedCaseGuids
                            );
                            this.guidsOfRelatedOldCases =
                                res.data.testplanRelatedCaseGuids;
                        }
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
                    this.$message.error(res.msg || res.message);
                    if (reject) {
                        reject(res.success);
                    }
                });
        },
        // 合并列
        mergeColumns({ row, column, rowIndex, columnIndex }) {
            if (row.children.length) {
                if (columnIndex == 1) {
                    return [1, 7];
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

        // 自动勾选计划关联的用例
        checkCaseRow(testplanRelatedCaseGuids) {
            this.$nextTick(() => {
                for (let j = 0; j < this.tableData.length; j++) {
                    //只在测试用例中查找已关联记录id
                    for (
                        let i = 0;
                        i < this.tableData[j].children.length;
                        i++
                    ) {
                        if (
                            testplanRelatedCaseGuids &&
                            testplanRelatedCaseGuids.indexOf(
                                this.tableData[j].children[i].guid
                            ) != -1
                        ) {
                            this.$refs.myTable.toggleRowSelection(
                                this.tableData[j].children[i],
                                true
                            );
                        }
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
                suiteId: this.suiteID,
                productId: this.productID,
                sprintId: this.sprintID,
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
                    suiteId: row.suiteId,
                    productId: row.productId,
                    sprintId: row.sprintId,
                    suiteType: row.suiteType,
                    caseId: row.id,
                    guid: row.guid,
                    customNo: row.customNo,
                    name: row.name,
                    createrName: row.createrName,
                    updaterName: row.updaterName, // 更新人
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
                this.row = row;
                this.openCaseDialog("查看用例", false);
            };

            // 点击行非套件，并且非“操作”列
            if (!row.children.length && column && column.label != "操作") {
                if (this.caseDialogEditing) {
                    this.$confirm(
                        "您有正在编辑的用例，确定继续操作吗?",
                        "提示",
                        {
                            confirmButtonText: "确定",
                            cancelButtonText: "取消",
                            type: "warning",
                            cancelButtonClass: "btn-custom-cancel",
                        }
                    )
                        .then(() => {
                            handleFunc();
                        })
                        .catch(() => {});
                } else {
                    handleFunc();
                }
            }
        },
        // 点击“查看”按钮
        viewCase(index, row) {
            this.caseData = {
                caseId: row.id, // 测试用例ID
                guid: row.guid,
                suiteId: row.suiteId,
                productId: row.productId,
                sprintId: row.sprintId,
                suiteType: row.suiteType, // 测试集类型
                customNo: row.customNo, // 定义用例编号
                name: row.name, // 用例名称
                createrName: row.createrName, // 创建人
                updaterName: row.updaterName, // 更新人
                priority: row.priority, // 优先级
                executedEachSprint: row.executedEachSprint,
                executionMethod: row.executionMethod,
                executionPhase: row.executionPhase,
                suitePath: row.suitePath, // 测试集路径
                precondition: row.precondition, // 前置条件
                steps: JSON.parse(row.steps), // 用例步骤
                postcondition: row.postcondition, //后置条件
                desc: row.desc, // 用例描述
                tags: row.tags, // 存放测试用例标签
            };

            this.operation = "viewCase";
            this.row = row;
            this.openCaseDialog("查看用例", false);
        },
        // 复制用例
        copyCase(index, row) {
            this.caseData = {
                guid: row.guid,
                suiteId: row.suiteId,
                sprintId: row.sprintId,
                productId: row.productId,
                suiteType: row.suiteType, // 测试集类型
                customNo: row.customNo, // 定义用例编号
                name: row.name + "-副本", // 用例名称
                createrName: "",
                updaterName: "", // 更新人
                priority: row.priority, // 优先级
                executedEachSprint: row.executedEachSprint,
                executionMethod: row.executionMethod,
                executionPhase: row.executionPhase,
                suitePath: row.suitePath, // 测试集路径
                precondition: row.precondition, // 前置条件
                steps: JSON.parse(row.steps), // 用例步骤
                postcondition: row.postcondition, //后置条件
                desc: row.desc, // 用例描述
                tags: row.tags, // 存放测试用例标签
            };

            this.row = row;
            this.operation = "copyCase";
            this.openCaseDialog("复制用例", true);
        },
        // caseGuidArray 用例guid数组，用于发送删除用例请求
        deleteCases(caseGuidArray) {
            this.elementLoadingText = "正在删除测试用例，请勿进行其它操作";
            this.loading = true;
            // 发送删除请求
            this.$api.sprintCaseTable
                .deleteTestCases({
                    suiteId: this.suiteID,
                    guids: caseGuidArray,
                    suiteType: this.suiteType,
                    delBaseCasesCascade: this.confirmRadioValue,
                })
                .then((res) => {
                    this.loading = false;
                    if (res.success) {
                        // 减少记录总数
                        this.total = this.total - caseGuidArray.length;

                        this.$message.success(res.msg);

                        for (let i = 0; i < caseGuidArray.length; i++) {
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
                                            this.tableData[x].children[y]
                                                .guid == caseGuidArray[i]
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

                            // 当前页面数据被删除后的处理工作 // 如果本页数据都被删除//并且还存在其它数据页
                            if (!this.tableData.length && this.total != 0) {
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
                    this.loading = false;
                    this.$message.error(res.msg || res.message);
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

            this.confirmRadioValue = "1";
            const h = this.$createElement;

            var comfirmMessage = undefined;
            if (this.suiteType == "sprint") {
                comfirmMessage = h("div", null, [
                    h("div", "请选择是否级联删除关联的基线测试用例"),
                    h("br"),
                    h("span", null, [
                        h(
                            "el-radio",
                            {
                                attrs: {
                                    label: "1",
                                    value: this.confirmRadioValue,
                                },
                                ref: "radio1",
                                // key: this._uid,
                                nativeOn: {
                                    input: (event) => {
                                        this.confirmRadioValue = "1";
                                        this.$nextTick(() => {
                                            this.$refs.radio1.value = "1";
                                            this.$refs.radio2.value = "1";
                                        });
                                    },
                                },
                            },
                            "级联删除"
                        ),
                        h("span", "    "),
                    ]),
                    h("span", [
                        h(
                            "el-radio",
                            {
                                attrs: {
                                    label: "2",
                                    value: this.confirmRadioValue,
                                },
                                ref: "radio2",
                                // key: this._uid + 1,

                                nativeOn: {
                                    input: (event) => {
                                        this.confirmRadioValue = "2";
                                        this.$nextTick(() => {
                                            this.$refs.radio1.value = "2";
                                            this.$refs.radio2.value = "2";
                                        });
                                    },
                                },
                            },
                            "不删除"
                        ),
                    ]),
                ]);
            } else {
                comfirmMessage = "确定要删除该用例吗";
            }

            this.$msgbox({
                title: "提示",
                message: comfirmMessage,
                showCancelButton: true,
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                cancelButtonClass: "btn-custom-cancel",
            })
                // this.$confirm("确定要删除该用例吗?", "提示", {
                //     confirmButtonText: "确定",
                //     cancelButtonText: "取消",
                //     type: "warning",
                //     cancelButtonClass: "btn-custom-cancel"
                // })
                .then(() => {
                    // 发送删除请求
                    this.$api.sprintCaseTable
                        .deleteTestCase({
                            suiteId: row.suiteId,
                            caseId: row.id,
                            guid: row.guid,
                            suiteType: row.suiteType,
                            delBaseCasesCascade: this.confirmRadioValue,
                        })
                        .then((res) => {
                            if (res.success) {
                                // 减少记录总数
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
                            this.$message.error(res.msg || res.message);
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
        //用户手动勾选记录（逐行，非通过全选复选框,并且是手动勾选）时的事件处理函数
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
                for (let i = 0; i < row.children.length; i++) {
                    this.$refs.myTable.toggleRowSelection(
                        row.children[i],
                        selected
                    );
                }
            } else {
                // 如果勾选的是测试用例，则需要判断是否已勾选其所在测试集映射记录，否则直接勾选
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
        batchDeleteCases() {
            if (this.showCaseDialog) {
                this.$alert("请关闭当前打开的用例对话框后再操作", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            this.confirmRadioValue = "1";
            const h = this.$createElement;
            var comfirmMessage = undefined;
            if (this.suiteType == "sprint") {
                comfirmMessage = h("div", null, [
                    h("div", "请选择是否级联删除关联的基线测试用例"),
                    h("br"),
                    h("span", null, [
                        h(
                            "el-radio",
                            {
                                attrs: {
                                    label: "1",
                                    value: this.confirmRadioValue,
                                },
                                ref: "radio1",
                                key: this._uid,
                                nativeOn: {
                                    input: (event) => {
                                        this.confirmRadioValue = "1";
                                        this.$nextTick(() => {
                                            this.$refs.radio1.value = "1";
                                            this.$refs.radio2.value = "1";
                                        });
                                    },
                                },
                            },
                            "级联删除"
                        ),
                        h("span", "    "),
                    ]),
                    h("span", [
                        h(
                            "el-radio",
                            {
                                attrs: {
                                    label: "2",
                                    value: this.confirmRadioValue,
                                },
                                ref: "radio2",
                                key: this._uid + 1,

                                nativeOn: {
                                    input: (event) => {
                                        this.confirmRadioValue = "2";
                                        this.$nextTick(() => {
                                            this.$refs.radio1.value = "2";
                                            this.$refs.radio2.value = "2";
                                        });
                                    },
                                },
                            },
                            "不删除"
                        ),
                    ]),
                ]);
            } else {
                comfirmMessage = "确定要删除选中用例吗";
            }

            this.$msgbox({
                title: "提示",
                message: comfirmMessage,
                showCancelButton: true,
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    let caseGuidArray = []; // 存放用例guid
                    let rowsSelected = this.$refs.myTable.selection;

                    for (let i = 0; i < rowsSelected.length; i++) {
                        if (!rowsSelected[i].children.length) {
                            // 勾选的记录不为测试套件
                            caseGuidArray.push(rowsSelected[i].guid);
                        }
                    }

                    if (!caseGuidArray.length) {
                        this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                            confirmButtonText: "确定",
                        });
                        this.loading = false;
                        return;
                    }

                    this.deleteCases(caseGuidArray);
                })
                .catch(() => {});
        },
        // 导入用例
        importTestCases() {
            if (!this.suiteID) {
                this.$message.error(
                    "操作失败，请先选择要待上传测试用例归属的测试套件"
                );
            }
            this.elementLoadingText = "正在导入测试用例，请勿进行其它操作";
            this.dataForImportCase["suiteType"] = this.suiteType;
            this.dataForImportCase["suiteId"] = this.suiteID;
            this.dataForImportCase["productId"] = this.productID;
            this.importCaseDialogVisible = true;
        },

        // 复制用例到迭代对话框
        copyTestCasesToSprint() {
            this.casesCopyToSprint = [];
            let rowsSelected = this.$refs.myTable.selection;
            for (let i = 0; i < rowsSelected.length; i++) {
                if (!rowsSelected[i].children.length) {
                    // 勾选的记录不为测试套件
                    this.casesCopyToSprint.push(rowsSelected[i]);
                }
            }

            if (!this.casesCopyToSprint.length) {
                this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }
            this.copyCaseToSprintDlgVisible = true;
        },
        // 拷贝用例
        copyCases() {
            let caseArray = []; // 存放用例guid
            let rowsSelected = this.$refs.myTable.selection;

            for (let i = 0; i < rowsSelected.length; i++) {
                if (!rowsSelected[i].children.length) {
                    // 勾选的记录不为测试套件
                    caseArray.push(rowsSelected[i]);
                }
            }

            if (!caseArray.length) {
                this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            this.$store.commit("setTestcasesCut", []); // 设置被剪切用例为空
            this.$store.commit("setTestcasesCopied", caseArray);
            this.$message.success("拷贝成功，请右键左侧目标测试集黏贴");
        },
        // 剪切用例
        cutCases() {
            let caseArray = []; // 存放用例guid
            let rowsSelected = this.$refs.myTable.selection;
            for (let i = 0; i < rowsSelected.length; i++) {
                if (!rowsSelected[i].children.length) {
                    // 勾选的记录不为测试套件
                    caseArray.push(rowsSelected[i]);
                }
            }

            if (!caseArray.length) {
                this.$alert("未选择用例，请勾选至少一条用例", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            this.$store.commit("setTestcasesCopied", []); // 设置被复制用例为空
            this.$store.commit("setTestcasesCut", caseArray);
            this.$message.success("剪切成功，请右键左侧目标测试集黏贴");
        },

        // 导出用例(Excel)
        exportTestCases() {
            this.$confirm("确定导出所查询的用例吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.elementLoadingText =
                        "正在导出测试用例，请勿进行其它操作";
                    this.loading = true;
                    let queryParams = Object.assign({}, this.queryForm);
                    queryParams["suiteId"] = this.suiteID;
                    // queryParams["productId"] = this.productID
                    queryParams["suiteType"] = this.suiteType;
                    queryParams["testplanId"] = this.testplanId;
                    queryParams.priority = queryParams.priority.join(",");

                    // 向后台发送请求
                    this.$api.sprintCaseTable
                        .exportTestCases(queryParams)
                        .then((res) => {
                            let link = document.createElement("a");
                            let blob = new Blob([res.data], {
                                type: "application/vnd.ms-excel",
                            });
                            link.style.display = "none";
                            link.href = window.URL.createObjectURL(blob);
                            // link.setAttribute(
                            //     "download",
                            //     "导出用例" +
                            //         this.$customUtils.dateTimeHandler.datetimeToString(
                            //             new Date()
                            //         ) +
                            //         ".xlsx"
                            // );
                            let disposition =
                                res.headers["content-disposition"];
                            let filename = decodeURI(
                                disposition.replace("attachment;filename=", "")
                            );

                            link.setAttribute("download", filename);

                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            this.loading = false;
                        })
                        .catch((res) => {
                            this.loading = false;
                            if (
                                Object.prototype.toString.call(
                                    res.response.data
                                ) == "[object Blob]"
                            ) {
                                let reader = new FileReader();
                                reader.onload = (e) => {
                                    let responseData = JSON.parse(
                                        e.target.result
                                    );
                                    this.$message.error(
                                        res.msg ||
                                            res.message + ":" + responseData.msg
                                    );
                                };
                                reader.readAsText(res.response.data);
                            } else {
                                this.$message.error(res.msg || res.message);
                            }
                        });
                })
                .catch(() => {
                    this.loading = false;
                });
        },
        // 导出用例(XMind)
        exportXmindTestCases() {
            this.$confirm("确定导出所查询的用例吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.loading = true;
                    let queryParams = Object.assign({}, this.queryForm);
                    queryParams["suiteId"] = this.suiteID;
                    // queryParams["productId"] = this.productID
                    queryParams["suiteType"] = this.suiteType;
                    queryParams["testplanId"] = this.testplanId;
                    queryParams.priority = queryParams.priority.join(",");

                    // 向后台发送请求
                    this.$api.sprintCaseTable
                        .exportXmindTestCases(queryParams)
                        .then((res) => {
                            let link = document.createElement("a");
                            let blob = new Blob([res.data], {
                                type: "application/octet-stream",
                            });
                            link.style.display = "none";
                            link.href = window.URL.createObjectURL(blob);
                            let disposition =
                                res.headers["content-disposition"];
                            let filename = decodeURI(
                                disposition.replace("attachment;filename=", "")
                            );

                            link.setAttribute("download", filename);

                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            this.loading = false;
                        })
                        .catch((res) => {
                            this.loading = false;
                            if (
                                Object.prototype.toString.call(
                                    res.response.data
                                ) == "[object Blob]"
                            ) {
                                let reader = new FileReader();
                                reader.onload = (e) => {
                                    let responseData = JSON.parse(
                                        e.target.result
                                    );
                                    this.$message.error(
                                        res.msg ||
                                            res.message + ":" + responseData.msg
                                    );
                                };
                                reader.readAsText(res.response.data);
                            } else {
                                this.$message.error(res.msg || res.message);
                            }
                        });
                })
                .catch(() => {
                    this.loading = false;
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

        // 清空执行方式时的事件处理函数
        clearExecutionMethod() {
            this.queryForm.executionMethod = "";
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
                    this.queryForm.sort = "-" + property + ",-id";
                } else {
                    this.queryForm.sort = "-" + property;
                }
            } else {
                if (property == "priority") {
                    this.queryForm.sort = property + ",id";
                } else {
                    this.queryForm.sort = property;
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
                            ] = label;
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
                    this.$message.error(res.msg || res.message);
                });
        },
        toggleQueryItems() {
            this.isQueryItemsCollapsed = !this.isQueryItemsCollapsed;
        },
        getInputWidthStyle(string, initWidth) {
            let style = "width:" + initWidth + "px";
            if (string) {
                let tempWidth = this.$customUtils.stringHandler.getTextPixelWith(
                    string,
                    "400 13.3333px Arial"
                ); //
                if (tempWidth > initWidth - 32) {
                    //初始宽度110px - 32px  //  32为输入框padding-left + padding-right + border-left + border-right之和
                    style = "width:" + (tempWidth + 40) + "px"; // 40=32+8 # 8 预留宽度
                }
            }
            return style;
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
            suitePath: (state) => state.sprintCaseSuite.suitePath,
            suiteID: (state) => state.sprintCaseSuite.suiteID,
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
    },
    created() {
        try {
            this.getTestPhases();
        } catch (err) {
            this.$message.error(err.message);
        }
    },
    mounted() {
        // this.queryRows(); // 加载时查询用例数据// 这里，请求套件用例可能会慢于watch监听代码被执行，导致数据和迭代套件对应不上的问题
    },

    updated() {
        this.setTableBodySize(); // 设置表格高度
        this.expandAll(); // 数据更新后展开折叠行
        if (this.currentModule == "bindPlanAndCaseDialog") {
            this.$nextTick(() => {
                this.checkCaseRow(this.guidsOfRelatedOldCases);
            });
        }
    },
};
</script>

<style lang="scss">
.sprint-testcase-table {
    .el-table__header-wrapper {
        th {
            padding-top: 3px !important;
            padding-bottom: 3px !important;
        }
    }

    // 设置用例名称靠左展示
    .el-table__placeholder {
        width: 0px;
    }

    .el-table__indent {
        padding-left: 0px !important;
    }

    .operation-col-cell-class .cell {
        padding-left: 5px !important;
        padding-right: 5px !important;
    }

    .operation-col-cell-class .cell .el-button--danger {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .operation-col-cell-class .cell .el-button {
        margin-left: 5px !important;
        margin-right: 1px;
    }

    .row-class-for-colspan {
        background: rgb(231, 229, 229);
        td {
            padding-top: 3px !important;
            padding-bottom: 3px !important;
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
        }
        .cell {
            padding-left: 2px;
            padding-right: 5px;
            height: auto !important;
        }
    }
}
</style>
