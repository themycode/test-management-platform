<template>
    <el-dialog
        title="关联项目"
        width="45%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form
                :model="dialogForm"
                :rules="rules"
                ref="dialogForm"
                label-width="130px"
            >
                <el-form-item label="平台" prop="platform">
                    <el-select
                        v-model="dialogForm.platform"
                        :multiple="false"
                        filterable
                        placeholder="请选择待关联项目所在平台"
                        style="width: 100%"
                        @change="onPlatformChange"
                    >
                        <el-option
                            v-for="item in platformOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="关联项目" prop="project">
                    <el-select
                        v-model="dialogForm.project"
                        :multiple="false"
                        value-key="id"
                        clearable
                        filterable
                        placeholder="请选择需要关联的项目"
                        style="width: 100%"
                        @clear="clearProject"
                    >
                        <el-option
                            v-for="item in projectOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                    <br />
                    <span
                        >注：如果需要取消关联，清空已关联项目，执行保存即可</span
                    >
                </el-form-item>
                <el-form-item
                    v-if="dialogForm.platform == 'jira'"
                    label="缺陷归属类型"
                    prop="defectIssueTypeId"
                >
                    <el-select
                        v-model="dialogForm.defectIssueTypeId"
                        filterable
                        placeholder="请选择缺陷归属类型"
                        style="width: 100%"
                    >
                        <el-option
                            v-for="item in issueTypeOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item
                    label="自定义字段映射"
                    v-if="dialogForm.platform == 'jira'"
                >
                    <div>
                        <el-select
                            v-model="systemField"
                            :multiple="false"
                            filterable
                            placeholder="请选择系统自定义字段"
                            style="width: 45%"
                        >
                            <el-option
                                v-for="item in systomFieldsOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            ></el-option>
                        </el-select>
                        <el-select
                            v-model="platformField"
                            :multiple="false"
                            filterable
                            placeholder="请选择关联平台自定义字段"
                            style="width: 45%"
                        >
                            <el-option
                                v-for="item in customFieldOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            ></el-option>
                        </el-select>
                        <span class="my-icon-wrapper">
                            <i
                                class="el-icon-plus"
                                @click="addCustomFieldMap"
                            ></i>
                        </span>
                    </div>
                </el-form-item>
                <el-form-item
                    v-for="(item, index) in dialogForm.customFieldMapArray"
                    :key="item.key"
                >
                    <el-select
                        v-model="item.key"
                        :multiple="false"
                        filterable
                        placeholder="请选择系统自定义字段"
                        style="width: 45%"
                        @change="onSystemFieldSelectChange($event, index)"
                        @visible-change="
                            onSystemFieldVisibleChange($event, item.key)
                        "
                    >
                        <el-option
                            v-for="item in systomFieldsOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                    <el-select
                        v-model="item.value"
                        :multiple="false"
                        filterable
                        placeholder="请选择关联平台自定义字段"
                        style="width: 45%"
                    >
                        <el-option
                            v-for="item in customFieldOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>

                    <span class="my-icon-wrapper">
                        <i
                            class="el-icon-delete"
                            @click="delCustomFieldMap($event, index, item.key)"
                        ></i>
                    </span>
                </el-form-item>
                <el-form-item label="缺陷严重级别映射" prop="defectSeverityMap">
                    <el-tooltip
                        effect="dark"
                        content="系统缺陷严重级别划分为：致命，严重，一般，轻微；如果关联项目的缺陷严重级别划分和系统不一致，则需要为其建立映射关系"
                        placement="right-start"
                    >
                        <i class="fa fa-question-circle" aria-hidden="true"></i>
                    </el-tooltip>
                    <el-input
                        :placeholder="severityMapPlaceholder"
                        v-model="dialogForm.defectSeverityMap"
                        type="textarea"
                        :autosize="{ minRows: 2 }"
                        @blur="onSeverityMapBlur"
                    ></el-input>
                </el-form-item>
                <el-form-item label="缺陷状态映射" prop="defectStatusMap">
                    <el-tooltip
                        effect="dark"
                        content="系统缺陷状态划分为：新建，处理中，延期处理，已解决，已拒绝，已关闭，重新打开，如果关联项目的缺陷状态和系统不一致，则需要为其建立映射关系"
                        placement="right-start"
                    >
                        <i class="fa fa-question-circle" aria-hidden="true"></i>
                    </el-tooltip>
                    <el-input
                        :placeholder="statusMapPlaceholder"
                        v-model="dialogForm.defectStatusMap"
                        type="textarea"
                        :autosize="{ minRows: 2 }"
                        @blur="onStatusMapBlur"
                    ></el-input>
                </el-form-item>

                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog">取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')"
                            >保存</el-button
                        >
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "dialogFormData", "row"],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: JSON.parse(JSON.stringify(this.dialogFormData)),
            // 存放关联平台下拉选项
            platformOptions: [
                { id: "jira", name: "jira" },
                { id: "zentao", name: "禅道" },
                // { id: "tapd", name: "tapd" },
            ],
            projectOptions: [], // 存放关联项目下拉选项
            issueTypeOptions: [], // 问题类型选项列表
            defectCustomFieldsOptions: [],
            customFieldOptions: [], // 存放不同平台自定义字段
            rules: {
                platform: [
                    {
                        type: "string",
                        required: true,
                        message: "请选择待关联项目所在平台",
                        trigger: "change",
                    },
                ],
            },
            
            severityMapPlaceholder:
                'JSON格式,形如{"Critical":"致命", "Major":"严重"}',
            statusMapPlaceholder:
                'JSON格式,形如{"打开":"新建","已接受":"处理中":"正在处理":"处理中","reopen":"重新打开"}',
            severityMapFormatError: false, // 标记缺陷严重级别映射配置格式化是否出错
            statusMapFormatError: false, // 标记缺陷状态映射配置格式化是否出错
            systemField: "", // 存放用户选取的系统自定义字段
            systemFieldOld: "", // 存放用户更改已选取的系统自定义字段之前的值
            platformField: "", // 存放用户选取的平台自定义字段
        };
    },
    methods: {
        onPlatformChange(value) {
            if (!value) {
                return;
            }
            this.dialogForm.project = null;
            this.platformField = "";
            this.dialogForm.customFieldMapArray = [];

            this.getProjectOptions();
            if (this.dialogForm.platform == "jira") {
                this.getJiraIssueTypeOptions();
                this.getJiraIssueCustomFieldOptions();
            } else if (this.dialogForm.platform == "zentao") {
                this.getZentaoDefectCustomFieldOptions();
            } else {
            }
        },
        // 获取关联项目列表
        getProjectOptions() {
            this.projectOptions = [];

            this.$api.project
                .getPlatformProjects({
                    platform: this.dialogForm.platform,
                })
                .then((res) => {
                    if (res.success) {
                        this.projectOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 获取系统定义字段
        getSystomFieldsOptions() {
            this.systomFieldsOptions = [];

            this.$api.project
                .getSystomFieldsOptions()
                .then((res) => {
                    if (res.success) {
                        this.systomFieldsOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 增加系统自定义字段和平台自定义字段的映射
        addCustomFieldMap() {
            if (!this.systemField) {
                this.$alert("请选择系统自定义字段", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (!this.platformField) {
                this.$alert("请选择关联平台自定义字段", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (
                this.dialogForm.customFieldMap.hasOwnProperty(this.systemField)
            ) {
                this.$message.warning("已添加该系统自定义字段，请选择其它字段");
                return;
            }
            this.dialogForm.customFieldMap[
                this.systemField
            ] = this.platformField;
            this.dialogForm.customFieldMapArray.splice(0, 0, {
                key: this.systemField,
                value: this.platformField,
            });
        },
        // 删除系统自定义字段和平台自定义字段的映射
        delCustomFieldMap(event, index, key) {
            delete this.dialogForm.customFieldMap[key];
            this.dialogForm.customFieldMapArray.splice(index, 1);
        },
        // 系统自定义字段选择框值变更时事件处理函数
        onSystemFieldSelectChange(value, index) {
            if (this.dialogForm.customFieldMap.hasOwnProperty(value)) {
                this.$message.warning("该系统自定义字段已存在，请选择其它字段");
                this.dialogForm.customFieldMapArray[
                    index
                ].key = this.systemFieldOld;

                return;
            }
        },
        // 平台自定义字段打开、隐藏下拉选取列表时的事件处理函数
        onSystemFieldVisibleChange(value, systemField) {
            if (value) {
                this.systemFieldOld = systemField;
            }
        },
        // 获取jira问题类型列表
        getJiraIssueTypeOptions() {
            this.issueTypeOptions = [];
            this.$api.project
                .getJiraIssueTypes()
                .then((res) => {
                    if (res.success) {
                        this.issueTypeOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 获取jira问题自定义字段列表
        getJiraIssueCustomFieldOptions() {
            this.customFieldOptions = [];
            this.$api.project
                .getJiraIssueCustomFields()
                .then((res) => {
                    if (res.success) {
                        this.customFieldOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 获取禅道缺陷自定义字段列表
        getZentaoDefectCustomFieldOptions() {
            this.customFieldOptions = [];
            this.$api.project
                .getZentaoDefectCustomFields()
                .then((res) => {
                    if (res.success) {
                        this.customFieldOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 关联项目
        bindProject() {
            if (this.severityMapFormatError) {
                this.$alert(
                    "缺陷严重级别映射配置格式错误，请按json格式填写",
                    "提示",
                    {
                        confirmButtonText: "确定",
                    }
                );
                return;
            }
            if (this.statusMapFormatError) {
                this.$alert(
                    "缺陷状态映射配置格式错误，请按json格式填写",
                    "提示",
                    {
                        confirmButtonText: "确定",
                    }
                );

                return;
            }

            this.dialogForm.customFieldMap = {};
            for (
                let i = 0;
                i < this.dialogForm.customFieldMapArray.length;
                i++
            ) {
                this.dialogForm.customFieldMap[
                    this.dialogForm.customFieldMapArray[i].key
                ] = this.dialogForm.customFieldMapArray[i].value;
            }

            let data = {
                projectId: this.row.id,
                platform: this.dialogForm.platform,
                platformProjectId: this.dialogForm.project.id,
                platformProjectName: this.dialogForm.project.name,
                defectIssueTypeId: this.dialogForm.defectIssueTypeId,
                defectStatusMap: this.dialogForm.defectStatusMap,
                defectSeverityMap: this.dialogForm.defectSeverityMap,
                customFieldMap: this.dialogForm.customFieldMap,
            };

            this.$api.project
                .bindPlatformProject(data)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        for (let key in res.data) {
                            if (key in this.row) {
                                this.row[key] = res.data[key];
                            }
                        }
                        this.closeDialog();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 解除关联
        unbindProject() {
            let data = { projectId: this.row.id };
            this.$api.project
                .unbindPlatformProject(data)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        for (let key in res.data) {
                            if (key in this.row) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                this.row[key] = res.data[key];
                            }
                        }
                        this.closeDialog();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        clearProject() {
            this.dialogForm.project = null;
        },
        onSeverityMapBlur() {
            try {
                let temp = this.dialogForm.defectSeverityMap;
                temp = temp.trim();

                if (temp) {
                    if (temp.startsWith("{")) {
                        JSON.parse(temp);
                    } else {
                        this.severityMapFormatError = true;
                        this.$message.error(
                            "缺陷严重级别映射配置格式错误，请按json格式填写"
                        );
                        return;
                    }
                }
                this.severityMapFormatError = false;
            } catch (err) {
                this.severityMapFormatError = true;
                this.$message.error(
                    "缺陷严重级别映射配置格式错误，请按json格式填写:" +
                        err.message
                );
            }
        },
        onStatusMapBlur() {
            try {
                let temp = this.dialogForm.defectStatusMap;
                temp = temp.trim();
                if (temp) {
                    if (temp.startsWith("{")) {
                        JSON.parse(temp);
                    } else {
                        this.statusMapFormatError = true;
                        this.$message.error(
                            "缺陷状态映射配置格式错误，请按json格式填写"
                        );
                        return;
                    }
                }
                this.statusMapFormatError = false;
            } catch (err) {
                this.statusMapFormatError = true;
                this.$message.error(
                    "缺陷状态映射配置格式错误，请按json格式填写:" + err.message
                );
            }
        },
        // 保存
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (this.dialogForm.project) {
                        this.bindProject();
                    } else {
                        this.unbindProject();
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
    created() {
        this.getProjectOptions();
        this.getSystomFieldsOptions();
        if (this.dialogForm.platform == "jira") {
            this.getJiraIssueTypeOptions();
            this.getJiraIssueCustomFieldOptions();
        } else if (this.dialogForm.platform == "zentao") {
            this.getZentaoDefectCustomFieldOptions();
        }
    },
};
</script>

<style scoped>
.my-dialog-footer {
    text-align: center;
    margin-left: -130px;
}

.my-dialog-body .el-form-item {
    margin-right: 20px;
}

.my-icon-wrapper {
    display: inline-block;
    position: relative;
    top: 3px;
    margin-left: 5px;
    font-size: 20px;
    line-height: 37px;
    height: 37px;
}

.el-tooltip {
    position: relative;
    float: left;
    left: -15px;
}

/deep/ .el-form-item {
    margin-bottom: 20px;
}
</style>
