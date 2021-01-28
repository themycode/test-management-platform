<template>
    <div class="view-wrapper" ref="viewWrapper" v-resize="setTableBodySize">
        <!-- 操作按钮 -->
        <div ref="tableToolbar" class="table-toolbar">
            <el-button-group>
                <el-button :size="buttonSize" @click="addEnv">新增环境</el-button>
                <el-button :size="buttonSize" @click="deleteRows($api.env.deleteEnvs)">删除环境</el-button>
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
            :cell-class-name="getCellClassName"
            @selection-change="onSelectChange"
            highlight-current-row
        >
            <!--多选复选框-->
            <el-table-column type="selection" :width="checkBoxColWidth" align="center"></el-table-column>
            <!-- <el-table-column prop="id" label="ID" width="70px" header-align="center" align="center"></el-table-column> -->
            <el-table-column
                prop="name"
                label="环境名称"
                header-align="center"
                align="left"
                min-width="250px"
            ></el-table-column>
            <el-table-column
                prop="desc"
                label="环境描述"
                header-align="center"
                align="left"
                min-width="400px"
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
            <el-table-column label="操作" align="left" width="160px">
                <template slot-scope="scope">
                    <el-button
                        size="mini"
                        @click="editEnv(scope.$index, scope.row)"
                    >编辑</el-button>
                    <el-button
                        size="mini"
                        type="danger"
                        @click="deleteRow(scope.$index, scope.row, $api.env.deleteEnv)"
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
        <env-dialog
            v-if="dialogVisible"
            :dialogVisible.sync="dialogVisible"
            :dialogTitle="dialogTitle"
            :tableData="tableData"
            :dialogFormData="envData"
            :row="row"
        ></env-dialog>
    </div>
</template>

<script>
import EnvDialog from "./Env/EnvDialog";
import { elTableMixin } from "@/common/mixins/elTableMixin";
import { elButtonMixin } from "@/common/mixins/elButtonMixin";

export default {
    mixins: [elTableMixin, elButtonMixin],
    name: "Env",
    data() {
        return {
            envData: null, // 存放新增，修改时的环境数据
            dialogVisible: false, // 标识新建\编辑迭代对话框是否可见，true - 可见， false - 不可见
            dialogTitle: "", // 迭代对话框标题
        };
    },
    components: {
        EnvDialog,
    },
    methods: {
        addEnv() {
            if (!this.dialogVisible) {
                this.envData = {
                    name: "",
                    desc: "",
                };

                this.dialogVisible = true;
                this.dialogTitle = "新增环境";
            }
        },
        editEnv(index, row) {
            if (!this.dialogVisible) {
                this.envData = {
                    id: row.id,
                    name: row.name,
                    desc: row.desc,
                };
                this.row = row;
                this.dialogVisible = true;
                this.dialogTitle = "修改环境";
            }
        },
    },
    updated() {
        this.setTableBodySize();
    },

    created() {
        this.queryRowsAPI = this.$api.env.getEnvs;
        this.queryRows();
    },
};
</script>

<style lang="scss">
</style>
