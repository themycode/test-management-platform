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
                <el-form-item label="姓名" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="dialogForm.email"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="mobile">
                    <el-input v-model="dialogForm.mobile"></el-input>
                </el-form-item>
                <el-form-item label="工号" prop="jobNumber">
                    <el-input v-model="dialogForm.jobNumber"></el-input>
                </el-form-item>
                <el-form-item
                    label="是否启用"
                    prop="isActive"
                    v-if="!operateOneSelf"
                >
                    <el-radio-group v-model="dialogForm.isActive">
                        <el-radio
                            v-for="item in statusOptions"
                            :key="item.value"
                            :label="item.value"
                            >{{ item.label }}</el-radio
                        >
                    </el-radio-group>
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
    props: [
        "dialogVisible",
        "dialogTitle",
        "dialogFormData",
        "row",
        "tableData",
        "statusOptions",
        "operateOneSelf",
    ],
    mixins: [elDialogMixin],

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
                name: [
                    {
                        required: true,
                        message: "请填写姓名",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                email: [
                    {
                        required: true,
                        message: "请填写邮箱",
                        trigger: "blur",
                    },
                    {
                        min: 7,
                        max: 50,
                        message: "长度在 7 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                mobile: [
                    {
                        required: true,
                        message: "请填写手机号",
                        trigger: "blur",
                    },
                    {
                        min: 11,
                        max: 11,
                        message: "手机号必须11位数",
                        trigger: "blur",
                    },
                ],
                jobNumber: [
                    {
                        required: true,
                        message: "请填写工号",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 20,
                        message: "工号不能超过20位数",
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
        // 保存用户
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add(this.$api.sysUser.addSysUser);
                    } else {
                        this.update(this.$api.sysUser.updateSysUser);
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
