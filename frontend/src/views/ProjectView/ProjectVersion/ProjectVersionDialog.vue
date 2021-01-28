<template>
    <el-dialog
        :title="dialogTitle"
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
                :label-width="dialogFormLabeWidth"
            >
                <el-form-item label="名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="关联迭代" prop="sprint">
                    <el-select
                        v-model="dialogForm.sprint"
                        :multiple="false"
                        value-key="id"
                        clearable
                        filterable
                        placeholder="请选择需要关联的迭代"
                    >
                        <el-option
                            v-for="item in sprintOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="预估开始时间" prop="beginTime">
                    <el-date-picker
                        v-model="dialogForm.beginTime"
                        type="date"
                        placeholder="预估开始日期"
                        value-format="yyyy-MM-dd"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="预估结束日期" prop="endTime">
                    <el-date-picker
                        v-model="dialogForm.endTime"
                        type="date"
                        placeholder="预估结束时间"
                        value-format="yyyy-MM-dd"
                    ></el-date-picker>
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
        "row",
    ],
    mixins: [elDialogMixin],

    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),
            sprintOptions: [], // 存放关联迭代下拉选项
            rules: {
                name: [
                    {
                        required: true,
                        message: "请填写版本名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                sprint: [
                    {
                        required: true,
                        message: "请选择版本要关联的迭代",
                        trigger: "change",
                    },
                ],
                beginTime: [
                    {
                        required: true,
                        message: "请选择预估起始日期",
                        trigger: "change",
                    },
                ],
                endTime: [
                    {
                        required: true,
                        message: "请选择预估结束日期",
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
            },
        };
    },
    methods: {
        add() {
            this.requestData = {
                name: this.dialogForm.name,
                beginTime: this.dialogForm.beginTime,
                endTime: this.dialogForm.endTime,
                desc: this.dialogForm.desc,
                projectId: this.dialogForm.projectId,
                productId: this.dialogForm.productId,
                sprintId: this.dialogForm.sprint.id,
                desc: this.dialogForm.desc,
            };

            this.$api.projectVersion
                .addProjectVersion(this.requestData)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.closeDialog();

                        let version = res.data;
                        version["sprint"] = this.dialogForm.sprint.name;
                        version["platformProjectVersionName"] = "";
                        version["platformProjectVersionId"] = "";
                        version["platform"] = "";
                        this.tableData.splice(0, 0, version);
                        this.$parent.total += 1;

                        if (this.tableData.length > this.$parent.pageSize) {
                            // 如果当前页面记录数超过页面大小，则删除最后一条记录
                            this.tableData.splice(-1, 1);
                        }
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        update() {
            this.requestData = {
                id: this.dialogForm.id,
                name: this.dialogForm.name,
                beginTime: this.dialogForm.beginTime,
                endTime: this.dialogForm.endTime,
                desc: this.dialogForm.desc,
                projectId: this.dialogForm.projectId,
                sprintId: this.dialogForm.sprint.id,
                desc: this.dialogForm.desc,
            };
            this.$api.projectVersion
                .updateProjectVersion(this.requestData)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.closeDialog();

                        let versionInfo = res.data;
                        versionInfo["sprint"] = this.dialogForm.sprint.name;
                        for (let key in versionInfo) {
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
                        this.$message.error("开始日期不能晚于结束日期");
                        return;
                    }

                    if (!this.dialogForm.id) {
                        this.add();
                    } else {
                        this.update();
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
    created() {
        // 获取迭代关联产品所关联的迭代信息
        this.$api.product
            .getProductSprintsDetails({
                productId: this.dialogFormData.productId,
            })
            .then((res) => {
                if (res.success) {
                    this.sprintOptions = res.data;
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
