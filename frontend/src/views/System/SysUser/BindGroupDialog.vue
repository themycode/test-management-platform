<template>
    <el-dialog
        title="关联组别"
        :visible="dialogVisible"
        :width="dialogWidth"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form :label-width="dialogFormLabeWidth">
                <el-form-item label="组别名称">
                    <el-select
                        v-model="optionsSelected"
                        value-key="id"
                        multiple
                        filterable
                        clearable
                        size="medium"
                        style="width:100%"
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
                        <el-button type="primary" @click="save">保存</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
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

            this.$api.sysUser
                .bindGroups({
                    userId: this.row.id,
                    groupIds: groupIds,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
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
                    this.$message.error(res.msg || res.message);
                });
        },

        // 获取未关联的组别
        getUnRelatedGroups() {
            this.$api.sysUser
                .getUnRelatedGroups({
                    userId: this.row.id,
                })
                .then((res) => {
                    if (res.success) {
                        this.selectOptions = res.data;
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
        this.getUnRelatedGroups();
    },
};
</script>

<style scoped lang="scss"></style>
