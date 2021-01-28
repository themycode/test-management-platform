<template>
    <el-dialog
        title="修改密码"
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
                <el-form-item label="原密码" prop="oldPasswd">
                    <el-input v-model="dialogForm.oldPasswd"  type="input"></el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="newPasswd">
                    <el-input v-model="dialogForm.newPasswd" type="password"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPasswd">
                    <el-input v-model="dialogForm.confirmPasswd" type="password"></el-input>
                </el-form-item>

                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog" style>取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')" style>保存</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    mixins: [elDialogMixin],
    props: ["dialogVisible", "accountData"],
    data() {
        return {
            dialogForm: {
                oldPasswd: "",
                newPasswd: "",
                confirmPasswd: "",
            },
            rules: {
                oldPasswd: [
                    {
                        required: true,
                        message: "请输入原密码",
                        trigger: "blur",
                    },
                ],
                newPasswd: [
                    {
                        required: true,
                        message: "请输入新密码",
                        trigger: "blur",
                    },
                    {
                        min: 6,
                        max: 32,
                        message: "长度在 6 到 32 个字符",
                        trigger: "blur",
                    },
                ],
                confirmPasswd: [
                    {
                        required: true,
                        message: "请再次输入新密码",
                        trigger: "blur",
                    },
                    {
                        min: 6,
                        max: 32,
                        message: "长度在 6 到 32 个字符",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        // 保存
        save(form) {
            let data = {};
            data["oldPasswd"] = this.dialogForm.oldPasswd;
            data["newPasswd"] = this.dialogForm.newPasswd;
            data["confirmPasswd"] = this.dialogForm.confirmPasswd;

            this.$refs[form].validate((valid) => {
                if (valid) {
                    this.$api.sysUser
                        .modifyPasswd(data)
                        .then((res) => {
                            console.log(res);
                            if (res.success) {
                                this.$message.success(res.msg);
                                this.closeDialog();
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                        });
                } else {
                    // this.$message.error("保存失败，请正确填写信息")
                }
            });
        },
    },
};
</script>

<style scoped>
</style>