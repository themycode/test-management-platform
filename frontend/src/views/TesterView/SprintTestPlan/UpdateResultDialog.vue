<template>
    <el-dialog
        title="批量修改测试结果"
        width="45%"
        :visible="dialogVisible"
        :show-close="showClose"
        :append-to-body="false"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <div style="margin-bottom:10px">批量修改选中记录测试结果为：</div>

            <el-radio-group v-model="testResult">
                <el-radio
                    v-for="item in resultOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                ></el-radio>
            </el-radio-group>
        </div>
        <span slot="footer">
            <el-button @click="closeDialog">取 消</el-button>
            <el-button type="primary" @click="save">确 定</el-button>
        </span>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: [
        "dialogVisible",
        "resultOptions",
        "caseIDsSelected",
        "planRow",
        "tableData",
    ],
    mixins: [elDialogMixin],

    data() {
        return {
            testResult: "通过", // 测试结果
        };
    },
    methods: {
        save() {
            // 更新用例执行结果
            this.$api.testPlanCaseTable
                .updateCaseTestResults({
                    caseIds: this.caseIDsSelected,
                    result: this.testResult,
                    planId:this.planRow.id
                })
                .then((res) => {
                    if (res.success) {
                        this.closeDialog();

                        this.$message.success(res.msg);
                        this.$parent.queryRows();
                        // 更新测试计划详情及测试计划表中对应测试计划信息
                        for (let key in res.data.planDataUpdated) {
                            if (key in this.planRow) {
                                this.planRow[key] =
                                    res.data.planDataUpdated[key];
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
};
</script>

<style scoped>

</style>
