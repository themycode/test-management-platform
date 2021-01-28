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
                <el-form-item label="类型">
                    <el-select v-model="queryForm.type" clearable style="width: 100px;">
                        <el-option
                            v-for="item in typeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
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
                <el-button :size="buttonSize" @click="addAccount">新增账号</el-button>
                <el-button
                    :size="buttonSize"
                    @click="deleteRows($api.msgPushAccount.deleteAccounts)"
                >删除账号</el-button>
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
                prop="account"
                label="账号"
                header-align="center"
                align="left"
                min-width="200px"
            ></el-table-column>
            <el-table-column
                prop="type"
                label="类型"
                header-align="center"
                align="center"
                width="70px"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="描述"
                header-align="center"
                align="center"
                min-width="200px"
            ></el-table-column>
            <el-table-column
                prop="groups"
                label="归属组别"
                header-align="center"
                min-width="180px"
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
                    <el-button size="mini" @click="bindGroup(scope.$index, scope.row)">
                        <i class="fa fa-plus" aria-hidden="true"></i>关联组别
                    </el-button>
                </template>
            </el-table-column>

            <el-table-column
                prop="status"
                label="状态切换"
                width="80px"
                header-align="center"
                align="center"
            >
                <template slot-scope="scope">
                    <el-button
                        v-if="scope.row.isActive"
                        size="mini"
                        @click="toggleAccountStatus(scope.$index, scope.row)"
                    >禁用</el-button>
                    <el-button
                        v-else
                        size="mini"
                        @click="toggleAccountStatus(scope.$index, scope.row)"
                    >启用</el-button>
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
                label="修改人"
                width="100px"
                header-align="center"
                align="center"
            ></el-table-column>
            <el-table-column
                prop="updateTime"
                label="修改时间"
                width="160px"
                header-align="center"
                align="center"
            ></el-table-column>

            <el-table-column label="操作" align="left" width="160px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editAccount(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.msgPushAccount.deleteAccount)"
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

        <!-- 新增\修改账号对话框 -->
        <msg-push-account-dlg
            v-if="accountDialogVisible"
            :dialogVisible.sync="accountDialogVisible"
            :dialogTitle="accountDialogTitle"
            :tableData="tableData"
            :dialogFormData="accountData"
            :row="row"
            :typeOptions="typeOptions"
            :statusOptions="statusOptions"
        ></msg-push-account-dlg>

        <!-- 关联组别对话框 -->
        <bind-sys-group-dialog
            v-if="bindGroupDialogVisible"
            :dialogVisible.sync="bindGroupDialogVisible"
            :row="row"
        ></bind-sys-group-dialog>
    </div>
</template>

<script>
import MsgPushAccountDlg from "./MsgPushAccount/MsgPushAccountDlg";
import BindSysGroupDialog from "./MsgPushAccount/BindSysGroupDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    data() {
        return {
            // 查询表单
            queryForm: {
                account: "", // 账号名称
                type: "", // 账号类型
                isActive: "", // 账号状态
            },
            accountData: null, // 存放新增，修改时的数据
            accountDialogVisible: false, // 标识新建\编辑账号对话框是否可见，true - 可见， false - 不可见
            accountDialogTitle: "", // 账号对话框标题

            bindGroupDialogVisible: false, // 标识分关联组别对话框是否可见
            statusOptions: [
                { label: "启用", value: true },
                { label: "禁用", value: false },
            ],
            typeOptions: [
                { label: "邮箱号", value: "邮箱号" },
                { label: "手机号", value: "手机号" },
                { label: "钉钉号", value: "钉钉号" },
            ],
        };
    },
    components: {
        MsgPushAccountDlg,
        BindSysGroupDialog,
    },
    methods: {
        addAccount() {
            if (!this.accountDialogVisible) {
                this.accountData = {
                    account: "", //账号名称
                    type: "",
                    desc: "", // 账号名称
                    isActive: true, // 是否启用
                };

                this.accountDialogVisible = true;
                this.accountDialogTitle = "新增账号";
            }
        },
        editAccount(index, row) {
            if (!this.accountDialogVisible) {
                this.accountData = {
                    id: row.id,
                    account: row.account,
                    type: row.type,
                    desc: row.desc, // 账号名称
                    isActive: row.isActive, // 是否启用
                };

                this.row = row;
                this.accountDialogVisible = true;
                this.accountDialogTitle = "修改账号";
            }
        },
        // 启用\禁用账号
        toggleAccountStatus(index, row) {
            let targetStatus = row.isActive ? "禁用" : "启用";
            this.$confirm("确定要" + targetStatus + "该账号吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.msgPushAccount
                        .toggleAccountStatus({
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
        bindGroup(index, row) {
            if (!this.bindGroupDialogVisible) {
                this.bindGroupDialogVisible = true;
                this.row = row;
            }
        },
        deleteRelatedGroup(row, group) {
            this.$confirm("确定要取消关联该组别吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    this.$api.msgPushAccount
                        .deleteRelatedGroup({
                            accountId: row.id,
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
        // 清空状态时，赋值isActive=""，方便后台查询处理,否则前端不会传递isActive参数给后台
        clearStatus() {
            this.queryForm.isActive = "";
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.msgPushAccount.getAccounts;
        this.queryRows();
    },
};
</script>

<style lang="scss">
</style>
