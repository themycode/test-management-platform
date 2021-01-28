<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="版本名称">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入版本名称"
                        clearable
                        style="width:240px"
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
                <el-button :size="buttonSize" @click="addVersion">新增项目版本</el-button>
                <el-button
                    :size="buttonSize"
                    @click="deleteRows($api.projectVersion.deleteProjectVersions)"
                >删除项目版本</el-button>
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
            @selection-change="onSelectChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="版本名称"
                header-align="center"
                align="left"
                min-width="250px"
                show-overflow-tooltip
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
                prop="sprint"
                label="关联迭代"
                header-align="center"
                align="left"
                min-width="200px"
                show-overflow-tooltip
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="版本描述"
                header-align="center"
                align="left"
                min-width="250px"
                show-overflow-tooltip
            ></el-table-column>
            <el-table-column
                prop="platformProjectVersion"
                label="关联项目版本"
                header-align="center"
                align="center"
                show-overflow-tooltip
                min-width="200px"
            >
                <template slot-scope="scope">
                    <el-link
                        type="primary"
                        v-if="scope.row.platformProjectVersionName"
                        @click="changeProjectVersionAssociated(scope.$index, scope.row)"
                    >
                        {{ scope.row.platformProjectVersionName }}
                        <i class="el-icon-edit"></i>
                    </el-link>
                    <el-button
                        v-else
                        size="mini"
                        @click="bindProjectVersion(scope.$index, scope.row)"
                    >
                        <i class="fa fa-plus" aria-hidden="true"></i>关联项目版本
                    </el-button>
                </template>
            </el-table-column>
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
            <el-table-column label="操作" align="left" width="150px">
                <template slot-scope="scope">
                    <el-button
                        size="mini"
                        @click="editVersion(scope.$index, scope.row)"
                        class="table-row-operation-btn"
                    >编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.projectVersion.deleteProjectVersion)"
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
            :pager-count = "pagerCount"
        ></el-pagination>

        <!-- 新增\修改项目对话框 -->
        <project-version-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :row="row"
            :dialogFormData="projectVersionData"
        ></project-version-dialog>

        <!-- 绑定/解绑项目版本对话框 -->
        <bind-project-version-dialog
            v-if="bindProjectVersionDlgVisible"
            :dialogVisible.sync="bindProjectVersionDlgVisible"
            :row="row"
            :dialogFormData="associatedProjectVersion"
        ></bind-project-version-dialog>
    </div>
</template>

<script>
import ProjectVersionDialog from "./ProjectVersionDialog";
import BindProjectVersionDialog from "./BindProjectVersionDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    props: ["project"],
    data() {
        return {
            // 查询表单
            queryForm: {
                name: "", // 版本名称
            },
            projectVersionData: null, // 存放新增，修改项目用的数据
            dialogVisible: false, // 标识新建\编辑项目对话框是否可见，true - 可见， false - 不可见
            bindProjectVersionDlgVisible: false, // 标识绑定、解绑项目版本对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 迭代对话框标题
        };
    },
    components: {
        ProjectVersionDialog,
        BindProjectVersionDialog,
    },
    methods: {
        queryRows(action) {
            this.tableData = [];
            if (action == 'clickQuery') {
                this.currentPage = 1;
            }
            this.queryForm["pageSize"] = this.pageSize;
            this.queryForm["pageNo"] = this.currentPage;

            if (this.project) {
                this.queryForm["projectId"] = this.project.id;
            } else {
                this.total = 0;
                return;
            }

            // 向后台发送请求
            this.$api.projectVersion
                .getProjectVersions(this.queryForm)
                .then((res) => {
                    if (res.success) {
                        this.total = res.data.total;
                        this.tableData = res.data.rows;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(
                        "获取表记录出错： " + res.msg || res.message
                    );
                });
        },
        addVersion() {
            if (!this.project) {
                this.$alert("请先选择项目", "提示", {
                    confirmButtonText: "确定",
                });
                return;
            }

            if (!this.dialogVisible) {
                this.projectVersionData = {
                    name: "", //名称
                    beginTime: "", // 预估开始时间
                    endTime: "", // 预估结束时间
                    desc: "", // 是否启用
                    projectId: this.project.id,
                    productId: this.project.productId,
                    sprint: null,
                    desc: "", // 描述
                };

                this.dialogVisible = true;
                this.dialogTitle = "新增项目版本";
            }
        },
        editVersion(index, row) {
            if (!this.dialogVisible) {
                this.projectVersionData = {
                    id: row.id,
                    name: row.name,
                    beginTime: row.beginTime,
                    endTime: row.endTime,
                    productId: this.project.productId,
                    sprint: { id: row.sprintId, name: row.sprintName },
                    desc: row.desc,
                };
                this.row = row;
                this.dialogVisible = true;
                this.dialogTitle = "修改项目版本";
            }
        },

        //绑定项目版本
        bindProjectVersion(index, row) {
            this.associatedProjectVersion = {
                projectVersion: null,
            };
            this.row = row;
            this.bindProjectVersionDlgVisible = true;
        },
        // 修改绑定项目版本
        changeProjectVersionAssociated(index, row) {
            this.associatedProjectVersion = {
                projectVersion: {
                    name: row.platformProjectVersionName,
                    id: row.platformProjectVersionId,
                    platform: row.platform,
                },
            };
            this.row = row;
            this.bindProjectVersionDlgVisible = true;
        },
    },
    created() {
        this.queryRows();
    },
    updated() {
        this.setTableBodySize(); // 设置表格高度
    },
};
</script>

<style lang="scss" scoped>
</style>
