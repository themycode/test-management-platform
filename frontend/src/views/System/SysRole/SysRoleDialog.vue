<template>
    <el-dialog
        :title="dialogTitle"
        :width="dialogWidth"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
    >
        <div class="my-dialog-body">
            <el-form
                :model="dialogForm"
                :rules="rules"
                ref="dialogForm"
                :label-width="dialogFormLabeWidth"
            >
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="角色描述" prop="desc">
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
                <el-form-item>
                    <div class="dialog-footer">
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
        "statusOptions",
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
                        message: "请输入角色名称",
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
                        message: "角色描述不能超过 300 个字符",
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
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add(this.$api.sysRole.addSysRole);
                    } else {
                        this.update(this.$api.sysRole.updateSysRole);
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
