<template>
    <el-dialog
        title="关联用例"
        width="80%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
        ref="bindCaseDialog"
    >
        <div class="my-dialog-body">
            <sprint-case-suite-tree
                class="sprint-case-suite-tree"
                :sprintID="planRow.sprintId"
                :productID="planRow.productId"
                :currentModule="currentModule"
                ref="leftElement"
            ></sprint-case-suite-tree>

            <sprint-case-table
                class="sprint-case-table"
                :currentModule="currentModule"
                :testplanId="planRow.id"
                :productID="planRow.productId"
                :sprintID="planRow.sprintId"
                ref="rightElement"
            ></sprint-case-table>
        </div>
        <div class="dialog-footer">
            <el-button type="primary" @click="bindCases" size="small">关联选中</el-button>
            <el-button @click="closeDialog" size="small">完成</el-button>
        </div>
    </el-dialog>
</template>

<script>
import SprintCaseSuiteTree from "../SprintCase/SprintCaseSuiteTree";
import SprintCaseTable from "../SprintCase/SprintCaseTable";
import { horizontalDragMixin } from "@/common/mixins/horizontalDragMixin";
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "planRow"],
    components: {
        SprintCaseSuiteTree,
        SprintCaseTable,
    },
    mixins: [horizontalDragMixin, elDialogMixin],
    data() {
        return {
            currentModule: "bindPlanAndCaseDialog", //用于标识测试当前在哪个页面模块操作用例集树&测试用例表组件
            caseBinding: false, // 标识是否正在执行用例绑定//防极短时间内重复点击用,
        };
    },
    methods: {
        //关联测试用例
        bindCases() {
            let rowsSelected = this.$refs.rightElement.$refs.myTable.selection;

            if (this.caseBinding) {
                this.$message.warning("正在执行关联用例操作，请稍后再试");
                return;
            }

            this.caseBinding = true;
            this.$api.sprintTestPlan
                .bindTestCases({
                    planId: this.planRow.id,
                    guidsOfRelatedOldCases: this.$refs.rightElement
                        .guidsOfRelatedOldCases,
                    rowsSelected: rowsSelected,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        // 更新计划相关信息
                        this.$nextTick(() => {
                            for (let key in res.data) {
                                if (key in this.planRow) {
                                    this.planRow[key] = res.data[key];
                                }
                            }
                        });
                    } else {
                        this.$message.error(res.msg);
                    }
                    this.caseBinding = false;
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                    this.caseBinding = false;
                });
        },
    },
    mounted() {
        this.$refs.bindCaseDialog.$el.addEventListener(
            "mousedown",
            this.mousedown,
            false
        );
        this.$refs.bindCaseDialog.$el.addEventListener(
            "mousemove",
            this.mousemove,
            false
        );
        this.$refs.bindCaseDialog.$el.addEventListener(
            "mouseup",
            this.mouseup,
            false
        );
    },

    beforeDestroy() {
        this.$refs.bindCaseDialog.$el.removeEventListener(
            "mousedown",
            this.mousedown
        );
        this.$refs.bindCaseDialog.$el.removeEventListener(
            "mousemove",
            this.mousemove
        );
        this.$refs.bindCaseDialog.$el.removeEventListener(
            "mouseup",
            this.mouseup
        );
    },
};
</script>

<style lang="scss" scoped>
.my-dialog-body {
    height: 500px;
    padding-left: 0px;
    padding-right: 0px;
}

.sprint-case-suite-tree {
    position: absolute;
    top: 0px; // 顶部筛选栏占用高度42 + 5px
    bottom: 0px;
    padding: 0px;
    width: 320px;
    margin-right: 2px;
    border-right: solid;
    border-right-color: rgba(172, 167, 167, 1);
    border-right-width: 1px;
}

// 测试用例表样式
.sprint-case-table {
    position: absolute;
    left: 322px; // 左侧套件树占用宽度
    right: 0px;
    top: 0px;
    bottom: 0px;
    border-left: solid;
    border-left-color: rgba(172, 167, 167, 1);
    border-left-width: 1px;
}

.dialog-footer {
    text-align: right !important;
    position: relative;
}
</style>
