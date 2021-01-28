<template>
    <div>
        <el-dialog
            title="关联组别"
            width="45%"
            :visible="dialogVisible"
            :append-to-body="true"
            :show-close="showClose"
            :close-on-click-modal="closeOnClickModal"
            :close-on-press-escape="closeOnPressEscape"
            @close="onCloseDialog"
        >
            <div class="my-dialog-body">
                <el-form :model="dialogForm" ref="dialogForm" :label-width="dialogFormLabeWidth">
                    <el-form-item label="请选择组别">
                        <el-select
                            v-model="optionsSelected"
                            value-key="id"
                            multiple
                            filterable
                            clearable
                            size="medium"
                            style="width:99%"
                            placeholder="请选择组别"
                        >
                            <el-option
                                v-for="item in selectOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item"
                            ></el-option>
                        </el-select>
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
    </div>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "row"],
    mixins: [elDialogMixin],
    data() {
        return {
            selectOptions: [], // group下拉选项
            optionsSelected: [], // 选取的group
        };
    },
    methods: {
        save() {
            const len = this.optionsSelected.length;
            if (!len) {
                // 未选择group
                return;
            }

            let groupIds = [];
            for (let i = 0; i < len; i++) {
                groupIds.push(this.optionsSelected[i].id);
            }

            this.$api.msgPushAccount
                .bindGroups({
                    accountId: this.row.id,
                    groupIds: groupIds,
                })
                .then((res) => {
                    if (res.success) {
                        // 更新列表数据
                        for (let i = 0; i < this.optionsSelected.length; i++) {
                            var groupExists = this.row.groups.some((item) => {
                                if (item.id == this.optionsSelected[i].id) {
                                    return true;
                                }
                            });

                            if (!groupExists) {
                                this.row.groups.push(this.optionsSelected[i]);
                            }
                        }
                        this.closeDialog();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message({
                        message: "绑定失败" + res.msg || res.message,
                        type: "error",
                    });
                });
        },

        // 获取用户未关联的组别
        getUnRelatedGroups() {
            this.$api.msgPushAccount
                .getUnRelatedGroups({
                    accountId: this.row.id,
                })
                .then((res) => {
                    if (res.success) {
                        this.selectOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(
                        " 获取未关联组别失败" + res.msg || res.message
                    );
                });
        },
    },
    created() {
        this.getUnRelatedGroups();
    },
};
</script>

<style scoped lang="scss">
</style>
