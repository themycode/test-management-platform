<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="账号">
                    <el-input
                        v-model="queryForm.account"
                        placeholder="请输入账号名称"
                        clearable
                        style="width:230px"
                    ></el-input>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入姓名"
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
                            :label="item.label"
                            :value="item.value"
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
                <el-button :size="buttonSize" @click="addUser">新增用户</el-button>
                <el-button :size="buttonSize" @click="deleteRows">删除用户</el-button>
            </el-button-group>
        </div>
        <!-- 表格 -->
        <el-table
            ref="myTable"
            :data="tableData"
            :empty-text="emptyText"
            border
            stripe
            class="my-table"
            @selection-change="onSelectChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="account"
                label="账号"
                show-overflow-tooltip
                header-align="center"
                align="left"
                min-width="120px"
            ></el-table-column>
            <el-table-column
                prop="name"
                label="姓名"
                show-overflow-tooltip
                header-align="center"
                align="center"
                width="95px"
            ></el-table-column>
            <el-table-column
                prop="email"
                label="邮箱"
                show-overflow-tooltip
                header-align="center"
                align="left"
                min-width="230px"
            ></el-table-column>
            <el-table-column
                prop="mobile"
                label="手机号"
                header-align="center"
                align="center"
                width="115px"
            ></el-table-column>
            <el-table-column
                prop="jobNumber"
                label="工号"
                show-overflow-tooltip
                header-align="center"
                align="left"
                width="110px"
            ></el-table-column>
            <el-table-column
                prop="roles"
                label="所属角色"
                header-align="center"
                min-width="210px"
                align="left"
            >
                <template slot-scope="scope">
                    <span v-for="role in scope.row.roles" :key="role.id" @click.stop>
                        {{ role.name }}
                        <i
                            class="el-icon-close"
                            aria-hidden="true"
                            @click.prevent="deleteRelatedRole(scope.row, role)"
                        >;&nbsp;&nbsp;</i>
                    </span>
                    <el-button
                        size="mini"
                        @click="bindRole(scope.$index, scope.row)"
                        class="row-operation-btn"
                    >
                        <i class="fa fa-plus" aria-hidden="true"></i>分配角色
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column
                prop="groups"
                label="归属组别"
                header-align="center"
                min-width="210px"
                align="left"
            >
                <template slot-scope="scope">
                    <span v-for="group in scope.row.groups" :key="group.id" @click.stop>
                        {{ group.name }}
                        <i
                            class="el-icon-close"
                            aria-hidden="true"
                            @click.prevent="deleteRelatedGroup(scope.row, group)"
                        >;&nbsp;&nbsp;</i>
                    </span>
                    <el-button
                        size="mini"
                        @click="bindGroup(scope.$index, scope.row)"
                        class="row-operation-btn"
                    >
                        <i class="fa fa-plus" aria-hidden="true"></i>关联组别
                    </el-button>
                </template>
            </el-table-column>

            <el-table-column
                prop="isActive"
                label="状态切换"
                width="80px"
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">
                    <el-button
                        v-if="scope.row.isActive"
                        size="mini"
                        @click="toggleUserStatus(scope.$index, scope.row)"
                    >禁用</el-button>
                    <el-button
                        v-else
                        size="mini"
                        @click="toggleUserStatus(scope.$index, scope.row)"
                    >启用</el-button>
                </template>
            </el-table-column>
            <el-table-column
                prop="createTime"
                label="创建时间"
                width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="lastLoginTime"
                label="最后登录时间"
                width="160px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column label="操作" align="left" width="250px" class="operation-col">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editUser(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" @click="bindAccount(scope.$index, scope.row)">关联账号</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="resetPasswd(scope.$index, scope.row)"
                    >重置密码</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteOneRow(scope.$index, scope.row)"
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

        <!-- 新增\修改用户对话框 -->
        <sys-user-dialog
            v-if="userDialogVisible"
            :dialogVisible.sync="userDialogVisible"
            :dialogTitle="userDialogTitle"
            :tableData="tableData"
            :dialogFormData="userData"
            :operateOneSelf="operateOneSelf"
            :row="row"
            :statusOptions="statusOptions"
        ></sys-user-dialog>

        <!-- 分配角色对话框 -->
        <bind-role-dialog
            v-if="bindRoleDialogVisible"
            :dialogVisible.sync="bindRoleDialogVisible"
            :row="row"
        ></bind-role-dialog>

        <!-- 关联组别对话框 -->
        <bind-group-dialog
            v-if="bindGroupDialogVisible"
            :dialogVisible.sync="bindGroupDialogVisible"
            :row="row"
        ></bind-group-dialog>

        <!-- 关联账号对话框 -->
        <related-account-dlg
            v-if="relatedAccountDlgVisible"
            :dialogVisible.sync="relatedAccountDlgVisible"
            :userId="row.id"
        ></related-account-dlg>
    </div>
