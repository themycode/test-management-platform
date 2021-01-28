<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="产品名称">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入产品名称"
                        clearable
                        style="width:240px"
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
                <el-form-item label="产品负责人">
                    <el-input
                        v-model="queryForm.productOwner"
                        placeholder="请输入产品负责人"
                        clearable
                        style="width:230px"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="queryRows('clickQuery')">查询</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addProduct">新增产品</el-button>
                <el-button :size="buttonSize" @click="deleteRows($api.product.deleteProducts)">删除产品</el-button>
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
            <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column>
            <el-table-column
                prop="name"
                label="产品名称"
                header-align="center"
                align="left"
                min-width="180px"
                show-overflow-tooltip
            ></el-table-column>
            <el-table-column
                prop="status"
                label="状态"
                width="50px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="productOwner"
                label="产品负责人"
                width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="developOwner"
                label="研发负责人"
                width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="testOwner"
                label="测试负责人"
                width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="产品描述"
                header-align="center"
                align="center"
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
            <el-table-column label="操作" align="left" width="160px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editProduct(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.product.deleteProduct)"
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

        <!-- 新增\修改产品对话框 -->
        <product-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :statusOptions="statusOptions"
            :row="row"
            :dialogFormData="dialogData"
        ></product-dialog>
    </div>
</template>

<script>
import ProductDialog from "./Product/ProductDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    data() {
        return {
            // 查询表单
            queryForm: {
                name: "", // 产品名称
                status: "", // 产品状态
                productOwner: "", // 产品负责人
            },
            dialogData: null, // 存放新增，修改迭代用的数据
            statusOptions: [
                // 状态选项
                { label: "正常", value: "正常" },
                { label: "结束", value: "结束" },
            ],

            userName: "", // 存放当前迭代名称
            dialogVisible: false, // 标识新建\编辑迭代对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 迭代对话框标题
        };
    },
    components: {
        ProductDialog,
    },
    methods: {
        addProduct() {
            if (!this.dialogVisible) {
                this.dialogData = {
                    name: "", //产品名称
                    code: "", // 产品编码
                    status: "正常", // 产品状态
                    productOwner: { id: -1, name: "" }, // 产品负责人
                    developOwner: { id: -1, name: "" }, // 负责人
                    testOwner: { id: -1, name: "" }, // 测试负责人
                    desc: "", // 产品描述
                };
                this.dialogVisible = true;
                this.dialogTitle = "新增产品";
            }
        },
        editProduct(index, row) {
            if (!this.dialogVisible) {
                this.dialogData = {
                    id: row.id,
                    name: row.name,
                    code: row.code,
                    status: row.status,
                    productOwner: {
                        id: row.productOwnerId,
                        name: row.productOwner,
                    },
                    developOwner: {
                        id: row.developOwnerId,
                        name: row.developOwner,
                    },
                    testOwner: { id: row.testOwnerId, name: row.testOwner },
                    desc: row.desc,
                };
                this.row = row;
                this.dialogVisible = true;
                this.dialogTitle = "修改迭代项目";
            }
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.product.getProducts;
        this.queryRows();
    },
};
</script>

<style lang="scss" scoped>
</style>
