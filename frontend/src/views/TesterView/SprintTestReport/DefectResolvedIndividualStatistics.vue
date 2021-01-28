<template>
    <div>
        <!-- 个人开发情况统计 -->
        <el-table
            :data="
                defectsResolvedIndividual.slice(
                    (currentPage - 1) * pageSize,
                    currentPage * pageSize
                )
            "
            border
            stripe
            highlight-current-row
        >
            <el-table-column
                prop="resolver"
                label="姓名"
                min-width="16%"
                show-overflow-tooltip
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="totalResolved"
                label="解决缺陷数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="totalRaised"
                label="引发缺陷数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="DI"
                label="缺陷密度值"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="deadly"
                label="致命缺陷数"
                show-overflow-tooltip
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="critical"
                label="严重缺陷总数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="general"
                label="一般缺陷数"
                min-width="14%"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                label="轻微缺陷数"
                prop="minor"
                min-width="14%"
                header-align="center"
                align="center"
            >
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
    props: ["defectsResolvedIndividual"],
    data() {
        return {
            totalRows: this.defectsResolvedIndividual.length,
            pageSizes: [10, 20, 30, 40, 50, 80, 100, 150], //每页显示记录数选择器的选项设置
            pageSize: 10, // 表格默认每页显示的记录数
            currentPage: 1, // 当前页页码
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
        },
    },
};
</script>