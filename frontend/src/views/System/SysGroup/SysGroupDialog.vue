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
                <el-form-item label="组别名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="组别描述" prop="desc">
                    <el-input v-model="dialogForm.desc" type="textarea"></el-input>
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
        "userName",
    ],
    mixins: [elDialogMixin],

    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),

            rules: {
                name: [
                    {
                        required: true,
                        message: "请输入组别名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "资源描述不能超过 300 个字符",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        // 保存组别
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add(this.$api.sysGroup.addSysGroup);
                    } else {
                        this.update(this.$api.sysGroup.updateSysGroup)
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