</template>

<script>
import { elTableMixin } from "@/common/mixins/elTableMixin";
import SysUserDialog from "./SysUser/SysUserDialog";
import BindRoleDialog from "./SysUser/BindRoleDialog";
import BindGroupDialog from "./SysUser/BindGroupDialog";
import RelatedAccountDlg from "./SysUser/RelatedAccountDialog";

import { mapState } from "vuex";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],

    data() {
        return {
            // 查询表单
            queryForm: {
                account: "", // 账号名称
                name: "", // 用户名称
                isActive: true, // 用户状态
            },
            userData: null, // 存放新增、修改时的用户数据
            operateOneSelf: false, // 标识是否操作用户自己的记录
            userDialogVisible: false, // 标识新建\编辑用户对话框是否可见，true - 可见， false - 不可见
            userDialogTitle: "", // 用户对话框标题

            bindRoleDialogVisible: false, // 标识分配角色对话框是否可见
            bindGroupDialogVisible: false, // 标识分关联组别对话框是否可见
            relatedAccountDlgVisible: false, // 标识关联账号对话框是否可见
            statusOptions: [
                { label: "启用", value: true },
                { label: "禁用", value: false },
            ],
        };
    },
    components: {
        SysUserDialog,
        BindRoleDialog,
        BindGroupDialog,
        RelatedAccountDlg,
    },
    methods: {
        addUser() {
            if (!this.userDialogVisible) {
                this.userData = {
                    account: "", //账号名称
                    name: "", // 用户名称
                    email: "", // 用户邮箱
                    mobile: "", // 手机号
                    jobNumber:"", // 工号
                    isActive: true, // 是否启用
                };

                this.operateOneSelf = false;

                this.userDialogVisible = true;
                this.userDialogTitle = "新增用户";
            }
        },
        editUser(index, row) {
            if (!this.userDialogVisible) {
                this.userData = {
                    id: row.id,
                    account: row.account,
                    name: row.name,
                    email: row.email,
                    mobile: row.mobile,
                    jobNumber:row.jobNumber, 
                    isActive: row.isActive,
                };

                if (this.userId == row.id) {
                    this.operateOneSelf = true; // 操作用户自身记录
                } else {
                    this.operateOneSelf = false;
                }

                this.row = row;
                this.userDialogVisible = true;
                this.userDialogTitle = "修改用户";
            }
        },
        // 逐条删除用户
        deleteOneRow(index, row) {
            if (row.isSuperuser) {
                this.$alert("不能删除超级管理员", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (this.userId == row.id) {
                this.$alert("用户不能删除自身账号", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:delete"
                    )
                ) {
                    this.$alert("抱歉，您没有删除用户权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            this.deleteRow(index, row, this.$api.sysUser.deleteSysUser);
        },

        // 批量删除用户
        deleteRows() {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:delete"
                    )
                ) {
                    this.$alert("抱歉，您没有删除用户权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            this.$confirm("确定要删除选中用户吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    if (!this.rowsSelected.length) {
                        this.$alert("未选择用户，请勾选至少一条用户", "提示", {
                            confirmButtonText: "确定",
                        });
                        return;
                    }
                    let rowIds = []; // 存放用户ID
                    for (let i = 0; i < this.rowsSelected.length; i++) {
                        if (this.rowsSelected[i].isSuperuser) {
                            this.$message.info(
                                "账号" +
                                    this.rowsSelected[i].account +
                                    "为超级管理员，不能删除，已自动为您跳过"
                            );
                            continue;
                        }

                        if (this.rowsSelected[i].id == this.userId) {
                            this.$message.info(
                                this.rowsSelected[i].account +
                                    "为当前用户账号，不能删除，已自动为您跳过"
                            );
                            continue;
                        }
                        rowIds.push(this.rowsSelected[i].id);
                    }

                    if (!rowIds.length) {
                        this.$message({
                            message: "操作完成",
                            type: "success",
                        });
                        return;
                    }

                    // 发送删除请求
                    this.$api.sysUser
                        .deleteSysUsers({
                            rowIds: rowIds,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);
                                // 减少记录总数
                                this.total =
                                    this.total - this.rowsSelected.length;

                                for (
                                    let i = 0;
                                    i < this.rowsSelected.length;
                                    i++
                                ) {
                                    this.tableData.splice(
                                        this.tableData.indexOf(
                                            this.rowsSelected[i]
                                        ),
                                        1
                                    );
                                }

                                if (!this.tableData.length && this.total != 0) {
                                    // 如果本页数据都被删除

                                    let totalPages = Math.ceil(
                                        this.total / this.pageSize
                                    );

                                    if (this.currentPage > totalPages) {
                                        // 当前页位于最后一页，翻页到前一页
                                        this.currentPage -= 1;
                                    } else {
                                        // 直接刷新当前页
                                    }
                                    this.queryRows();
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
        // 启用\禁用用户
        toggleUserStatus(index, row) {
            this.row = row;

            if (this.userId == row.id && row.isActive) {
                this.$alert("您不能禁用自身账号", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:toggleStatus"
                    )
                ) {
                    this.$alert("抱歉，您没有修改用户状态的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            let targetStatus = row.isActive ? "禁用" : "启用";
            this.$confirm("确定要" + targetStatus + "该用户吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.sysUser
                        .toggleUserStatus({
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
        bindRole(index, row) {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:bindRole"
                    )
                ) {
                    this.$alert("抱歉，您没有分配角色的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            if (!this.bindRoleDialogVisible) {
                this.bindRoleDialogVisible = true;
                this.row = row;
            }
        },
        deleteRelatedRole(row, role) {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:deleteRole"
                    )
                ) {
                    this.$alert("抱歉，您没有删除用户角色的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            this.$confirm("确定要取消关联该角色吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.sysUser
                        .deleteRelatedRole({
                            userId: row.id,
                            roleId: role.id,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message({
                                    message: res.msg,
                                    type: "success",
                                });

                                const index = row.roles.indexOf(role);
                                if (index != -1) {
                                    row.roles.splice(index, 1);
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
        bindGroup(index, row) {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:bindGrp"
                    )
                ) {
                    this.$alert("抱歉，您没有关联用户组别的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }
            if (!this.bindGroupDialogVisible) {
                this.bindGroupDialogVisible = true;
                this.row = row;
            }
        },
        deleteRelatedGroup(row, group) {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:deleteGrp"
                    )
                ) {
                    this.$alert("抱歉，您没有删除用户组别的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            this.$confirm("确定要取消关联该组别吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.sysUser
                        .deleteRelatedGroup({
                            userId: row.id,
                            groupId: group.id,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message({
                                    message: res.msg,
                                    type: "success",
                                });

                                const index = row.groups.indexOf(group);
                                if (index != -1) {
                                    row.groups.splice(index, 1);
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
        bindAccount(index, row) {
            if (!this.isSuperuser) {
                if (this.userId != row.id) {
                    this.$alert("抱歉，您只能操作自己的账号", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }
            if (!this.relatedAccountDlgVisible) {
                this.relatedAccountDlgVisible = true;
                this.row = row;
            }
        },
        // 清空状态时，赋值isActive=""，方便后台查询处理
        clearStatus() {
            this.queryForm.isActive = "";
        },
        resetPasswd(index, row) {
            if (!this.isSuperuser) {
                if (
                    !this.$customUtils.permission.hasPermission(
                        "sys:user:resetPasswd"
                    )
                ) {
                    this.$alert("抱歉，您没有重置用户密码的权限", "提示", {
                        confirmButtonText: "确定",
                    });
                    return;
                }
            }

            this.$confirm("确定重置密码吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.sysUser
                        .resetPasswd({
                            userId: row.id,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message.success(res.msg);
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
        getUserPersonalInfo() {
            new Promise(this.$customUtils.userInfo.getCurrentUserInfo)
                .then((res) => {
                    this.$store.commit("setUserId", res.data.id);
                    this.$store.commit("setIsSuperUser", res.data.isSuperuser); // 保存是否超级管理员用户标识
                })
                .catch((err) => {
                    this.$message.error(res.msg || res.message);
                });
        },
    },
    created() {
        if (this.isSuperuser == undefined) {
            this.getUserPersonalInfo();
        }
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.sysUser.getSysUsers;
        this.queryRows();
    },
    computed: {
        ...mapState({
            isSuperuser: (state) => state.user.isSuperuser,
            userId: (state) => state.user.userId,
        }),
    },
};
</script>

<style lang="scss" scoped>
.el-button {
    margin-left: 1px;
    margin-right: 0px;
    padding-left: 5px;
    padding-right: 5px;
}

/deep/ .cell {
    padding-left: 10px;
    padding-right: 10px;
}
</style>
