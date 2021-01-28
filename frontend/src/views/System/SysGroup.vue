<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="组别">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入组别名称"
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
                <el-button :size="buttonSize" @click="addSysGroup">新增组别</el-button>
                <el-button
                    :size="buttonSize"
                    @click="deleteRows($api.sysGroup.deleteSysGroups)"
                >删除组别</el-button>
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
            >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="60px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="组别名称"
                header-align="center"
                align="left"
                min-width="150px"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="组别描述"
                header-align="center"
                align="center"
                min-width="150px"
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
                    <el-button size="mini" @click="editSysGroup(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.sysGroup.deleteSysGroup)"
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

        <!-- 新增\修改组别对话框 -->
        <sys-group-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :row="row"
            :dialogFormData="groupData"
        ></sys-group-dialog>

    </div>
</template>

<script>
import SysGroupDialog from "./SysGroup/SysGroupDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    data() {
        return {
            // 查询表单
            queryForm: {
                name: "", // 组别名称
            },
            groupData: null, // 存放组别记录行数据
            dialogVisible: false, // 标识新建\编辑组别对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 组别对话框标题
            relatedGroupDlgVisible: false, // 标识分关联账号对话框是否可见
            idOfSetTimeOut: null,
        };
    },
    components: {
        SysGroupDialog
    },
    methods: {
        addSysGroup() {
            if (!this.dialogVisible) {
                this.groupData = {
                    name: "", //组别名称
                    desc: "", // 组别描述
                };

                this.dialogVisible = true;
                this.dialogTitle = "新增组别";
            }
        },
        editSysGroup(index, row) {
            if (!this.dialogVisible) {
                this.row = row;

                this.groupData = {
                    id: row.id,
                    name: row.name,
                    desc: row.desc,
                };
                this.dialogVisible = true;
                this.dialogTitle = "修改组别";
            }
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.sysGroup.getSysGroups;
        this.queryRows();
    },
};
</script>

<style lang="scss" scoped>
</style>
