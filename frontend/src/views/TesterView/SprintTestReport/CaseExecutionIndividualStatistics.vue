<template>
    <div>
        <!-- 个人测试情况统计表 -->
        <el-table
            :data="caseExecutionIndividual.slice((currentPage-1)*pageSize,currentPage*pageSize)"
            border
            stripe
            highlight-current-row
        >
            <el-table-column
                prop="username"
                label="姓名"
                min-width="16%"
                show-overflow-tooltip
                header-align="center"
                align="center"
            ></el-table-column>
         
            <el-table-column
                prop="testcaseAssigned"
                label="分配用例数"
                show-overflow-tooltip
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="testcaseExecuted"
                label="执行用例数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="testcasePassed"
                label="通过用例数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                label="用例执行率"
                prop="testcaseExecutionRate"
                min-width="14%"
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">{{scope.row.testcaseExecutionRate}}%</template>
            </el-table-column>
            <el-table-column
                label="用例通过率"
                prop="testcasePassRate"
                min-width="14%"
                show-overflow-tooltip
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">{{scope.row.testcasePassRate}}%</template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination           
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            layout="total, sizes, prev, pager, next"
            :hide-on-single-page="false"
            :total="totalRows"
            prev-text="上一页"
            next-text="下一页"
            :current-page="currentPage"
            :page-sizes="pageSizes"
            :page-size="pageSize"
        ></el-pagination>
    </div>
</template>

<script>
export default {
    props: ["caseExecutionIndividual"],
    data() {
        return {
            totalRows: this.caseExecutionIndividual.length,
            pageSizes: [10, 20, 30, 40, 50, 80, 100, 150], //每页显示记录数选择器的选项设置
            pageSize: 10, // 表格默认每页显示的记录数
            currentPage: 1 // 当前页页码
        };
    },

    methods: {
        // 切换表格页面大小
        handleSizeChange(pageSize) {
            this.currentPage = 1;
            this.pageSize = pageSize;
        },
        // 翻页
        handleCurrentChange(currentPage) {
            this.currentPage = currentPage;
        }
    }
};
</script>