<template>
    <el-dialog
        :title="dialogTitle"
        width="50%"
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
                :label-width="dialogFormLabeWidth"
            >
                <el-form-item label="产品名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="产品编码" prop="code">
                    <el-input v-model="dialogForm.code"></el-input>
                </el-form-item>
                <el-form-item label="产品状态" prop="status">
                    <el-select v-model="dialogForm.status" placeholder="请选择">
                        <el-option
                            v-for="item in statusOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="产品负责人" prop="productOwner">
                    <el-select
                        v-model="dialogForm.productOwner"
                        filterable
                        clearable
                        value-key="id"
                        placeholder="请选择"
                    >
                        <el-option
                            v-for="item in userOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="研发负责人" prop="developOwner">
                    <el-select
                        v-model="dialogForm.developOwner"
                        filterable
                        clearable
                        value-key="id"
                        placeholder="请选择"
                    >
                        <el-option
                            v-for="item in userOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="测试负责人" prop="testOwner">
                    <el-select
                        v-model="dialogForm.testOwner"
                        filterable
                        clearable
                        value-key="id"
                        placeholder="请选择"
                    >
                        <el-option
                            v-for="item in userOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="产品描述" prop="desc">
                    <el-input v-model="dialogForm.desc" type="textarea"></el-input>
                </el-form-item>

                <el-form-item>
                    <div class="dialog-footer">
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
        "dialogFormData",
        "tableData",
        "statusOptions",
        "row",
    ],
    mixins: [elDialogMixin],
    data() {
        return {
            dialogForm: Object.assign({}, this.dialogFormData),
            productOptions: [], // 存放关联产品下拉选项
            userOptions: [], // 存放产品、研发、测试负责人下拉选项
            rules: {
                name: [
                    {
                        required: true,
                        message: "请填写产品名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                code: [
                    {
                        required: false,
                        message: "请填写产品编码",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                status: [
                    {
                        required: true,
                        message: "请选择产品状态",
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 500,
                        message: "产品描述不能超过 500 个字符",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        // 新增
        addProduct() {
            this.requestData = {
                name: this.dialogForm.name,
                code: this.dialogForm.code,
                status: this.dialogForm.status,
                productOwnerId: this.dialogForm.productOwner.id,
                productOwner: this.dialogForm.productOwner.name,
                developOwnerId: this.dialogForm.developOwner.id,
                developOwner: this.dialogForm.developOwner.name,
                testOwnerId: this.dialogForm.testOwner.id,
                testOwner: this.dialogForm.testOwner.name,
                desc: this.dialogForm.desc, // 产品描述
            };

            this.add(this.$api.product.addProduct);
        },
        // 修改
        updateProduct() {
            this.requestData = {
                id: this.dialogForm.id,
                name: this.dialogForm.name,
                code: this.dialogForm.code,
                status: this.dialogForm.status,
                productOwnerId: this.dialogForm.productOwner.id,
                productOwner: this.dialogForm.productOwner.name,
                developOwnerId: this.dialogForm.developOwner.id,
                developOwner: this.dialogForm.developOwner.name,
                testOwnerId: this.dialogForm.testOwner.id,
                testOwner: this.dialogForm.testOwner.name,
                desc: this.dialogForm.desc,
            };

            this.update(this.$api.product.updateProduct);
        },
        // 保存
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.addProduct();
                    } else {
                        this.updateProduct();
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
    created() {
        this.$api.sysUser
            .getUsersDetails()
            .then((res) => {
                if (res.success) {
                    this.userOptions = res.data;
                } else {
                    this.$message.error(res.msg);
                }
            })
            .catch((res) => {
                this.$message.error(res.msg || res.message);
            });
    },
};
</script>

<style scoped>

</style>
