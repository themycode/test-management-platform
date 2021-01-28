<template>
    <div>
        <el-dialog
            title="提示"
            width="40%"
            :visible="dialogVisible"
            :append-to-body="true"
            :show-close="false"
        >
            <div class="my-dialog-body">
                <div>确定要删除该测试集吗？ 删除该测试集将会删除其所有子测试集</div>

                <div v-if="suiteTypeForDel == 'sprint'">
                    <br />
                    <div>
                        <el-radio v-model="delBaseSuitesCascade" label="1">级联删除关联的基线测试集</el-radio>
                        <el-radio v-model="delBaseSuitesCascade" label="2">不删除关联的基线测试集</el-radio>
                    </div>
                    <br />
                    <div>备注：如果关联的基线测试集下存在用例，则跳过删除该基线测试集及其父测试集</div>
                </div>
            </div>

            <div class="dialog-footer">
                <el-button @click="cancel">取 消</el-button>
                <el-button type="primary" @click="confirm">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    props: ["dialogVisible", "suiteIdForDel", "suiteTypeForDel"],
    data() {
        return {
            delBaseSuitesCascade: "1", // 级联删除基线测试套件
        };
    },
    methods: {
        closeDialog() {
            this.$emit("update:dialogVisible", false); // 关闭对话框
        },
        cancel() {
            this.closeDialog();
        },
        confirm() {
            this.$api.sprintCaseSuite
                .deleteSprintCaseSuite({
                    suiteId: this.suiteIdForDel,
                    type: this.suiteTypeForDel,
                    delBaseSuitesCascade: this.delBaseSuitesCascade,
                })
                .then((res) => {
                    if (res.success) {
                        this.$parent.removeCurrNodeClicked();
                        this.$message.success(res.msg);
                    } else {
                        this.$message.error(res.msg);
                    }

                    this.closeDialog();
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
    },
};
</script>

<style>

</style>
