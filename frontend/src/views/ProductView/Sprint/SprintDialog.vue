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
                <el-form-item label="名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="版本" prop="version">
                    <el-input v-model="dialogForm.version"></el-input>
                </el-form-item>
                <el-form-item label="预估开始时间" prop="beginTime">
                    <el-date-picker
                        v-model="dialogForm.beginTime"
                        type="date"
                        placeholder="预估开始时间"
                        value-format="yyyy-MM-dd"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="预估结束时间" prop="endTime">
                    <el-date-picker
                        v-model="dialogForm.endTime"
                        type="date"
                        placeholder="预估结束时间"
                        value-format="yyyy-MM-dd"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="状态" prop="status">
                    <el-select v-model="dialogForm.status" placeholder="请选择状态">
                        <el-option
                            v-for="item in this.statusOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="描述" prop="desc">
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
        "tableData",
        "statusOptions",
        "row",
        "total",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),
            rules: {
                name: [
                    {
                        required: true,
                        message: "请填写迭代名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                version: [
                    {
                        required: false,
                        message: "请填写迭代版本",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                beginTime: [
                    {
                        required: true,
                        message: "请选择预估起始时间",
                        trigger: "change",
                    },
                ],
                endTime: [
                    {
                        required: true,
                        message: "请选择预估结束时间",
                        trigger: "change",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "不能超过 300 个字符",
                        trigger: "blur",
                    },
                ],
                status: [
                    {
                        required: true,
                        message: "请选择状态",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        // 保存
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    const beginTime = new Date(
                        this.dialogForm.beginTime.replace(/-/g, "/")
                    ).getTime();

                    const endTime = new Date(
                        this.dialogForm.endTime.replace(/-/g, "/")
                    ).getTime();

                    if (beginTime > endTime) {
                        this.$message.error("开始时间不能晚于结束时间");
                        return;
                    }

                    if (!this.dialogForm.id) {
                        this.add(this.$api.sprint.addSprint);
                    } else {
                        this.update(this.$api.sprint.updateSprint);
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
    created() {
        // 获取产品
        this.$api.product
            .getProductsDetails()
            .then((res) => {
                if (res.success) {
                    this.productOptions = res.data;
                } else {
                    this.$message.error(res.msg);
                }
            })
            .catch((res) => {
                this.$message.error(res.msg || res.message);
            });
    },
};
</script>

<style scoped>
</style>
