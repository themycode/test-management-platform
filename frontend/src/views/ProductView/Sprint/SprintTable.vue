<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="迭代名称">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入迭代名称"
                        clearable
                        style="width:240px"
                    ></el-input>
                </el-form-item>
                <el-form-item label="版本">
                    <el-input
                        v-model="queryForm.version"
                        placeholder="请输入版本"
                        clearable
                        style="width:230px"
                    ></el-input>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="queryForm.status" clearable style="width: 100px;">
                        <el-option
                            v-for="item in statusOptions"
                            :key="item.value"
                            :value="item.value"
                            :label="item.label"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="querySprints('clickQuery')">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addSprint">新增迭代</el-button>
                <el-button :size="buttonSize" @click="deleteRows($api.sprint.deleteSprints)">删除迭代</el-button>
            </el-button-group>
        </div>
        <!-- 表格 -->
        <el-table
            ref="myTable"
            :data="tableData"
            border
            stripe
            :empty-text="emptyText"
            class="my-table"
            :cell-class-name="getCellClassName"
            @selection-change="onSelectChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="迭代名称"
                header-align="center"
                align="left"
                show-overflow-tooltip
                min-width="180px"
            ></el-table-column>
            <el-table-column
                prop="version"
                label="版本"
                header-align="center"
                show-overflow-tooltip
                align="left"
                width="130px"
            ></el-table-column>
            <el-table-column
                prop="status"
                label="状态"
                width="80px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="beginTime"
                label="预估开始日期"
                width="110px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="endTime"
                label="预估结束日期"
                width="110px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="描述"
                header-align="center"
                align="left"
                min-width="250px"
                show-overflow-tooltip
            ></el-table-column>
            <el-table-column
                prop="createrName"
                label="创建人"
                width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="createTime"
                label="创建时间"
                width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updaterName"
                label="更新人"
                width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updateTime"
                label="更新时间"
                width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column label="操作" align="left" width="215px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editSprint(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" @click="copySprint(scope.$index, scope.row)">复制</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.sprint.deleteSprint)"
                    >删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination
            ref="tablePagination"
            class="table-pagination"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            layout="total, sizes, prev, pager, next"
            :hide-on-single-page="false"
            :total="total"
            prev-text="上一页"
            next-text="下一页"
            :current-page="currentPage"
            :page-sizes="pageSizes"
            :page-size="pageSize"
            :pager-count="pagerCount"
        ></el-pagination>

        <!-- 新增\修改迭代对话框 -->
        <sprint-dialog
            v-if="sprintDialogVisible"
            :dialogVisible.sync="sprintDialogVisible"
            :dialogTitle="sprintDialogTitle"
            :tableData="tableData"
            :statusOptions="statusOptions"
            :row="row"
            :dialogFormData="dialogFormData"
        ></sprint-dialog>
    </div>
</template>

<script>
import SprintDialog from "./SprintDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    props: ["productID"],
    data() {
        return {
            // 查询表单
            queryForm: {
                productId: this.productID,
                name: "", // 迭代名称
                version: "", // 版本
                status: "", // 迭代状态
            },
            dialogFormData: null, // 存放新增，修改迭代用的数据
            statusOptions: [
                // 状态选项
                { label: "未开始", value: "未开始" },
                { label: "进行中", value: "进行中" },
                { label: "已结束", value: "已结束" },
            ],

            sprintDialogVisible: false, // 标识新建\编辑迭代对话框是否可见，true - 可见， false - 不可见
            sprintDialogTitle: "", // 迭代对话框标题
        };
    },
    components: {
        SprintDialog,
    },
    methods: {
        querySprints(action) {
            if (!this.productID) {
                this.total = 0;
                this.tableData = [];
                return;
            }
            this.queryRows(action);
        },
        addSprint() {
            if (!this.productID) {
                this.$message.error("请先选择产品");
                return;
            }

            if (!this.sprintDialogVisible) {
                this.dialogFormData = {
                    name: "", //名称
                    version: "", // 版本
                    productId: this.productID,
                    beginTime: "", // 预估开始时间
                    endTime: "", // 预估结束时间
                    desc: "", // 迭代描述
                    status: "进行中", // 状态
                };

                this.sprintDialogVisible = true;
                this.sprintDialogTitle = "新增迭代";
            }
        },
        copySprint(index, row) {
            if (!this.sprintDialogVisible) {
                this.dialogFormData = {
                    name: row.name,
                    version: row.version,
                    productId: row.productId,
                    beginTime: row.beginTime,
                    endTime: row.endTime,
                    desc: row.desc,
                    status: row.status,
                };
                this.sprintDialogVisible = true;
                this.sprintDialogTitle = "复制迭代";
            }
        },
        editSprint(index, row) {
            if (!this.sprintDialogVisible) {
                this.dialogFormData = {
                    id: row.id,
                    productId: row.productId,
                    name: row.name,
                    version: row.version,
                    productId: row.productId,
                    beginTime: row.beginTime,
                    endTime: row.endTime,
                    desc: row.desc,
                    status: row.status,
                };
                this.row = row;
                this.sprintDialogVisible = true;
                this.sprintDialogTitle = "修改迭代";
            }
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.sprint.getSprints;
        this.querySprints();
    },
};
</script>

<style lang="scss" scoped>
</style>
