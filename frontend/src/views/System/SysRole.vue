<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="角色名称">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入角色名称"
                        clearable
                        style="width:230px"
                    ></el-input>
                </el-form-item>

                <el-form-item label="状态">
                    <el-select
                        v-model="queryForm.isActive"
                        clearable
                        @clear="clearStatus"
                        style="width: 100px;"
                    >
                        <el-option
                            v-for="item in statusOptions"
                            :key="item.value"
                            :value="item.value"
                            :label="item.label"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="queryRows('clickQuery')">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addRole">新增角色</el-button>
                <el-button
                    :size="buttonSize"
                    @click="deleteRows($api.sysRole.batchDeleteSysRole)"
                >删除角色</el-button>
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
            @row-click="clickRow"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="60px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="角色名称"
                show-overflow-tooltip
                header-align="center"
                align="left"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="角色描述"
                show-overflow-tooltip
                header-align="center"
                align="left"
            ></el-table-column>
            <el-table-column
                prop="isActive"
                label="是否启用"
                width="80px"
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">
                    <span v-if="scope.row.isActive">启用</span>
                    <span v-else>禁用</span>
                </template>
            </el-table-column>
            <el-table-column
                prop="createrName"
                label="创建人"
                width="100px"
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
                width="100px"
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
            <el-table-column label="操作" align="left" width="290px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="bindMenu(scope.$index, scope.row)">关联菜单</el-button>
                    <el-button size="mini" @click="editRole(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        v-if="scope.row.isActive"
                        size="mini"
                        @click="toggleRoleStatus(scope.$index, scope.row)"
                    >禁用</el-button>
                    <el-button
                        v-else
                        size="mini"
                        @click="toggleRoleStatus(scope.$index, scope.row)"
                    >启用</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.sysRole.deleteSysRole)"
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

        <!-- 新增修改角色对话框 -->
        <sys-role-dialog
            v-if="roleDialogVisible"
            :dialogVisible.sync="roleDialogVisible"
            :dialogTitle="roleDialogTitle"
            :tableData="tableData"
            :dialogFormData="roleData"
            :row="row"
            :statusOptions="statusOptions"
        ></sys-role-dialog>

        <!-- 关联菜单资源对话框 -->
        <bind-menu-dialog
            v-if="bindMenuDialogVisible"
            :dialogVisible.sync="bindMenuDialogVisible"
            :roleID="roleID"
        ></bind-menu-dialog>
    </div>
</template>

<script>
import SysRoleDialog from "./SysRole/SysRoleDialog";
import BindMenuDialog from "./SysRole/BindMenuDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    data() {
        return {
            // 查询表单
            queryForm: {
                name: "", // 角色名称
                isActive: "", // 角色状态
            },
            roleData: null, // 存放新增、修改的角色数据
            roleDialogVisible: false, // 标识新建\编辑测试角色对话框是否可见，true - 可见， false - 不可见
            roleDialogTitle: "", // 测试角色对话框标题
            bindMenuDialogVisible: false, // 标识绑定资源对话框是否可见
            roleID: 0, // 存放当前点击的测试角色id
            statusOptions: [
                { label: "启用", value: true },
                { label: "禁用", value: false },
            ],
        };
    },
    components: {
        SysRoleDialog,
        BindMenuDialog,
    },
    methods: {
        // 新增角色
        addRole() {
            if (!this.roleDialogVisible) {
                this.roleData = {
                    name: "", // 角色名称
                    desc: "", // 角色描述
                    isActive: true, // 是否启用
                };

                this.roleDialogVisible = true;
                this.roleDialogTitle = "新增角色";
            }
        },
        // 编辑角色
        editRole(index, row) {
            if (!this.roleDialogVisible) {
                this.roleData = {
                    id: row.id,
                    name: row.name, // 角色名称
                    desc: row.desc, // 角色描述
                    isActive: row.isActive, // 是否启用
                };
                this.roleDialogVisible = true;
                this.roleDialogTitle = "修改角色";
                this.row = row;
            }
        },
        // 启用角色
        toggleRoleStatus(index, row) {
            let targetStatus = row.isActive ? "禁用" : "启用";
            this.$confirm("确定要" + targetStatus + "该角色吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.sysRole
                        .updateSysRole({
                            id: row.id,
                            isActive: !row.isActive,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message({
                                    message: res.msg,
                                    type: "success",
                                });

                                for (let key in res.data) {
                                    if (key in row) {
                                        // 以防后续表单字段有变更，仅保存对应key的值
                                        row[key] = res.data[key];
                                    }
                                }
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                        });
                })
                .catch(() => {});
        },
        // 打开关联测试用例对话框
        bindMenu(index, row) {
            if (!this.bindMenuDialogVisible) {
                this.bindMenuDialogVisible = true;
                this.roleID = row.id;
            }
        },
        // 点击表格记录行
        clickRow(row, column, event) {
            if (column.label != "操作") {
                this.editRole(undefined, row);
            }
        },
        // 清空状态时，赋值isActive=""，方便后台查询处理,否则前端不会传递isActive参数给后台
        clearStatus() {
            this.queryForm.isActive = "";
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.sysRole.getSysRoles;
        this.queryRows();
    },
};
</script>

<style lang="scss">
</style>
