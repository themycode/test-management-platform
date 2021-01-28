<template>
    <!-- 用例详情组件 -->
    <div class="case-dialog-div">
        <el-dialog
            ref="caseDialog"
            :title="caseDialogTitle"
            :visible="caseDialogVisible"
            :fullscreen="fullscreen"
            :modal="false"
            :close-on-click-modal="true"
            :before-close="beforeClose"
            :destroy-on-close="true"
            custom-class="case-dialog-class"
            @close="onCloseDialog"
        >
            <div>
                <span
                    v-if="
                        currentModule == 'testPlanCaseTable' &&
                        operation != 'newCase'
                    "
                    >测试结果</span
                >
                <el-select
                    v-if="
                        currentModule == 'testPlanCaseTable' &&
                        operation != 'newCase'
                    "
                    v-model="row.result"
                    placeholder="请选择"
                    size="small"
                    style="width: 95px"
                    @change="onResultChanged(row)"
                    @visible-change="onVisibleChange($event, row.result)"
                >
                    <el-option
                        v-for="item in resultOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>

                <el-button size="small" @click="editCase" v-if="!caseEditing">
                    <i class="fa fa-edit" aria-hidden="true"></i>编辑
                </el-button>
                <el-button size="small" @click="cancelCaseEditing" v-else>
                    <i class="fa fa-edit" aria-hidden="true"></i>取消
                </el-button>
                <el-button
                    size="small"
                    @click="saveCase(false)"
                    v-if="caseEditing"
                >
                    <i class="fa fa-floppy-o" aria-hidden="true"></i>保存
                </el-button>
                <el-button
                    size="small"
                    @click="saveCase(true)"
                    v-if="caseEditing && operation != 'editCase'"
                >
                    <i class="fa fa-floppy-o" aria-hidden="true"></i
                    >保存并新增下一条
                </el-button>
                <el-button
                    size="small"
                    @click="copyCase"
                    v-if="!caseEditing && currentModule != 'testPlanCaseTable'"
                >
                    <i class="fa fa-copy" aria-hidden="true"></i>复制
                </el-button>
                <el-button
                    size="small"
                    @click="expandDialog"
                    v-if="!fullscreen"
                >
                    <i class="fa fa-expand" aria-hidden="true"></i>全屏
                </el-button>
                <el-button size="small" @click="compressDialog" v-else>
                    <i class="fa fa-compress" aria-hidden="true"></i>退出全屏
                </el-button>
                <div
                    v-if="operation != 'newCase'"
                    style="display: inline-block"
                >
                    <el-button size="small" @click="loadPrevCase"
                        >&lt;</el-button
                    >
                    <span style="padding: 0 5px"
                        >{{ this.caseOrder }}&nbsp;&nbsp;of&nbsp;&nbsp;{{
                            total
                        }}</span
                    >
                    <el-button size="small" @click="loadNextCase"
                        >&gt;</el-button
                    >
                </div>
                <span style="font-size: 9px">
                    备注：双击【{{ caseDialogTitle }}
                    】标题所在行可以快速展开/退出全屏
                </span>
            </div>
            <div class="case-detail-div">
                <div style="display: inline-block; margin-right: 10px">
                    <span>创建人：{{ caseInfo.createrName }}</span>
                </div>
                <div style="display: inline-block; margin-right: 10px">
                    <span>更新人：{{ caseInfo.updaterName }}</span>
                </div>

                <div style="display: inline-block; padding-right: 10px">
                    <span>优先级</span>：
                    <el-select
                        @change="onPriorityChanged"
                        @visible-change="
                            onPriorityVisibleChange($event, row.result)
                        "
                        ref="casePrioritySelect"
                        v-model="caseInfo.priority"
                        style="width: 70px"
                        size="mini"
                    >
                        <el-option
                            v-for="item in priorityOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </div>
                <div style="display: inline-block; padding-right: 10px">
                    <span>执行阶段/是否每个迭代都执行？：</span>
                    <span v-if="!caseEditing">{{ executionPhase }}</span>
                    <el-select
                        v-else
                        v-model="caseInfo.executionPhase"
                        style="width: 460px"
                        size="mini"
                        multiple
                    >
                        <el-option
                            v-for="item in executionPhaseOptions"
                            :key="item.value"
                            :label="
                                item.label +
                                '/' +
                                executedEachSprintMap[item.value][
                                    'executedEachSprint'
                                ]
                            "
                            :value="item.value"
                        >
                            <span style="float: left">{{ item.label }}</span>
                            <span
                                style="
                                    float: right;
                                    color: #8492a6;
                                    font-size: 13px;
                                    margin-right: 50px;
                                "
                            >
                                <span>每个迭代都执行？：</span>
                                <el-radio
                                    v-model="
                                        executedEachSprintMap[item.value][
                                            'executedEachSprint'
                                        ]
                                    "
                                    label="Y"
                                    @click.native="clickRadio(item, 'Y')"
                                    >是</el-radio
                                >
                                <el-radio
                                    v-model="
                                        executedEachSprintMap[item.value][
                                            'executedEachSprint'
                                        ]
                                    "
                                    label="N"
                                    @click.native="clickRadio(item, 'N')"
                                    >否</el-radio
                                >
                            </span>
                        </el-option>
                    </el-select>
                </div>
                <div style="display: inline-block; padding-right: 10px">
                    <span>执行方式：</span>
                    <span v-if="!caseEditing">
                        {{ executionMethodMap[caseInfo.executionMethod] }}
                    </span>
                    <el-select
                        v-else
                        v-model="caseInfo.executionMethod"
                        style="width: 100px"
                        size="mini"
                    >
                        <el-option
                            v-for="item in executionMethodOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </div>
                <div style="display: inline-block">
                    <span>测试集：{{ caseInfo.suitePath }}</span>
                </div>
            </div>
            <div class="case-detail-div">
                <!-- <span>用例编号：</span>
                <span v-if="!caseEditing" style="font-weight:bold;">{{ caseInfo.customNo }}</span>
                <el-input
                    v-else
                    placeholder="请输入用例编号"
                    v-model="caseInfo.customNo"
                    minlength="1"
                    maxlength="60"
                    size="small"
                    clearable
                ></el-input>-->
                <!-- <br /> -->

                <span>用例名称：</span>
                <span v-if="!caseEditing" style="font-weight: bold">
                    {{ caseInfo.name }}
                </span>

                <el-input
                    v-else
                    placeholder="请输入用例名称"
                    v-model="caseInfo.name"
                    minlength="1"
                    maxlength="60"
                    size="small"
                    clearable
                ></el-input>
            </div>
            <div class="case-detail-div">
                <span>用例备注：</span>
                <!-- <span v-if="!caseEditing" style="padding-right:20px">{{ caseInfo.desc }}</span> -->
                <pre
                    v-if="!caseEditing"
                    style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    "
                    >{{ caseInfo.desc }}</pre
                >
                <el-input
                    v-else
                    type="textarea"
                    :autosize="{ minRows: 2 }"
                    ref="descInput"
                    placeholder="请输入用例备注"
                    v-model="caseInfo.desc"
                    maxlength="1000"
                    show-word-limit
                ></el-input>
            </div>
            <div class="case-detail-div">
                <span>前置条件：</span>
                <pre
                    v-if="!caseEditing"
                    style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    "
                    >{{ caseInfo.precondition }}</pre
                >
                <!-- <span v-if="!caseEditing">{{ caseInfo.precondition }}</span> -->
                <el-input
                    v-else
                    ref="preconditionInput"
                    type="textarea"
                    :autosize="{ minRows: 2 }"
                    placeholder="请输入前置条件"
                    v-model="caseInfo.precondition"
                    maxlength="1000"
                    show-word-limit
                ></el-input>
            </div>

            <div class="case-detail-div">
                测试步骤：
                <!-- 操作按钮 -->
                <el-row>
                    <el-button-group>
                        <el-button size="mini" @click="addCaseStep"
                            >新增</el-button
                        >
                        <el-button size="mini" @click="deleteCaseStepsInBatch"
                            >删除</el-button
                        >
                        <el-button
                            v-if="caseStepsEditing && caseEditing"
                            el-button
                            size="mini"
                            @click="finishCaseStepsEditing"
                            >完成</el-button
                        >
                        <el-button
                            v-else-if="caseStepsEditing && !caseEditing"
                            el-button
                            size="mini"
                            @click="finishCaseStepsEditing"
                            >保存</el-button
                        >
                        <el-button
                            v-else
                            el-button
                            size="mini"
                            @click="editCaseSteps"
                            >编辑</el-button
                        >
                    </el-button-group>
                    <span
                        >说明：双击步骤行可进入编辑状态；非编辑用例状态下，新增/删除/编辑操作后需要点击"保存"才会生效</span
                    >
                </el-row>

                <!-- 表格 -->
                <el-table
                    :data="caseInfo.steps"
                    style="width: 100%; margin-bottom: 0px; overflow: auto"
                    border
                    @row-dblclick="dblclickStepRow"
                    @selection-change="onSelectChange"
                >
                    <!--多选复选框-->
                    <el-table-column
                        type="selection"
                        width="35px"
                        align="center"
                        :resizable="false"
                    ></el-table-column>
                    <!-- 展示索引列 -->
                    <el-table-column
                        type="index"
                        align="center"
                        :resizable="false"
                        label="步序"
                        width="50px"
                    ></el-table-column>
                    <!-- <el-table-column
                        prop="id"
                        label="ID"
                        width="65px"
                        header-align="center"
                        align="center"
                        :resizable="false"
                    ></el-table-column>-->

                    <el-table-column
                        prop="action"
                        label="步骤动作"
                        min-width="250px"
                        show-overflow-tooltip
                        header-align="center"
                        align="left"
                    >
                        <template slot-scope="scope">
                            <span v-if="caseStepsEditing && scope.row.editing">
                                <el-input
                                    type="textarea"
                                    size="small"
                                    :autosize="{ minRows: 2 }"
                                    placeholder="请输入步骤动作"
                                    v-model="scope.row.action"
                                ></el-input>
                            </span>
                            <pre
                                v-else
                                style="
                                    margin-top: 0px;
                                    margin-bottom: 0px;
                                    white-space: pre-wrap;
                                    word-wrap: break-word;
                                "
                                >{{ scope.row.action }}</pre
                            >
                        </template>
                    </el-table-column>
                    <el-table-column
                        prop="expection"
                        label="预期结果"
                        min-width="250px"
                        show-overflow-tooltip
                        header-align="center"
                        align="left"
                    >
                        <template slot-scope="scope">
                            <span v-if="caseStepsEditing && scope.row.editing">
                                <el-input
                                    type="textarea"
                                    size="small"
                                    :autosize="{ minRows: 2 }"
                                    placeholder="请输入步骤预期结果"
                                    v-model="scope.row.expection"
                                ></el-input>
                            </span>
                            <span
                                v-else
                                style="
                                    margin-top: 0px;
                                    margin-bottom: 0px;
                                    white-space: pre-wrap;
                                    word-wrap: break-word;
                                "
                                >{{ scope.row.expection }}</span
                            >
                        </template>
                    </el-table-column>

                    <el-table-column
                        label="操作"
                        align="center"
                        width="190px"
                        :resizable="false"
                    >
                        <template slot-scope="scope">
                            <el-button
                                class="operationBtn"
                                size="mini"
                                @click="
                                    insertCaseStep(scope.$index - 1, scope.row)
                                "
                                >上方插入行</el-button
                            >
                            <el-button
                                class="operationBtn"
                                size="mini"
                                @click="insertCaseStep(scope.$index, scope.row)"
                                >下方插入行</el-button
                            >
                            <el-button
                                class="operationBtn"
                                size="mini"
                                type="danger"
                                @click="
                                    deleteOneCaseStep(scope.$index, scope.row)
                                "
                                >删除</el-button
                            >
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="case-detail-div">
                <span>后置条件：</span>
                <pre
                    v-if="!caseEditing"
                    style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    "
                    >{{ caseInfo.postcondition }}</pre
                >

                <el-input
                    v-else
                    style="white-space: pre-wrap; word-wrap: break-word"
                    ref="postconditionInput"
                    type="textarea"
                    :autosize="{ minRows: 2 }"
                    placeholder="请输入后置条件"
                    v-model="caseInfo.postcondition"
                    maxlength="1000"
                    show-word-limit
                ></el-input>
            </div>

            <div class="case-detail-div">
                <span style="margin-right: 10px">用例标签：</span>
                <el-tag
                    :key="tag"
                    v-for="tag in this.caseInfo.tags"
                    :closable="caseEditing"
                    :disable-transitions="true"
                    @close="onCloseTag(tag)"
                    >{{ tag }}</el-tag
                >
                <el-input
                    class="input-new-tag"
                    v-if="tagInputVisible"
                    v-model="tagInputValue"
                    ref="saveTagInput"
                    size="small"
                    @keyup.enter.native="handleTagInputConfirm"
                    @blur="handleTagInputConfirm"
                ></el-input>

                <el-button
                    v-else-if="caseEditing"
                    class="button-new-tag"
                    size="small"
                    @click="showTagInput"
                    >+点击新增标签</el-button
                >
            </div>

            <div class="case-detail-div" v-if="!caseEditing">
                <el-upload
                    class="upload-demo"
                    action="fakeaction"
                    ref="attatchmentUploader"
                    :file-list="caseAttachmentList"
                    :http-request="uploadAttatchment"
                    :before-remove="onBeforeRemoveCaseAttachment"
                    :on-preview="onPreviewCaseAttachment"
                    :with-credentials="true"
                >
                    <el-button size="small" type="primary">上传附件</el-button>
                    <!-- <div slot="tip" class="el-upload__tip">只能上传xxxx文件，且不超过xxxkb</div> -->
                </el-upload>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
    props: [
        "caseDialogLoaded",
        "caseDialogEditing",
        "caseDialogTitle",
        "caseDialogVisible",
        "caseData",
        "row",
        "tableData",
        "caseListData",
        "currentPage",
        "pageSize",
        "total",
        "operation",
        "caseOrder",
        "currentModule",
        "resultOptions",
        "planRow",
        "priorityOptions",
        "executionPhaseOptions",
        "executedEachSprintDict",
    ],
    data() {
        return {
            fullscreen: false, // 是否全屏
            caseInfo: this.caseData,
            caseEditing: this.caseDialogEditing, // 标识是否在编辑测试用例
            caseStepsEditing: false, // 标识是否在编辑测试用例步骤
            caseStepRowSelected: [], // 存放用户勾选的记录行数据
            tagInputVisible: false, // 控制测试用例标签输入对话框是否可见 false 不可见 true 可见
            tagInputValue: "", // 测试用例标签输入框的值
            caseAttachmentList: [], // 存放测试用例附件
            caseTestResult: "", // 用于临时存放用例测试结果更新前的结果值
            casePriority: "", // 用于临时存放用例优先级更新前的结果值
            executionMethodOptions: [
                { label: "手工", value: "handwork" },
                { label: "自动化", value: "automation" },
            ],
            executionMethodMap: { handwork: "手工", automation: "自动化" },
            executedEachSprintMap: {}, // 测试用例执行阶段和是否每次迭代都执行字典映射
        };
    },
    methods: {
        clickRadio(item, value) {
            this.executedEachSprintMap[item.value][
                "executedEachSprint"
            ] = value;
        },
        // 关闭测试用例对话框
        onCloseDialog() {
            this.$emit("update:caseDialogVisible", false); // 隐藏对话框
        },
        // 关闭测试用例对话框前
        beforeClose(closeDialog) {
            if (this.caseEditing || this.caseStepsEditing) {
                this.$confirm("确定要关闭吗？", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                    cancelButtonClass: "btn-custom-cancel",
                })
                    .then(() => {
                        closeDialog(true); // 关闭对话框

                        // 如果不添加以下代码，如果打开的对话框，已经进入编辑用例步骤的状态，强制关闭对话框，再次点击列表相同用例，打开对话框，双击用例步骤，无法进入编辑状态
                        // 退出编辑用例步骤状态
                        if (this.caseStepsEditing) {
                            this.caseStepsEditing = false;
                            //让全部步骤退出编辑状态
                            for (
                                let i = 0;
                                i < this.caseInfo.steps.length;
                                i++
                            ) {
                                this.caseInfo.steps[i].editing = false;
                            }
                        }
                    })
                    .catch(() => {});
            } else {
                // 非编辑状态，直接退出
                closeDialog(true); // 关闭对话框
            }
            this.$emit("update:caseDialogEditing", false);
        },
        // 调整对话框位置
        changeDialogPos() {
            this.$nextTick(() => {
                let dialog = this.$refs.caseDialog.$el.querySelector(
                    ".case-dialog-class"
                );

                if (dialog.style.left == "") {
                    dialog.style.left = "0px";
                    dialog.style.width = "100%";
                    dialog.style.right = "0px";
                } else {
                    if (dialog.style.left == "0px") {
                        dialog.style.width = "50%";
                        dialog.style.left = "50%";
                        dialog.style.right = "0px";
                    } else {
                        dialog.style.left = "0px";
                        dialog.style.width = "100%";
                        dialog.style.right = "0px";
                    }
                }
            });
        },
        // 全屏
        expandDialog() {
            this.fullscreen = true;
            this.changeDialogPos();
        },
        // 退出全屏
        compressDialog() {
            this.fullscreen = false;
            this.changeDialogPos();
        },

        // 编辑用例
        editCase() {
            this.$emit("update:operation", "editCase");
            this.$emit("update:caseDialogTitle", "编辑用例");

            if (!this.caseEditing) {
                this.caseEditing = true;
                this.$emit("update:caseDialogEditing", true);
            }
        },
        // 复制用例
        copyCase() {
            this.caseInfo["name"] = this.caseInfo["name"] + "-副本";
            this.$emit("update:operation", "copyCase");
            this.$emit("update:caseDialogTitle", "复制用例");

            if (!this.caseEditing) {
                this.caseEditing = true;
                this.$emit("update:caseDialogEditing", true);
            }
        },
        // 取消编辑用例
        cancelCaseEditing() {
            if (this.operation == "newCase" || this.operation == "copyCase") {
                this.$confirm(
                    "当前内容没保存，取消会自动关闭对话框，确定取消吗?",
                    "提示",
                    {
                        confirmButtonText: "确定",
                        cancelButtonText: "取消",
                        type: "warning",
                        cancelButtonClass: "btn-custom-cancel",
                    }
                )
                    .then(() => {
                        this.$emit("update:caseDialogVisible", false); //语句的执行不会触发close关闭对话框事件，即不会触发调用onCloseDialog，仅是隐藏对话框
                        this.$emit("update:caseDialogTitle", "查看用例");
                        this.$emit("update:operation", "viewCase");
                        this.$emit("update:caseDialogEditing", false);
                        this.$emit("update:caseDialogLoaded", false); // 防止本次给对话框设置的属性数据干扰下次的操作，保守起见，“卸载”对话框
                    })
                    .catch(() => {});
            } else {
                // 设置对话框全局编辑状态为非编辑状态
                this.caseEditing = false;
                this.caseStepsEditing = false;
                //让全部步骤退出编辑状态
                for (let i = 0; i < this.caseInfo.steps.length; i++) {
                    this.caseInfo.steps[i].editing = false;
                }
                this.$emit("update:caseDialogEditing", false);
                this.$emit("update:caseDialogTitle", "查看用例");
                this.$emit("update:operation", "viewCase");
            }
        },
        // 用例基础信息校验
        caseInfoCheck() {
            if (!this.caseInfo.name) {
                this.$message.error("用例名称不能为空");
                return false;
            }

            if (!this.caseInfo.executionPhase) {
                this.$message.error("用例执行阶段不能为空");
                return false;
            }

            // 如果存在正在编辑的步骤，先让步骤退出编辑状态
            if (this.caseStepsEditing) {
                // 退出编辑状态
                this.caseStepsEditing = false;

                //让全部步骤退出编辑状态
                for (let i = 0; i < this.caseInfo.steps.length; i++) {
                    this.caseInfo.steps[i].editing = false;
                }
                this.$emit("update:caseDialogEditing", false);
            }

            return true;
        },
        // 保存用例
        saveCase(ifNewNextCase) {
            try {
                if (!this.caseInfoCheck()) {
                    return;
                }
                let caseInfo = Object.assign({}, this.caseInfo);
                caseInfo["tags"] = caseInfo["tags"].join(",");
                let tempStr = "";
                for (let i = 0; i < caseInfo["executionPhase"].length; i++) {
                    let executionPhase = caseInfo["executionPhase"][i];
                    // this.executedEachSprintMap 一定存在key为executionPhase的值，所以不做判断
                    if (executionPhase in this.executedEachSprintMap) {
                        tempStr +=
                            executionPhase +
                            "/" +
                            this.executedEachSprintMap[executionPhase][
                                "executedEachSprint"
                            ] +
                            ",";
                    }
                }
                caseInfo["executedEachSprint"] = tempStr.substring(
                    0,
                    tempStr.length - 1
                );
                caseInfo["executionPhase"] = caseInfo["executionPhase"].join(
                    ","
                );

                caseInfo["steps"] = JSON.stringify(caseInfo["steps"]);

                if (
                    this.operation == "newCase" || // 新建用例
                    this.operation == "copyCase" // 复制用例
                ) {
                    if (caseInfo["suiteType"] == "base") {
                        caseInfo["sprintId"] = -1; // 新增基线用例，sprintId保持为-1
                    }
                    // 发送新增用例请求
                    this.$api.sprintCaseDialog
                        .addTestCase(caseInfo)
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);
                                if (!ifNewNextCase) {
                                    this.$emit(
                                        "update:caseDialogVisible",
                                        false
                                    ); // 先隐藏对话框

                                    // 卸载对话框
                                    this.$emit(
                                        "update:caseDialogLoaded",
                                        false
                                    );

                                    this.$emit(
                                        "update:caseDialogTitle",
                                        "查看用例"
                                    );
                                    this.$emit("update:operation", "viewCase");
                                    this.$emit(
                                        "update:caseDialogEditing",
                                        false
                                    );
                                } else {
                                    let executionPhase = [];
                                    for (let item in this
                                        .executedEachSprintDict) {
                                        if (
                                            this.executedEachSprintDict[item]
                                                .default
                                        ) {
                                            executionPhase = [item];
                                            break;
                                        }
                                    }
                                    this.caseInfo = {
                                        testplanId:this.caseInfo.testplanId,
                                        suiteId: this.caseInfo.suiteId,
                                        productId: this.caseInfo.productId,
                                        sprintId: this.caseInfo.sprintId,
                                        suiteType: this.caseInfo.suiteType,
                                        customNo: "",
                                        name: "",
                                        createrName: "",
                                        updaterName: "",
                                        priority: "P3",
                                        executedEachSprint: "",
                                        executionMethod: "handwork",
                                        executionPhase: executionPhase,
                                        suitePath: this.caseInfo.suitePath,
                                        precondition: "",
                                        steps: [],
                                        postcondition: "",
                                        tags: [],
                                        desc: "",
                                        result:"未执行",
                                        remark: ""
                                    };
                                }

                                
                                let suiteFound = false; // 标记是否找到用例所在的套件
                                for (
                                    let i = 0;
                                    i < this.tableData.length; 
                                    i++
                                ) {
                                    let caseSuite = this.tableData[i];
                                    if (caseSuite.suiteId == res.data.case.suiteId) {
                                        caseSuite.children.splice(
                                            0,
                                            0,
                                            res.data.case
                                        );
                                        suiteFound = true;
                                        break;
                                    }
                                }
                                if (!suiteFound) {
                                    console.log(
                                        "当前数据表中未找到对应的测试套件"
                                    ); // 给所在套件新增第一条测试用例的情况下，会出现找不到套件的情况
                                    this.$emit("update:currentPage", 1); // 切换到第一页，
                                    // 结束编辑用例
                                    this.$emit(
                                        "update:caseDialogEditing",
                                        false
                                    );
                                    this.$parent.queryRows();
                                } else {
                                    let lastSuite = this.tableData[
                                        this.tableData.length - 1
                                    ];

                                    if (this.total + 1 > this.pageSize) {
                                        // 如果当前记录数超过页面容量，删除最后一条用例
                                        lastSuite.children.splice(
                                            lastSuite.children.length - 1,
                                            1
                                        );

                                        if (!lastSuite.children.length) {
                                            // 所在测试集下没有其它测试用例，一并删除测试集
                                            this.tableData.splice(
                                                this.tableData.length - 1,
                                                1
                                            );
                                        }
                                    }

                                    this.$emit("update:total", this.total + 1); // 增加总记录数

                                    let tableData = Object.assign(
                                        [],
                                        this.tableData
                                    );

                                    this.$emit("update:tableData", tableData);
                                }

                                // 更新测试计划详情及测试计划表中对应测试计划信息
                                for (let key in res.data.planCaseStatistics) {
                                    if (key in this.planRow) {
                                        // 以防后续表单字段有变更，仅保存对应key的值
                                        this.planRow[key] = res.data.planCaseStatistics[key];
                                    }
                                }

                                // 自动勾选父级页面计划关联的用例
                                if (
                                    this.currentModule ==
                                    "bindPlanAndCaseDialog"
                                ) {
                                    this.$parent.checkCaseRow(
                                        this.$parent.guidsOfRelatedOldCases
                                    );
                                }
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                        });
                } else if (this.operation == "editCase") {
                    // 如果为编辑用例 // 发送更新用例请求
                    delete caseInfo["suitePath"];
                    delete caseInfo["sprintId"];
                    this.$api.sprintCaseDialog
                        .updateTestCase(caseInfo)
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);

                                // 设置对话框整体编辑状态为false
                                this.caseEditing = false;
                                this.$emit("update:caseDialogEditing", false);

                                this.$emit(
                                    "update:caseDialogTitle",
                                    "编辑用例"
                                );

                                // 更新列表数据
                                for (let key in res.data) {
                                    if (key in this.row) {
                                        // 以防后续表单字段有变更，仅保存对应key的值
                                        this.row[key] = res.data[key];
                                    }
                                }

                                // 更新对话框面板数据
                                this.caseInfo["updaterName"] =
                                    res.data["updaterName"];
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                            this.$parent.queryRows();
                        });
                }
            } catch (err) {
                this.$message.error(err.message);
            }
        },
        loadCaseData(targetOrder) {
            this.caseStepsEditing = false;
            this.$emit("update:caseOrder", targetOrder);

            let counter = 0; // 计数器
            for (let i = 0; i < this.tableData.length; i++) {
                let testSuite = this.tableData[i];

                if (testSuite.children.length) {
                    for (let i = 0; i < testSuite.children.length; i++) {
                        counter += 1;
                        const cnt =
                            (this.currentPage - 1) * this.pageSize + counter;
                        if (cnt == targetOrder) {
                            let testCase = testSuite.children[i];

                            this.$emit("update:row", testCase);

                            // 此处for循环会导致key丢失
                            // for (let key in this.caseInfo) {
                            //     this.caseInfo[key] = testCase[key];
                            // }

                            // this.caseInfo = testCase; // 这样会导致列表数据和对话框的数据联动

                            this.caseInfo = {
                                testplanId: testCase.testplanId,
                                suiteId: testCase.suiteId,
                                productId: testCase.productId,
                                sprintId: testCase.sprintId,
                                suiteType: testCase.suiteType, // 测试集类型，如果时测试计划，则固定为testplan
                                detailSuiteType: testCase.detailSuiteType, // 测试集细分类型，针对测试计划，细分base，sprint
                                caseId: testCase.id, // 测试用例ID
                                guid: testCase.guid,
                                customNo: testCase.customNo, // 定义用例编号
                                name: testCase.name, // 用例名称
                                createrName: testCase.createrName,
                                updaterName: testCase.updaterName, // 更新人
                                priority: testCase.priority, // 优先级
                                executedEachSprint: testCase.executedEachSprint,
                                executionMethod: testCase.executionMethod,
                                executionPhase: testCase.executionPhase,
                                suitePath: testCase.suitePath, // 测试集路径
                                precondition: testCase.precondition, // 前置条件
                                steps: JSON.parse(testCase.steps),
                                postcondition: testCase.postcondition, //后置条件
                                desc: testCase.desc, // 用例描述
                                tags: testCase.tags, // 存放测试用例标签
                            };

                            this.initExecutedEachSprintMap();

                            // 获取测试用例附件列表
                            this.queryCaseAttachments();
                            return;
                        }
                    }
                }
            }
        },
        // 加载用例数据显示到对话框
        // targetOrder 目标用例行所在的次序
        loadCase(targetOrder) {
            let loadCaseFunc = (targetOrder) => {
                // 判断要加载的记录位于第几页
                const targetPage = Math.ceil(targetOrder / this.pageSize);
                if (targetPage != this.currentPage) {
                    // 翻页到前一页
                    this.$emit("update:currentPage", targetPage);
                    new Promise((resolve, reject) => {
                        this.$parent.queryRows(null, resolve, reject);
                    }).then((result) => {
                        if (result) {
                            this.loadCaseData(targetOrder);
                        } else {
                            this.$message.error("加载用例失败");
                        }
                    });
                    return;
                }

                this.loadCaseData(targetOrder);
            };

            if (this.caseEditing || this.caseStepsEditing) {
                this.$confirm("您有正在编辑的用例，确定继续操作吗?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                    cancelButtonClass: "btn-custom-cancel",
                })
                    .then(() => {
                        loadCaseFunc(targetOrder);
                    })
                    .catch(() => {});
            } else {
                loadCaseFunc(targetOrder);
            }
        },

        // 加载上一条数据
        loadPrevCase() {
            if (this.caseOrder > 1) {
                this.loadCase(this.caseOrder - 1);
            }
        },

        // 加载下一条用例数据
        loadNextCase() {
            if (this.caseOrder < this.total) {
                this.loadCase(this.caseOrder + 1);
            }
        },

        // 新增测试用例步骤公用方法
        // caseStep 测试用例步骤对象
        // index 测试用例步骤插入的位置
        addStep(index, caseStep) {
            this.caseStepsEditing = true;
            this.$emit("update:caseDialogEditing", true);
            this.caseInfo.steps.splice(index, 0, caseStep);
        },
        // 新增测试用例步骤
        addCaseStep() {
            let caseStep = {
                action: "",
                expection: "",
                editing: true,
            };
            this.addStep(this.caseInfo.steps.length, caseStep);
        },
        // 插入测试用例步骤
        insertCaseStep(index, row) {
            let caseStep = {
                action: "",
                expection: "",
                editing: true,
            };
            this.addStep(index + 1, caseStep);
        },
        // 双击测试用例步骤行
        dblclickStepRow(row, column, event) {
            this.editCaseStep(null, row);
        },
        // 逐条编辑
        editCaseStep(index, row) {
            if (!row.editing) {
                row.editing = true;
                this.caseStepsEditing = true;
                this.$emit("update:caseDialogEditing", true);
            }
        },
        // 批量编辑
        editCaseSteps() {
            this.caseStepsEditing = true;
            this.$emit("update:caseDialogEditing", true);
            if (this.caseStepRowSelected.length) {
                // 由选中则让选中步骤进入编辑状态
                for (let i = 0; i < this.caseStepRowSelected.length; i++) {
                    this.caseStepRowSelected[i].editing = true;
                }
            } else {
                // 否则，让全部步骤进入编辑状态
                for (let i = 0; i < this.caseInfo.steps.length; i++) {
                    this.caseInfo.steps[i].editing = true;
                }
            }
        },
        // 点击测试步骤"完成"事件处理函数
        finishCaseStepsEditing() {
            // 退出编辑状态
            this.caseStepsEditing = false;

            //让全部步骤退出编辑状态
            for (let i = 0; i < this.caseInfo.steps.length; i++) {
                this.caseInfo.steps[i].editing = false;
            }

            this.$emit("update:caseDialogEditing", false);

            if (this.caseEditing) {
                return;
            }

            this.updateCaseSteps();
        },
        // 更新用例步骤
        updateCaseSteps() {
            let caseData = {};
            caseData["testplanId"] = this.row.testplanId;
            caseData["caseId"] = this.caseInfo.caseId;
            caseData["guid"] = this.caseInfo.guid;
            caseData["steps"] = JSON.stringify(this.caseInfo.steps);
            caseData["suiteId"] = this.caseInfo.suiteId;
            caseData["suiteType"] = this.caseInfo.suiteType;
            caseData["detailSuiteType"] = this.caseInfo.detailSuiteType;

            // 发送更新用例请求
            this.$api.sprintCaseDialog
                .updateTestCase(caseData)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);

                        // 更新列表数据
                        for (let key in res.data) {
                            if (key in this.row) {
                                this.row[key] = res.data[key];
                            }
                        }

                        // 更新对话框面板数据
                        this.caseInfo["updaterName"] = res.data["updaterName"];
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 逐条删除用例步骤
        deleteOneCaseStep(index, row) {
            this.caseStepsEditing = true;
            this.$emit("update:caseDialogEditing", true);

            this.caseInfo.steps.splice(index, 1);
        },
        // 勾选记录行发生改变时事件处理函数
        onSelectChange(selection) {
            this.caseStepRowSelected = selection;
        },
        // 批量删除用例步骤
        deleteCaseStepsInBatch() {
            this.caseStepsEditing = true;
            this.$emit("update:caseDialogEditing", true);

            if (!this.caseStepRowSelected.length) {
                this.$alert("未选择步骤，请勾选至少一条步骤", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            for (let i = 0; i < this.caseStepRowSelected.length; i++) {
                for (let x = 0; x < this.caseInfo.steps.length; x++) {
                    if (this.caseInfo.steps[x] == this.caseStepRowSelected[i]) {
                        this.caseInfo.steps.splice(x, 1);
                    }
                }
            }
        },
        // 删除tag
        onCloseTag(tag) {
            this.caseInfo.tags.splice(this.caseInfo.tags.indexOf(tag), 1);
        },
        // 点击按钮时加载tag输入框
        showTagInput() {
            this.tagInputVisible = true;
            this.$nextTick((_) => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },
        // tag输入框失去焦点、或者未失去焦点的情况下，回车键事件处理函数
        handleTagInputConfirm() {
            let tagInputValue = this.tagInputValue;
            // 输入标签不为空，且不存在当前tags中才可以添加
            if (
                tagInputValue &&
                this.caseInfo.tags.indexOf(tagInputValue) == -1
            ) {
                this.caseInfo.tags.push(tagInputValue);
            }
            this.tagInputVisible = false;
            this.tagInputValue = "";
        },
        // 关联测试用例附件
        queryCaseAttachments() {
            this.$api.sprintCaseDialog
                .getCaseAttachments({
                    caseId: this.caseInfo.caseId,
                    caseGuid: this.caseInfo.guid,
                    caseType: this.caseInfo.suiteType,
                    testplanId: this.caseInfo.testplanId,
                })
                .then((res) => {
                    if (res.success) {
                        this.caseAttachmentList = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 移除上传文件列表中的附件
        removeUploadAttatchment(fileUid) {
            let uploadFiles = this.$refs.attatchmentUploader.uploadFiles;
            for (let i = 0; i < uploadFiles.length; i++) {
                if (fileUid == uploadFiles[i].uid) {
                    uploadFiles.splice(i, 1);
                    break;
                }
            }
        },
        // 上传用例附件
        uploadAttatchment(params) {
            const file = params.file;
            // 上传数量限制
            if (
                this.caseAttachmentList.length >
                this.$appConfig.caseAttachmentNumLimit
            ) {
                this.$message.error(
                    "上传附件失败，最多只能上传" +
                        this.$appConfig.caseAttachmentNumLimit +
                        "个附件"
                );
                this.removeUploadAttatchment(file.uid);
                return;
            }

            if (!file.size) {
                // file.size默认字节为单位
                this.$message.error("上传失败，附件内容不能为空");
                this.removeUploadAttatchment(file.uid);
                return;
            } else {
                let ifExceedLimit = file.size / 1024 / 1024 > 10;
                if (ifExceedLimit) {
                    this.$message.error(
                        "上传附件失败，文件大小不能超过" +
                            this.$appConfig.caseAttachmentSizeLimit +
                            "M"
                    );
                    this.removeUploadAttatchment(file.uid);
                    return;
                }
            }

            // if (file.type.indexOf("vnd.ms-excel") == -1) {
            //     this.$message.error(
            //         "上传附件失败，只能上传excel文件"
            //     );
            //     this.removeUploadAttatchment(file.uid);
            //     return;
            // }

            let form = new FormData();
            form.append("file", file);
            form.append("caseGuid", this.row.guid);
            form.append("caseId", this.row.id);
            form.append("caseType", this.row.suiteType);
            form.append("detailCaseType", this.row.detailSuiteType);
            form.append("priority", this.row.priority);
            form.append("testplanId", this.row.testplanId);
            this.$api.sprintCaseDialog
                .uploadAttatchment(form)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.caseAttachmentList.push(res.data);
                    } else {
                        this.removeUploadAttatchment(file.uid);
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                    this.removeUploadAttatchment(file.uid);
                });
        },
        // 移除附件时事件处理函数
        onBeforeRemoveCaseAttachment(file, fileList) {
            this.$confirm("确定要删除该附件吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    // 发送删除请求
                    this.$api.sprintCaseDialog
                        .deleteAttatchment({
                            attachmentId: file.id,
                            guid: file.guid,
                            caseGuid: this.row.guid,
                            caseId: this.row.id,
                            caseType: this.row.suiteType,
                            priority: this.row.priority,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);
                                this.caseAttachmentList.splice(
                                    this.caseAttachmentList.indexOf(file),
                                    1
                                );

                                return true;
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                            return false;
                        });
                })
                .catch(() => {
                    return false;
                });
            return false;
        },
        // 预览附件\下载附件
        onPreviewCaseAttachment(file) {
            let fileSuffixArr = [
                ".png",
                ".jpeg",
                ".jpg",
                ".bmp",
                ".gif",
                ".txt",
                ".sql",
                ".pdf",
                ".html",
                ".htm",
                ".xml",
                ".json",
            ];
            let tempIndex = file.filePath.lastIndexOf(".");
            let fileSuffix = "";
            if (tempIndex > -1) {
                fileSuffix = file.filePath.substring(tempIndex);
            }

            if (fileSuffix && fileSuffixArr.indexOf(fileSuffix) > -1) {
                // 如果支持浏览器预览，则预览文件，否则下载文件
                let link = document.createElement("a");
                link.style.display = "none";
                link.href = this.$apiBaseURL + "/media" + file.filePath;
                link.setAttribute("target", "_blank");

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                return;
            }

            // 注释以下代码，主要是因为点击链接，弹出保存框，文件名称无法设置为file.name的问题，采用api请求，从后台返回数据
            // let link = document.createElement("a");
            // link.style.display = "none";
            // link.href = this.$apiBaseURL + "/media" + file.filePath;
            // link.setAttribute("download", decodeURI(file.name));

            // document.body.appendChild(link);
            // link.click();
            // document.body.removeChild(link);

            // 下载附件
            this.$api.sprintCaseDialog
                .downloadAttatchment({
                    attachmentId: file.id,
                    caseId: this.row.id,
                })
                .then((res) => {
                    let link = document.createElement("a");
                    let blob = new Blob([res.data], {
                        type: res.headers["content-type"],
                    });

                    link.style.display = "none";
                    link.href = window.URL.createObjectURL(blob);
                    link.setAttribute("download", file.name);

                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
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
                                        res.message + ":" + responseData.detail
                                );
                            }
                        };
                        reader.readAsText(res.response.data);
                    } else {
                        this.$message.error(res.msg || res.message);
                    }
                });
        },
        // 通过点击测试结果下拉选框，手动修改测试结果时的事件触发函数
        onVisibleChange(event, result) {
            if (event) {
                // 只记录更改前的值
                this.caseTestResult = result;
            }
        },
        onResultChanged(row) {
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
                    } else {
                        // 还原数据
                        row["result"] = this.caseTestResult;
                        this.$message.error(res.msg);
                    }

                    // 更新测试计划详情及测试计划表中对应测试计划信息
                    for (let key in res.data.planDataUpdated) {
                        if (key in this.planRow) {
                            // 以防后续表单字段有变更，仅保存对应key的值
                            this.planRow[key] = res.data.planDataUpdated[key];
                        }
                    }
                })
                .catch((res) => {
                    row["result"] = this.caseTestResult;
                    this.$message.error(res.msg);
                });
        },
        onPriorityVisibleChange(event, priority) {
            if (event) {
                // 只记录更改前的值
                this.casePriority = priority;
            }
        },
        // 更新优先级
        onPriorityChanged(priority) {
            if (this.caseEditing) {
                return;
            }

            let caseData = {};
            caseData["testplanId"] = this.row.testplanId;
            caseData["caseId"] = this.caseInfo.caseId;
            caseData["guid"] = this.caseInfo.guid;
            caseData["priority"] = priority;
            caseData["suiteId"] = this.caseInfo.suiteId;
            caseData["suiteType"] = this.caseInfo.suiteType;

            // 发送更新用例请求
            this.$api.sprintCaseDialog
                .updateTestCase(caseData)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        // 更新列表数据
                        for (let key in res.data) {
                            if (key in this.row) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                this.row[key] = res.data[key];
                            }
                        }

                        // 更新对话框面板数据
                        this.caseInfo["updaterName"] = res.data["updaterName"];
                    } else {
                        this.$message.error(res.msg);
                        this.caseInfo.priority = this.casePriority;
                        this.row["priority"] = this.casePriority;
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg);
                    this.caseInfo.priority = this.casePriority;
                    this.row["priority"] = this.casePriority;
                });
        },

        initExecutedEachSprintMap() {
            // 重新初始化 executedEachSprintMap
            this.executedEachSprintMap = JSON.parse(
                JSON.stringify(this.executedEachSprintDict)
            );

            // 根据用例原有配置，重新初始化用例“是否每个迭代都执行”配置
            let tempArray = this.caseInfo.executedEachSprint.split(",");
            for (let i = 0; i < tempArray.length; i++) {
                let item = tempArray[i];
                item = item.replace(" ", "");
                item = item.split("/"); // 形如 ["SystemTesting", "Y"]
                if (item[0] in this.executedEachSprintDict) {
                    this.executedEachSprintMap[item[0]]["executedEachSprint"] =
                        item[1];
                }
            }
        },
    },
    watch: {
        caseData: function (newValue, oldValue) {
            this.caseInfo = this.caseData;
            if (this.operation == "viewCase") {
                this.caseEditing = false;
                this.$emit("update:caseDialogEditing", false);
                // 仅查看用例时才加载附件
                this.queryCaseAttachments();
            } else {
                this.caseEditing = true;
                this.$emit("update:caseDialogEditing", true);
            }

            this.initExecutedEachSprintMap();
        },
    },
    computed: {
        executionPhase: {
            get() {
                let tempStr = "";
                for (let i = 0; i < this.caseInfo.executionPhase.length; i++) {
                    let optionValue = this.caseInfo.executionPhase[i];
                    let optionLabel = this.executedEachSprintMap[optionValue][
                        "executionPhase"
                    ];
                    let executedEachSprint = this.executedEachSprintMap[
                        optionValue
                    ]["executedEachSprint"];

                    if (executedEachSprint == "N") {
                        executedEachSprint = "否";
                    } else {
                        executedEachSprint = "是";
                    }

                    tempStr += optionLabel + "/" + executedEachSprint + "; ";
                }
                tempStr = tempStr.substring(0, tempStr.length - 1);
                return tempStr;
            },
        },
    },
    created() {
        if (this.operation == "viewCase") {
            // 获取测试用例附件
            this.queryCaseAttachments();
        }
        this.initExecutedEachSprintMap();
    },
    mounted() {
        // 双击dialog header，全屏或者退出全屏
        let dialogHeader = this.$refs.caseDialog.$el.querySelector(
            ".el-dialog__header"
        );

        dialogHeader.addEventListener("dblclick", () => {
            this.changeDialogPos();
        });

        // this.$refs.caseDialog.$el
        //     .querySelector(".el-dialog__header")
        //     .addEventListener("dblclick", () => {
        //         this.fullscreen = !this.fullscreen;
        //     });
    },
};
</script>

