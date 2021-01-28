<template>
    <el-dialog
        title="导入用例"
        width="45%"
        :visible="dialogVisible"
        :append-to-body="true"
        :show-close="false"
    >
        <div class="my-dialog-body">
            <div style="margin:0px 0px 10px 0px">
                <el-link
                    type="primary"
                    href="/static/templates/system_testcase_template.xlsx"
                    download="system_testcase_template.xlsx"
                >点击下载系统用例模板(Excel)</el-link>
                <span style="margin-right:30px;"></span>
                <el-link
                    type="primary"
                    href="/static/templates/system_testcase_template.xmind"
                    download="system_testcase_template.xmind"
                >点击下载系统用例模板(XMind)</el-link>
            </div>
            <div style="display:inline;padding-right:5px;">
                <el-select v-model="caseTemplateType" size="small" placeholder="请选择用例模板类型">
                    <el-option
                        v-for="item in caseFormatOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </div>
            <el-upload
                style="display:inline"
                class="upload-demo"
                action="fakeAction"
                :http-request="importTestcase"
                :with-credentials="true"
                :accept="fileTypeAccept"
                :show-file-list="false"
            >
                <el-button size="small" type="primary">点击上传用例</el-button>
                <div slot="tip" class="el-upload__tip">
                    注意：
                    <br />1、目前仅支持上传excel文件，上传用例文件后，自动导入用例
                    <br />2、导入过程中请不要刷新页面，可能耗时较长，因文件大小而不同，用例导入后手动刷新页面查看导入数据
                </div>
            </el-upload>
        </div>
        <div class="dialog-footer">
            <el-button type="primary" @click="closeDialog">关闭</el-button>
        </div>
    </el-dialog>
</template>

<script>
import constant from "@/common/constant";

export default {
    props: ["dialogVisible", "dataForImportCase"],
    data() {
        return {
            urlForCaseImport: constant.urlForCaseImport, // 附件上传地址
            // 可接受文件类型（打开文件选取对话框时,文件后缀名自动设置为此处设置的）
            // fileTypeAccept: ".xls,.xlsx,.xmind",
            // fileTypeAccept:"application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            // 导入用例模板
            caseFormatOptions: [
                {
                    value: "SYSTEM_EXCEL_TESTCASE_TEPLATE",
                    label: "系统用例模板(Excel)",
                },
                {
                    value: "SYSTEM_XMIND_TESTCASE_TEPLATE",
                    label: "系统用例模板(XMind)",
                },
            ],
            caseTemplateType: "SYSTEM_EXCEL_TESTCASE_TEPLATE",
        };
    },
    methods: {
        closeDialog() {
            this.$emit("update:dialogVisible", false); // 关闭对话框
        },
        importTestcase(params) {
            const file = params.file;
            // 文件大小校验
            if (!file.size) {
                // file.size默认字节为单位
                this.$message.error("上传失败，用例模板为空");
                return;
            }

            // 文件类型校验
            let tempArr = file.name.split(".");
            let fileNameSuffix = tempArr[tempArr.length - 1];
            if (this.fileTypeAccept.indexOf(fileNameSuffix) == -1) {
                this.$message.error(
                    "用例模板格式错误，支持的文件格式为：" + this.fileTypeAccept
                );
                return false;
            }
            this.$parent.loading = true;
            let form = new FormData();
            form.append("file", file);
            form.append("productId", this.dataForImportCase.productId);
            form.append("caseTemplateType", this.caseTemplateType);
            this.$api.sprintCaseTable
                .importTestCases(form)
                .then((res) => {
                    if (res.success) {
                        this.$alert(res.msg, "提示", {
                            confirmButtonText: "确定",
                            dangerouslyUseHTMLString: true,
                            callback: (action) => {
                                this.$parent.queryRows();
                            },
                        });
                    } else {
                        this.$alert(res.msg, "提示", {
                            confirmButtonText: "确定",
                            dangerouslyUseHTMLString: true,
                        });
                    }
                    this.$parent.loading = false;
                })
                .catch((res) => {
                    this.$parent.loading = false;
                    this.$alert(res.msg || res.message, "提示", {
                        confirmButtonText: "确定",
                    });
                });
            this.closeDialog();
        },
    },
    computed: {
        fileTypeAccept: {
            get() {
                if (this.caseTemplateType === "SYSTEM_EXCEL_TESTCASE_TEPLATE") {
                    return ".xls,.xlsx";
                } else if (
                    this.caseTemplateType === "SYSTEM_XMIND_TESTCASE_TEPLATE"
                ) {
                    return ".xmind";
                } else {
                    return "";
                }
            },
        },
    },
};
</script>

<style scoped>
</style>
