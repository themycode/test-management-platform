<template>
    <el-dialog
        title="克隆用例至迭代"
        width="40%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form :label-width="dialogFormLabeWidth">
                <el-form-item label="克隆至迭代">
                    <el-select
                        v-model="sprintId"
                        size="small"
                        placeholder="请选择迭代"
                        @change="onSprintSelectedChange"
                        style="width:100%"
                    >
                        <el-option
                            v-for="item in sprintOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog">取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')">开始克隆</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "currentModule"],
    mixins: [elDialogMixin],
    data() {
        return {
            sprintOptions: [],
            sprintId: "", // 存放选择的sprintId
        };
    },
    methods: {
        onSprintSelectedChange(value) {
            if (value) {
                sessionStorage.setItem("sprintSelectedForCaseCopy", value);
            }
        },
        save() {
            if (!this.sprintId) {
                this.$alert("未选择迭代项目，请选择", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }
            this.$api.sprintCaseTable
                .copyCaseToSprintDlg({
                    sprintId: this.sprintId,
                    productId: this.$parent.productID,
                    testcases: this.$parent.casesCopyToSprint,
                })
                .then((res) => {
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
        },
        getSprintsDetails() {
            // 请求迭代列表
            this.$api.product
                .getProductSprintsDetails({
                    productId: this.$parent.productID,
                })
                .then((res) => {
                    if (res.success) {
                        this.sprintOptions = res.data;
                        let sprintSelected = sessionStorage.getItem(
                            "sprintSelectedForCaseCopy"
                        );
                        if (sprintSelected) {
                            sprintSelected = parseInt(sprintSelected);
                            let result = this.sprintOptions.some((item) => {
                                if (item.id == sprintSelected) {
                                    return true;
                                }
                            });
                            if (result) {
                                this.sprintId = sprintSelected;
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
    },
    created() {
        this.getSprintsDetails();
    },
};
</script>

<style scoped>
</style>
