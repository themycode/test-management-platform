<template>
    <el-dialog
        :title="dialogTitle"
        :width="dialogWidth"
        :visible="dialogVisible"
        :show-close="showClose"
        append-to-body="false"
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
                <el-form-item label="密码" prop="password">
                    <el-input v-model="dialogForm.password" type="password"></el-input>
                </el-form-item>

                <el-form-item label="平台" prop="platform">
                    <el-select v-model="dialogForm.platform" placeholder="请选择账号关联的平台">
                        <el-option
                            v-for="item in platformOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
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
        "row",
        "tableData",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            platformOptions: [
                { label: "tpad", value: "tpad" },
                { label: "禅道", value: "禅道" },
                { label: "Confluence", value: "Confluence" },
            ],
            dialogForm: Object.assign({}, this.dialogFormData),
            rules: {
                account: [
                    {
                        required: true,
                        message: "请输入账号",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                password: [
                    {
                        required: true,
                        message: "请输入密码",
                        trigger: "blur",
                    },
                    {
                        min: 6,
                        max: 32,
                        message: "长度在 6 到 32 个字符",
                        trigger: "blur",
                    },
                ],
                platform: [
                    {
                        required: true,
                        message: "请选择账号关联的平台",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add(this.$api.sysUser.addRelatedAccount);
                    } else {
                        this.update(this.$api.sysUser.updateRelatedAccount);
                    }
                }
            });
        },
    },
};
</script>

<style scoped>
</style>
