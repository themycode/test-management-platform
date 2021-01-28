<template>
    <div class="view-wrapper">
        <!-- 迭代用例测试集树 -->
        <sprint-case-suite-tree
            class="testplan-casesuite-tree"
            :sprintID="sprintID"
            :productID="planRow.productId"
            :planID="planRow.id"
            :currentModule="currentModule"
            ref="leftElement"
        ></sprint-case-suite-tree>

        <!-- 同用例树，测试计划关联的测试用例列表(包含操作按钮及表单查询组件) -->
        <test-plan-case-table
            class="testplan-case-table"
            ref="rightElement"
            :currentModule="currentModule"
            :planRow="planRow"
        ></test-plan-case-table>
    </div>
</template>

<script>
import SprintCaseSuiteTree from "../SprintCase/SprintCaseSuiteTree";
import TestPlanCaseTable from "../SprintTestPlan/TestPlanCaseTable";
import { horizontalDragMixin } from "@/common/mixins/horizontalDragMixin";

export default {
    props: ["sprintID", "planRow"],
    components: {
        SprintCaseSuiteTree,
        TestPlanCaseTable,
    },
    mixins: [horizontalDragMixin],
    data() {
        return {
            currentModule: "planCaseListTab", //用于标识测试当前在哪个页面模块操作用例集树组件
        };
    },
    methods: {},
    mounted() {
        document.body.addEventListener("mousedown", this.mousedown, false);
        document.body.addEventListener("mousemove", this.mousemove, false);
        document.body.addEventListener("mouseup", this.mouseup, false);
    },
    beforeDestroy() {
        document.body.removeEventListener("mousedown", this.mousedown);
        document.body.removeEventListener("mousemove", this.mousemove);
        document.body.removeEventListener("mouseup", this.mouseup);
    },
};
</script>

<style lang="scss" scoped>
// 测试集树样式
.testplan-casesuite-tree {
    position: absolute;
    top: 5px;
    bottom: 0px;
    padding: 0px;
    width: 320px;
    margin-left: 0px;
    margin-right: 0px;
    border-right: solid;
    border-right-color: rgba(172, 167, 167, 1);
    border-right-width: 1px;
}

// 测试用例表样式
.testplan-case-table {
    position: absolute;
    top: 5px;
    bottom: 0px;
    left: 322px;
    right: 0px;
    border-left: solid;
    border-left-color: rgba(172, 167, 167, 1);
    border-left-width: 1px;
}
</style>