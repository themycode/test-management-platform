<template>
    <el-dialog
        :title="dialogTitle"
        width="40%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form
                :model="dialogForm"
                :rules="rules"
                ref="dialogForm"
                label-width="115px"
                class="demo-dialogForm"
            >
                <el-form-item label="计划名称" prop="name">
                    <el-input v-model="dialogForm.name" placeholder="请填写计划名称" class="datetime-input-style"></el-input>
                </el-form-item>
                <el-form-item label="预估开始日期" prop="beginTime">
                    <el-date-picker
                        v-model="dialogForm.beginTime"
                        type="date"
                        placeholder="预估计划开始日期"
                        value-format="yyyy-MM-dd"
                        class="datetime-input-style"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="预估结束日期" prop="endTime">
                    <el-date-picker
                        v-model="dialogForm.endTime"
                        type="date"
                        placeholder="预估计划结束日期"
                        value-format="yyyy-MM-dd"
                        class="datetime-input-style"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="关联迭代" prop="sprint">
                    <el-select
                        v-model="dialogForm.sprint"
                        :disabled="dialogForm.planId && row.caseNumRelated != 0"
                        :multiple="false"
                        filterable
                        value-key="id"
                        placeholder="请选择迭代"
                        class="datetime-input-style"
                    >
                        <el-option
                            v-for="item in sprintOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="关联项目" prop="projectIds">
                    <el-select
                        filterable
                        v-model="dialogForm.projectIds"
                        :multiple="true"
                        placeholder="请选择项目"
                        class="datetime-input-style"
                    >
                        <el-option
                            v-for="item in projectOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="执行环境" prop="envNames">
                    <el-select
                        v-model="dialogForm.envNames"
                        :multiple="true"
                        clearable
                        placeholder="请选择计划执行环境"
                        class="datetime-input-style"
                    >
                        <el-option
                            v-for="item in envOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="计划描述" prop="desc">
                    <el-input v-model="dialogForm.desc" type="textarea" class="datetime-input-style"></el-input>
                </el-form-item>
                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog">取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')">保存</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: [
        "dialogVisible",
        "dialogTitle",
        "tableData",
        "row",
        "dialogFormData",
        "sprintOptions",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: this.dialogFormData,
            envOptions: [], // 存放执行环境下拉选项
            projectOptions: [], // 存放关联项目下拉选项
            rules: {
                name: [
                    {
                        required: true,
                        message: "请输入测试计划名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "描述不能超过 300 个字符",
                        trigger: "blur",
                    },
                ],
                beginTime: [
                    {
                        required: true,
                        message: "请选择预估开始时间",
                        trigger: "change",
                    },
                ],
                endTime: [
                    {
                        required: true,
                        message: "请选择预估结束时间",
                        trigger: "change",
                    },
                ],
                projectIds: [
                    {
                        required: true,
                        message: "请选择要关联的项目",
                        trigger: "change",
                    },
                ],
                sprint: [
                    {
                        required: true,
                        message: "请选择迭代",
                        trigger: "change",
                    },
                ],
                envNames: [
                    {
                        required: true,
                        message: "请选择执行环境",
                        trigger: "change",
                    },
                ],
            },
        };
    },
    methods: {
        // 保存测试计划
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    const beginTime = new Date(
                        this.dialogForm.beginTime.replace(/-/g, "/")
                    ).getTime();

                    const endTime = new Date(
                        this.dialogForm.endTime.replace(/-/g, "/")
                    ).getTime();

                    if (beginTime > endTime) {
                        this.$message.error("开始时间不能晚于结束时间");
                        return;
                    }

                    this.requestData = JSON.parse(JSON.stringify(this.dialogForm));
                    this.requestData["sprintId"] = this.requestData.sprint.id;
                    this.requestData["sprintName"] = this.requestData.sprint.name;
                    delete this.requestData["sprint"];

                    let projectNameList = [];
                    this.projectOptions.forEach((item) => {
                        if (this.requestData.projectIds.includes(item.id)) {
                            projectNameList.push(item.name);
                        }
                    });
                    this.requestData["projectIds"] = this.requestData["projectIds"].join(
                        ","
                    );
                    this.requestData["envNames"] = this.requestData.envNames.join(",");
                    if (this.requestData.id) {
                        // 如果不存在匹配项，保留原有值
                        let projectNames = this.row.projectNames;
                        if (projectNameList.length) {
                            projectNames = projectNameList.join(",");
                        }
                        this.requestData["projectNames"] = projectNames;

                        this.update(this.$api.sprintTestPlan.updateTestPlan);
                    } else {
                        let projectNames = projectNameList.join(",");
                        this.requestData["projectNames"] = projectNames;

                        this.add(this.$api.sprintTestPlan.addTestPlan);
                    }
                }
            });
        },
        getSprintsDetails() {
            // 请求迭代列表
            this.$api.product
                .getProductSprintsDetails({
                    productId: this.dialogForm.productId,
                })
                .then((res) => {
                    if (res.success) {
                        this.sprintOptions = res.data;
                        if (this.sprintOptions.length) {
                            if (!this.dialogForm.sprint) {
                                this.dialogForm.sprint = this.sprintOptions[0];
                            }
                        }
                    } else {
                        this.sprintOptions = [];
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                    this.sprintOptions = [];
                });
        },
        // 获取产品关联的项目
        getProductProjectOptions() {
            this.projectOptions = [];
            if (!this.dialogForm.productId) {                
                return;
            }
            this.$api.project
                .getProductProjectsDetails({
                    productId: this.dialogForm.productId,
                })
                .then((res) => {
                    if (res.success) {
                        this.projectOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 获取执行环境下拉选项
        getEnvOptions() {
            this.envOptions = [];
            this.$api.env
                .getEnvsDetails()
                .then((res) => {
                    if (res.success) {
                        this.envOptions = res.data;
                    } else {
                        this.$message.error(res.msg);                        
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
    },
    created() {
        this.$parent.getProductSprintsDetails(); // 请求产品关联的最新迭代列表
        this.getProductProjectOptions();
        this.getEnvOptions();
    },
};
</script>

<style scoped lang="scss">
// 修改时间输入框样式，动态适应对话框大小
.datetime-input-style {
    width: 95%;
}
</style>
