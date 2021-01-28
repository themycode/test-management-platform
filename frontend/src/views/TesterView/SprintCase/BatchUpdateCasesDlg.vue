<template>
    <el-dialog
        title="批量修改用例"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="true"
        :close-on-press-escape="closeOnPressEscape"
        :append-to-body="true"
        custom-class="batch-update-cases-dlg-class"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <div class="remark-text">
                说明：
                <br />1、未勾选【是否参与批量修改】则表示不修改该配置项，否则表示会修改，其它具体规则查看具体配置项说明
                <br />2、数据量比较大的情况下，可能比较耗时，提交请求后请耐心等待
            </div>
            <el-form
                :model="dialogForm"
                :rules="rules"
                ref="dialogForm"
                label-width="70px"
                class="case-info-form"
                size="mini"
            >
                <el-form-item label="优先级" prop="priority">
                    <el-select v-model="dialogForm.priority" style="width: 100px;" size="mini">
                        <el-option
                            v-for="item in priorityOptions"
                            :key="item"
                            :label="item"
                            :value="item"
                        ></el-option>
                    </el-select>
                    <el-checkbox class="participation-check-box" v-model="priorityChecked">是否参与批量修改</el-checkbox>
                </el-form-item>
                <el-form-item label="执行方式" prop="executionMethod">
                    <el-select
                        v-model="dialogForm.executionMethod"
                        style="width: 100px;"
                        size="mini"
                    >
                        <el-option
                            v-for="item in executionMethodOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                    <el-checkbox
                        class="participation-check-box"
                        v-model="executionMethodChecked"
                    >是否参与批量修改</el-checkbox>
                </el-form-item>
                <el-form-item label="执行阶段" prop="executionPhase">
                    <el-select
                        v-model="dialogForm.executionPhase"
                        style="width: 70%;"
                        size="mini"
                        multiple
                    >
                        <el-option
                            v-for="item in executionPhaseOptions"
                            :key="item.value"
                            :label="
                item.label +
                  '/' +
                  executedEachSprintMap[item.value]['executedEachSprint']
              "
                            :value="item.value"
                        >
                            
                            <span
                                style="float: right; color: #8492a6; font-size: 13px;margin-right:50px; "
                            >
                                <span>每个迭代都执行？：</span>
                                <el-radio
                                    v-model="
                    executedEachSprintMap[item.value]['executedEachSprint']
                  "
                                    label="Y"
                                    @click.native="clickRadio(item, 'Y')"
                                >是</el-radio>
                                <el-radio
                                    v-model="
                    executedEachSprintMap[item.value]['executedEachSprint']
                  "
                                    label="N"
                                    @click.native="clickRadio(item, 'N')"
                                >否</el-radio>
                            </span>
                        </el-option>
                    </el-select>
                    <el-checkbox
                        class="participation-check-box"
                        v-model="executionPhaseChecked"
                    >是否参与批量修改</el-checkbox>
                </el-form-item>
                <el-form-item label="用例备注" prop="desc">
                    <div>
                        <el-input
                            type="textarea"
                            :autosize="{ minRows: 3 }"
                            ref="descInput"
                            placeholder="请输入用例备注(注意：如果已勾【选是否参与批量修改】，并且用例备注为空，则会清空已有用例备注)"
                            v-model="dialogForm.desc"
                            maxlength="1000"
                            show-word-limit
                        ></el-input>
                        <el-checkbox class="participation-check-box" v-model="descChecked">是否参与批量修改</el-checkbox>
                    </div>
                </el-form-item>
                <el-form-item label="前置条件" prop="preconditionInput">
                    <el-input
                        ref="preconditionInput"
                        type="textarea"
                        :autosize="{ minRows: 3 }"
                        placeholder="请输入前置条件(注意：如果已勾【选是否参与批量修改】，并且前置条件为空，则会清空已有前置条件)"
                        v-model="dialogForm.precondition"
                        maxlength="1000"
                        show-word-limit
                    ></el-input>
                    <el-checkbox
                        class="participation-check-box"
                        v-model="preconditionChecked"
                    >是否参与批量修改</el-checkbox>
                </el-form-item>

                <el-form-item label="后置条件" prop="postcondition">
                    <el-input
                        style="white-space: pre-wrap; word-wrap: break-word;"
                        ref="postconditionInput"
                        type="textarea"
                        :autosize="{ minRows: 3 }"
                        placeholder="请输入后置条件(注意：如果已勾【选是否参与批量修改】，并且后置条件为空，则会清空已有后置条件)"
                        v-model="dialogForm.postcondition"
                        maxlength="1000"
                        show-word-limit
                    ></el-input>
                    <el-checkbox
                        class="participation-check-box"
                        v-model="postconditionChecked"
                    >是否参与批量修改</el-checkbox>
                </el-form-item>
                <el-form-item label="用例标签" prop="tags">
                    <el-tag
                        :key="tag"
                        v-for="tag in dialogForm.tags"
                        :closable="true"
                        :disable-transitions="true"
                        @close="onCloseTag(tag)"
                    >{{ tag }}</el-tag>
                    <el-input
                        class="input-new-tag"
                        v-if="tagInputVisible"
                        v-model="tagInputValue"
                        ref="saveTagInput"
                        size="small"
                        @keyup.enter.native="handleTagInputConfirm"
                        @blur="handleTagInputConfirm"
                    ></el-input>

                    <el-button class="button-new-tag" size="small" @click="showTagInput">+点击新增标签</el-button>
                    <el-checkbox class="participation-check-box" v-model="tagsChecked">是否参与批量修改</el-checkbox>
                    <div class="custom-form-text">注意：如果已勾【选是否参与批量修改】，并且未设置用例标签，则会清空用例已有标签</div>
                </el-form-item>
                <el-form-item class="dialog-footer-form-item">
                    <!-- <div class="my-dialog-footer">
                        <el-button @click="closeDialog" style>取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')" style>保存</el-button>
                    </div>-->
                </el-form-item>
            </el-form>
        </div>
        <div slot="footer">
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" @click="save('dialogForm')">保存</el-button>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: [
        "dialogVisible",
        "executionPhaseOptions",
        "executedEachSprintDict",
        "casesInfoForUpdate",
        "suiteId",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: {
                priority: "P3", //用例优先级
                executionMethod: "handwork", // 执行方式
                executionPhase: ["SystemTesting"], //执行阶段
                desc: "", // 用例备注
                precondition: "", //前置条件
                postcondition: "", // 后置条件
                tags: [], // 用例标签
            },
            priorityChecked: true, // 是否勾选优先级
            priorityOptions: ["p1", "P2", "P3", "P4"],
            executionMethodOptions: [
                { label: "手工", value: "handwork" },
                { label: "自动化", value: "automation" },
            ],
            executionMethodChecked: false, // 是否勾选执行方式
            executionPhaseChecked: false, // 是否勾选执阶段
            descChecked: false, // 是否勾选描述
            preconditionChecked: false, // 是否勾选前置条件
            postconditionChecked: false, //是否勾选后置条件
            tagsChecked: false, // 是否勾选标签
            tagInputVisible: false, // 控制测试用例标签输入对话框是否可见 false 不可见 true 可见
            tagInputValue: "", // 测试用例标签输入框的值
            executedEachSprintMap: {},
            rules: {
                desc: [
                    {
                        min: 0,
                        max: 1000,
                        message: "用例备注不能超过 1000 个字符",
                        trigger: "blur",
                    },
                ],
                precondition: [
                    {
                        min: 0,
                        max: 1000,
                        message: "前置条件不能超过 1000 个字符",
                        trigger: "blur",
                    },
                ],
                postcondition: [
                    {
                        min: 0,
                        max: 1000,
                        message: "后置条件不能超过 1000 个字符",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        //执行阶段下拉列表的radio点击事件处理函数
        clickRadio(item, value) {
            this.executedEachSprintMap[item.value][
                "executedEachSprint"
            ] = value;
        },

        // 删除tag
        onCloseTag(tag) {
            this.dialogForm.tags.splice(this.caseInfo.tags.indexOf(tag), 1);
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
                this.dialogForm.tags.indexOf(tagInputValue) == -1
            ) {
                this.dialogForm.tags.push(tagInputValue);
            }
            this.tagInputVisible = false;
            this.tagInputValue = "";
        },
        // 用例基础信息校验
        caseInfoCheck() {
            if (this.priorityChecked && !this.dialogForm.priority) {
                this.$message.error("优先级不能为空");
                return false;
            }

            if (
                this.executionMethodChecked &&
                !this.dialogForm.executionMethod
            ) {
                this.$message.error("执行方式不能为空");
                return false;
            }

            if (
                this.executionPhaseChecked &&
                !this.dialogForm.executionPhase.length
            ) {
                this.$message.error("执行阶段不能为空");
                return false;
            }

            return true;
        },
        // 批量修改测试用例
        save(formName) {
            try {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        if (!this.caseInfoCheck()) {
                            return;
                        }
                        let caseInfo = {};
                        if (this.priorityChecked) {
                            caseInfo["priority"] = this.dialogForm.priority;
                        }

                        if (this.executionMethodChecked) {
                            caseInfo[
                                "executionMethod"
                            ] = this.dialogForm.executionMethod;
                        }
                        if (this.executionPhaseChecked) {
                            caseInfo[
                                "executionPhase"
                            ] = this.dialogForm.executionPhase;

                            let tempStr = "";
                            for (
                                let i = 0;
                                i < caseInfo["executionPhase"].length;
                                i++
                            ) {
                                let executionPhase =
                                    caseInfo["executionPhase"][i];
                                // this.executedEachSprintMap 一定存在key为executionPhase的值，所以不做判断
                                if (
                                    executionPhase in this.executedEachSprintMap
                                ) {
                                    tempStr +=
                                        executionPhase +
                                        "/" +
                                        this.executedEachSprintMap[
                                            executionPhase
                                        ]["executedEachSprint"] +
                                        ",";
                                }
                            }
                            caseInfo["executedEachSprint"] = tempStr.substring(
                                0,
                                tempStr.length - 1
                            );

                            caseInfo["executionPhase"] = caseInfo[
                                "executionPhase"
                            ].join(",");
                        }
                        if (this.descChecked) {
                            caseInfo["desc"] = this.dialogForm.desc;
                        }
                        if (this.preconditionChecked) {
                            caseInfo[
                                "precondition"
                            ] = this.dialogForm.precondition;
                        }
                        if (this.postconditionChecked) {
                            caseInfo[
                                "postcondition"
                            ] = this.dialogForm.postcondition;
                        }
                        if (this.tagsChecked) {
                            caseInfo["tags"] = this.dialogForm.tags;
                            caseInfo["tags"] = caseInfo["tags"].join(",");
                        }

                        caseInfo["targetCases"] = this.casesInfoForUpdate;
                        caseInfo["suiteId"] = this.suiteId;

                        // 发送更新用例请求
                        this.$parent.loading = true;
                        this.$api.sprintCaseTable
                            .batachUpdateTestCases(caseInfo)
                            .then((res) => {
                                if (res.success) {
                                    this.$message.success(res.msg);
                                } else {
                                    this.$message.error(res.msg);
                                }
                                this.$parent.loading = false;
                                this.$parent.queryRows();
                            })
                            .catch((res) => {
                                this.$parent.loading = false;
                                this.$message.error(res.msg || res.message);
                                this.$parent.queryRows();
                            });
                        this.closeDialog();
                    }
                });
            } catch (err) {
                this.$parent.loading = false;
                this.$message.error(err.message);
            }
        },
    },
    created() {
        this.executedEachSprintMap = JSON.parse(
            JSON.stringify(this.executedEachSprintDict)
        );
    },
};
</script>
<style lang="scss">
.batch-update-cases-dlg-class {
    position: fixed;
    display: block;
    height: 100%;
    width: 50%;
    left: 50%;
    // right: 0px; // 未使用弹窗右侧滑入动画效果时使用
    margin-top: 0px !important;
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
</style>
<style scoped lang="scss" scoped>
.my-dialog-body .el-form-item {
    margin-right: 10px;
}

.remark-text {
    margin-left: 0px;
    color: red;
}

.participation-check-box {
    margin-left: 10px;
}

// 修改textarea的宽度
/deep/ .el-textarea {
    width: 70%;
}

// 用例标签编辑输入框
.input-new-tag {
    width: 90px;
    vertical-align: bottom;
}

// 表单中一些自定义文本样式
.custom-form-text {
    margin-left: -69px;
}
</style>
