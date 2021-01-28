<template>
    <el-dialog
        title="关联账户"
        width="50%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <!-- 操作按钮 -->
            <div ref="actionBtn" style="text-align:right">
                <el-button type="primary" size="small" @click="addRelatedAccount">关联新账号</el-button>
            </div>

            <!-- 表格 -->
            <el-table :data="tableData" stripe highlight-current-row>
                <!--多选复选框-->
                <el-table-column
                    prop="id"
                    label="ID"
                    header-align="center"
                    align="center"
                    width="60px"
                ></el-table-column>
                <el-table-column
                    prop="account"
                    label="账号"
                    header-align="center"
                    align="left"
                    min-width="200px"
                ></el-table-column>

                <el-table-column
                    prop="platform"
                    label="平台"
                    header-align="center"
                    align="center"
                    min-width="150px"
                ></el-table-column>

                <el-table-column label="操作" align="center" width="150px">
                    <template slot-scope="scope">
                        <el-button
                            size="mini"
                            @click="editRelatedAccount(scope.$index, scope.row)"
                            class="row-operation-btn"
                        >编辑</el-button>

                        <el-button
                            size="mini"
                            type="danger"
                            @click="deleteRelatedAccount(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 新增\修改关联账号对话框 -->
            <bind-account-dialog
                v-if="bindAccountDialogVisible"
                :dialogVisible.sync="bindAccountDialogVisible"
                :dialogTitle="dialogTitle"
                :tableData="tableData"
                :row="row"
                :dialogFormData="accountData"
            ></bind-account-dialog>
        </div>
        <div class="dialog-footer" style="text-align:center">
            <el-button type="primary" @click="closeDialog">关闭</el-button>
        </div>
    </el-dialog>
</template>

<script>
import BindAccountDialog from "./BindAccountDialog";
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "userId"],
    components: {
        BindAccountDialog,
    },
    mixins: [elDialogMixin],

    data() {
        return {
            tableData: [], // 存放表数据
            accountData: null, // 存放新增，修改账号数据
            row: [], // 存放记录行完整数据
            bindAccountDialogVisible: false, // 标识新建\编辑关联账号对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 关联账号对话框标题
        };
    },
    methods: {
        queryRelatedAccounts() {
            // 向后台发送请求
            this.$api.sysUser
                .getRelatedAccounts({ userId: this.userId })
                .then((res) => {
                    if (res.success) {
                        this.tableData = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        addRelatedAccount() {
            if (!this.bindAccountDialogVisible) {
                this.accountData = {
                    userId: this.userId,
                    account: "", // 账号名称
                    password: "", // 账号密码
                    platform: "禅道",
                };

                this.bindAccountDialogVisible = true;
                this.dialogTitle = "新增关联账号";
            }
        },
        editRelatedAccount(index, row) {
            if (!this.bindAccountDialogVisible) {
                this.accountData = {
                    accountId: row.id,
                    userId: row.userId,
                    account: row.account, // 账号名称
                    password: row.password, // 账号密码
                    platform: row.platform,
                };
                this.row = row;
                this.bindAccountDialogVisible = true;
                this.dialogTitle = "修改关联账号";
            }
        },

        // 逐条删除记录
        deleteRelatedAccount(index, row) {
            this.$confirm("确定要删除该账号吗?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
                cancelButtonClass: "btn-custom-cancel",
            })
                .then(() => {
                    // 发送删除请求
                    this.$api.sysUser
                        .deleteRelatedAccount({
                            userId: row.userId,
                            accountId: row.id,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$message({
                                    message: res.msg,
                                    type: "success",
                                });

                                this.tableData.splice(index, 1); // 删除本行数据
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
    },
    created() {
        this.queryRelatedAccounts();
    },
};
</script>

<style lang="scss" scoped>
.dialog-footer {
    margin-top: 5px;
    text-align: right;
    position: relative;
}
</style>
