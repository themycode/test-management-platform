<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 查询表单 -->
        <div class="table-query-form" ref="queryForm">
            <el-form :inline="true" :model="queryForm" size="small">
                <el-form-item label="项目名称">
                    <el-input
                        v-model="queryForm.name"
                        placeholder="请输入项目名称"
                        clearable
                        style="width:240px"
                    ></el-input>
                </el-form-item>

                <el-form-item label="项目状态">
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
                    <el-button type="primary" @click="queryRows('clickQuery')">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addProject">新增项目</el-button>
                <el-button :size="buttonSize" @click="deleteRows($api.project.deleteProjects)">删除项目</el-button>
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
                label="项目名称"
                header-align="center"
                align="left"
                min-width="180px"
                show-overflow-tooltip
            ></el-table-column>
            <el-table-column
                prop="status"
                label="项目状态"
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
                label="项目描述"
                header-align="center"
                align="center"
                show-overflow-tooltip
                min-width="200px"
            ></el-table-column>
            <el-table-column
                prop="platformProjectName"
                label="关联项目"
                header-align="center"
                align="center"
                show-overflow-tooltip
                min-width="200px"
            >
                <template slot-scope="scope">
                    <el-link
                        type="primary"
                        v-if="scope.row.platformProjectName"
                        @click="changeProjectAssociated(scope.$index, scope.row)"
                    >
                        {{ scope.row.platformProjectName }}
                        <i class="el-icon-edit"></i>
                    </el-link>
                    <el-button v-else size="mini" @click="bindProject(scope.$index, scope.row)">
                        <i class="fa fa-plus" aria-hidden="true"></i>关联项目
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
            <el-table-column label="操作" align="left" width="160px">
                <template slot-scope="scope">
                    <el-button size="mini" @click="editProject(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.project
                        .deleteProject)"
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

        <!-- 新增\修改项目对话框 -->
        <project-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :statusOptions="statusOptions"
            :row="row"
            :dialogFormData="projectData"
        ></project-dialog>

        <!-- 绑定/解绑项目对话框 -->
        <bind-project-dialog
            v-if="bindProjectDlgVisible"
            :dialogVisible.sync="bindProjectDlgVisible"
            :row="row"
            :dialogFormData="associatedProjectData"
        ></bind-project-dialog>
    </div>
</template>

<script>
import ProjectDialog from "./Project/ProjectDialog";
import BindProjectDialog from "./Project/BindProjectDialog";
import { mapState } from "vuex";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    components: {
        ProjectDialog,
        BindProjectDialog,
    },
    data() {
        return {
            // 查询表单
            queryForm: {
                name: "", // 项目名称
                status: "", //项目状态
            },
            projectData: null, // 存放新增，修改项目用的数据
            statusOptions: [
                // 状态选项
                { label: "未开始", value: "未开始" },
                { label: "进行中", value: "进行中" },
                { label: "已结束", value: "已结束" },
            ],

            dialogVisible: false, // 标识新建\编辑项目对话框是否可见，true - 可见， false - 不可见
            bindProjectDlgVisible: false, // 标识关联项目\解绑项目对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 项目对话框标题
            loading: false, // 防短时间内重复点击，遮罩加载表示
            loadingText: "",
        };
    },

    methods: {
        addProject() {
            if (!this.dialogVisible) {
                this.projectData = {
                    name: "", //名称
                    beginTime: "", // 预估开始时间
                    endTime: "", // 预估结束时间
                    status: "进行中", // 状态
                    desc: "", // 描述
                };
                this.dialogVisible = true;
                this.dialogTitle = "新增项目";
            }
        },
        editProject(index, row) {
            if (!this.dialogVisible) {
                this.projectData = {
                    id: row.id,
                    name: row.name,
                    productId: row.productId,
                    beginTime: row.beginTime,
                    endTime: row.endTime,
                    status: row.status,
                    desc: row.desc,
                };
                this.row = row;
                this.dialogVisible = true;
                this.dialogTitle = "修改项目";
            }
        },
        //绑定项目
        bindProject(index, row) {
            this.associatedProjectData = {
                platform: "jira",
                project: null,
                defectIssueTypeId: "",
                defectSourceField: "",
                defectSeverityField: "",
                defectStatusMap: "",
                defectSeverityMap: "",
                customFieldMap:{},
                customFieldMapArray:[]
            };
            this.row = row;
            this.bindProjectDlgVisible = true;
        },
        // 修改绑定项目
        changeProjectAssociated(index, row) {
            let customFieldMap = typeof row.customFieldMap === typeof ""? JSON.parse(row.customFieldMap): row.customFieldMap;
            let customFieldMapArray = [];
            for (let item in customFieldMap){
                customFieldMapArray.push({key:item, value:customFieldMap[item]})
            }
            this.associatedProjectData = {
                platform: row.platform,
                project: {
                    name: row.platformProjectName,
                    id: row.platformProjectId,
                },
                defectIssueTypeId: row.defectIssueTypeId,
                defectSourceField: row.defectSourceField,
                defectSeverityField: row.defectSeverityField,
                defectStatusMap: row.defectStatusMap,
                defectSeverityMap: row.defectSeverityMap,
                customFieldMap:customFieldMap,
                customFieldMapArray:{},
                customFieldMapArray:customFieldMapArray,
            };
            this.row = row;
            this.bindProjectDlgVisible = true;
        },
    },
    updated() {
        this.setTableBodySize();
    },
    created() {
        this.queryRowsAPI = this.$api.project.getProjects;
        this.queryRows();
    },
};
</script>

<style lang="scss" scoped>
</style>
