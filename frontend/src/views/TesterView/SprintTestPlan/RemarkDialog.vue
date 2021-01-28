<template>
    <div>
        <el-dialog
            title="备注信息"
            width="50%"
            :visible="dialogVisible"
            :append-to-body="true"
            :show-close="showClose"
            @close="onCloseDialog"
        >
            <div class="my-dialog-body">
                <el-input
                    type="textarea"
                    :autosize="{ minRows: 8 }"
                    maxlength="1000"
                    show-word-limit
                    placeholder="请输入测试备注信息"
                    v-model="testRemark"
                ></el-input>
            </div>

            <span slot="footer">
                <el-button @click="closeDialog">取 消</el-button>
                <el-button type="primary" @click="save">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "row"],
    mixins: [elDialogMixin],
    data() {
        return {
            testRemark: this.row.remark, // 测试用例测试备注信息
        };
    },
    methods: {
        save() {
            this.requestData = {
                id: this.row.id,
                remark: this.testRemark,
                planId:this.row.testplanId
            };
            this.update(this.$api.testPlanCaseTable.updateTestCase);
        },
    },
};
</script>
<style scoped>
.my-dialog-body {
    padding: 0px;
}
</style>>