<style lang="scss">
// 修改dialog body样式//该样式不能放置.case-dialog-div下，否则 全屏 功能不起作用
.case-dialog-class {
    position: fixed;
    pointer-events: auto; // dialog本身区域不让“穿透点击”
    display: block;
    height: 100%;
    width: 55%; // width: 959px;
    left: 45%;
    // right: 0px; // 未使用弹窗右侧滑入动画效果时使用
    margin-top: 0px !important;
    padding: 10px !important;
    overflow: auto;
}

/*弹窗动画实现*/
@keyframes dialog-fade-in {
    0% {
        transform: translate3d(100%, 0, 0);
        opacity: 0;
    }
    100% {
        transform: translate3d(0, 0, 0);
        opacity: 1;
    }
}

@keyframes dialog-fade-out {
    0% {
        transform: translate3d(0, 0, 0);
        opacity: 1;
    }
    100% {
        transform: translate3d(100%, 0, 0);
        opacity: 0;
    }
}

.case-dialog-div {
    .el-dialog__wrapper {
        // pointer-events: none; // 可点击dialog区域外的html元素
        .el-dialog__header {
            padding: 10px 20px 10px 10px; // 调整header大小
            .el-dialog__headerbtn {
                top: 10px; // 调整x按钮位置
            }
        }
        .el-dialog__body {
            overflow: auto;
            padding: 2px 5px 5px 5px !important;
        }
    }

    // 用例详情部分组件公用样式
    .case-detail-div {
        border-style: solid;
        border-width: 1px;
        border-style: solid;
        background: rgba(241, 239, 239, 0.438);
        border-color: rgb(204, 206, 206);
        margin: 5px 0px 5px 0px;
        padding: 10px 0px 10px 0px;
    }

    // 测试用例步骤表
    .case-step-table {
        overflow: "auto";
    }

    // 测试用例标签
    .el-tag {
        margin-right: 10px;
    }

    // 新增测试用例标签按钮
    .button-new-tag {
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }

    // 测试用例标签编辑输入框
    .input-new-tag {
        width: 90px;
        vertical-align: bottom;
    }

    .el-table__row td {
        padding: 5px 0px !important;
    }
    .cell {
        padding: 0px 3px !important;
    }

    // 操作按钮样式更改
    .operationBtn {
        padding: 7px 3px;
        margin: 1px;
    }
}
</style>
