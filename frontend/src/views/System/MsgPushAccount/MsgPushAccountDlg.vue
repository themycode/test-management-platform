<template>
    <el-dialog
        :title="dialogTitle"
        :width="dialogWidth"
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
                :label-width="dialogFormLabeWidth"
            >
                <el-form-item label="账号" prop="account">
                    <el-input v-model="dialogForm.account"></el-input>
                </el-form-item>
                <el-form-item label="类型" prop="type">
                    <el-select v-model="dialogForm.type" clearable placeholder="请选择账号类型">
                        <el-option
                            v-for="item in typeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="描述" prop="email">
                    <el-input v-model="dialogForm.desc" type="textarea"></el-input>
                </el-form-item>

                <el-form-item label="是否启用" prop="isActive">
                    <el-radio-group v-model="dialogForm.isActive">
                        <el-radio
                            v-for="item in statusOptions"
                            :key="item.value"
                            :label="item.value"
                        >{{ item.label }}</el-radio>
                    </el-radio-group>
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
    props: [
        "dialogVisible",
        "dialogTitle",
        "dialogFormData",
        "tableData",
        "row",
        "statusOptions",
        "typeOptions",
    ],
    mixins:[elDialogMixin],
    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),
            rules: {
                account: [
                    {
                        required: true,
                        message: "请填写账号",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                type: [
                    {
                        required: true,
                        message: "请选择账号类型",
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "长度在 0 到 300 个字符",
                        trigger: "blur",
                    },
                ],
                isActive: [
                    {
                        required: true,
                        message: "请选是否启用",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        // 保存账号
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add(this.$api.msgPushAccount.addAccount);
                    } else {
                        this.update(this.$api.msgPushAccount.updateAccount);
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
};
</script>

<style scoped>
</style>
