<template>
    <el-dialog
        title="关联项目版本"
        width="45%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form :model="dialogForm" ref="dialogForm" :label-width="dialogFormLabeWidth">
                <el-form-item label="关联项目版本" prop="projectVersion">
                    <el-select
                        v-model="dialogForm.projectVersion"
                        :multiple="false"
                        value-key="id"
                        clearable
                        filterable
                        placeholder="请选择需要关联的项目版"
                        @clear="clearProject"
                    >
                        <el-option
                            v-for="item in projectVersionOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                    <br/>
                    <span>注：如果需要取消关联，清空已关联项目版本，执行保存即可</span>
                </el-form-item>
                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog">取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')">保存</el-button>
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
            dialogForm: JSON.parse(
                JSON.stringify(this.dialogFormData)
            ),
            projectVersionOptions: [], // 存放关联项目下拉选项
        };
    },
    methods: {
        // 获取关联项目版本列表
        getProjectVersionOptions() {
            this.$api.projectVersion
                .getPlatformProjectVersions({
                    projectId: this.row.projectId,
                })
                .then((res) => {
                    if (res.success) {
                        this.projectVersionOptions = res.data;
                    } else {
                        this.projectVersionOptions = [];
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.projectVersionOptions = [];
                    this.$message.error(res.msg || res.message);
                });
        },
        // 关联项目版本
        bindProjectVersion() {
            let data = {
                projectVersionId: this.row.id,
                platform: this.dialogForm.projectVersion.platform,
                platformProjectVersionId: this.dialogForm.projectVersion.id,
                platformProjectVersionName: this.dialogForm.projectVersion.name,
            };

            this.$api.projectVersion
                .bindPlatformProjectVersion(data)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.closeDialog();
                        for (let key in res.data) {
                            if (key in this.row) {
                                this.row[key] = res.data[key];
                            }
                        }                        
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
            let data = { projectVersionId: this.row.id };
            this.$api.projectVersion
                .unbindPlatformProjectVersion(data)
                .then((res) => {
                    if (res.success) {
                        this.closeDialog();
                        this.$message.success(res.msg);
                        for (let key in res.data) {
                            if (key in this.row) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                this.row[key] = res.data[key];
                            }
                        }                        
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        clearProject() {
            this.dialogForm.projectVersion = null;
        },
        // 保存
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (this.dialogForm.projectVersion) {
                        this.bindProjectVersion();
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
        this.getProjectVersionOptions();
    },
};
</script>

<style scoped>

</style>
