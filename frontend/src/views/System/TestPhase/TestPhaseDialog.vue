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
                <el-form-item label="阶段名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="唯一编码" prop="code">
                    <el-input v-model="dialogForm.code"></el-input>
                </el-form-item>
                <el-form-item label="阶段顺序" prop="order">
                    <el-input v-model="dialogForm.order"></el-input>
                </el-form-item>
                <el-form-item label="阶段描述" prop="desc">
                    <el-input v-model="dialogForm.desc" type="textarea"></el-input>
                </el-form-item>
                <el-form-item label="是否默认阶段" prop="default">
                    <el-checkbox v-model="dialogForm.default"></el-checkbox>
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
        "dialogTitle",
        "dialogVisible",
        "dialogFormData",
        "row",
        "tableData",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),
            rules: {
                name: [
                    {
                        required: true,
                        message: "请填写阶段名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                code: [
                    {
                        required: true,
                        message: "请填写唯一编码",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 20,
                        message: "长度在 1 到 20 个字符",
                        trigger: "blur",
                    },
                ],
                order: [
                    {
                        required: true,
                        message: "请填写阶段顺序",
                        trigger: "blur",
                    },
                    {
                        validator(rule, value, callback) {
                            if (!Number.isInteger(Number(value))) {
                                callback(new Error("请输入整数"));
                            } else if (Number(value) < 0) {
                                callback(new Error("请输入大于0的整数"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "测试阶段描述不能超过 300 个字符",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        add() {
            this.$api.testPhase
                .addTestPhase(this.dialogForm)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.closeDialog();
                        this.$parent.queryRows();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        update() {
            this.$api.testPhase
                .updateTestPhase(this.dialogForm)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.closeDialog();

                        this.$parent.queryRows();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error("修改失败： " + res.msg || res.message);
                });
        },
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add();
                    } else {
                        this.update();
                    }
                }
            });
        },
    },
};
</script>

<style scoped>
</style>