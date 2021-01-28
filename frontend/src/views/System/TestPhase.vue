<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addTestPhase">新增测试阶段</el-button>
                <el-button
                    :size="buttonSize"
                    @click="deleteRows($api.testPhase.deleteTestPhases)"
                >删除测试阶段</el-button>
            </el-button-group>
        </div>

        <!-- 表格 -->
        <el-table
            ref="myTable"
            :data="tableData"
            border
            stripe
            :empty-text="emptyText"
            :cell-class-name="getCellClassName"
            class="my-table"
            @selection-change="onSelectChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="测试阶段名称"
                header-align="center"
                align="left"
                min-width="200px"
            ></el-table-column>
            <el-table-column
                prop="default"
                label="是否默认阶段"
                header-align="center"
                align="center"
                min-width="200px"
            >
                <template slot-scope="scope">
                    <el-checkbox
                        v-model="scope.row.default"
                        @change="toggleDefaultTestPhase(scope.row)"
                    >{{scope.row.default?"是":"否"}}</el-checkbox>
                </template>
            </el-table-column>
            <el-table-column
                prop="code"
                label="唯一编码"
                header-align="center"
                align="center"
                min-width="200px"
            ></el-table-column>
            <el-table-column
                prop="order"
                label="阶段顺序"
                header-align="center"
                align="center"
                min-width="80px"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="阶段描述"
                header-align="center"
                align="left"
                min-width="250px"
            ></el-table-column>
            <el-table-column
                prop="createrName"
                label="创建人"
                min-width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="createTime"
                label="创建时间"
                min-width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updaterName"
                label="修改人"
                min-width="95px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updateTime"
                label="修改时间"
                min-width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column label="操作" align="left" width="150px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editTestPhase(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.testPhase.deleteTestPhase)"
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
        <test-phase-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :dialogFormData="testPhaseData"
            :row="row"
            :total.sync="total"
            :pageSize="pageSize"
        ></test-phase-dialog>
    </div>
</template>

<script>
import TestPhaseDialog from "./TestPhase/TestPhaseDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    data() {
        return {
            testPhaseData: null, // 存放新增，修改时的环境数据
            dialogVisible: false, // 标识新建\编辑迭代对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 迭代对话框标题
            checkTestPhase: false, // 是否勾选对应测试阶段
        };
    },
    components: {
        TestPhaseDialog,
    },
    methods: {
        addTestPhase() {
            if (!this.dialogVisible) {
                this.testPhaseData = {
                    name: "",
                    code: "",
                    order: "",
                    desc: "",
                    default: false,
                };

                this.dialogVisible = true;
                this.dialogTitle = "新增测试阶段";
            }
        },
        editTestPhase(index, row) {
            if (!this.dialogVisible) {
                this.testPhaseData = {
                    id: row.id,
                    name: row.name,
                    code: row.code,
                    order: row.order,
                    desc: row.desc,
                    default: row.default,
                };
                this.row = row;
                this.dialogVisible = true;
                this.dialogTitle = "修改测试阶段";
            }
        },
        toggleDefaultTestPhase(row) {
            let data = {
                id: row.id,
                default: row.default,
            };

            this.$api.testPhase
                .updateTestPhase(data)
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                    
                        this.queryRows();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error("修改失败： " + res);
                });
        },
    },

    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.testPhase.getTestPhases;
        this.queryRows();
    },
};
</script>

<style lang="scss">
</style>
